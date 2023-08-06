###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Helper functions.
"""


def parse_connection_args(db_url: str = None):
    """
    Return a dictionary with the arguments needed to connect to the required
    CouchDB instance, and the name of the database to use.

    >>> parse_connection_args('http://admin:pass@localhost:5984/nightly-builds')
    ({'url': 'http://localhost:5984', 'user': 'admin', 'auth_token': 'pass'}, 'nightly-builds')
    """
    from urllib.parse import SplitResult, urlsplit

    import lb.nightly.configuration

    try:
        config = (lb.nightly.configuration.service_config() or {}).get("couchdb")
    except FileNotFoundError:
        config = {}

    if db_url is None:
        db_url = config["url"]

    parts = urlsplit(db_url)

    # extract user and password from the url
    if "@" not in parts.netloc:
        user = auth_token = None
        netloc = parts.netloc
    else:
        user, netloc = parts.netloc.split("@")
        if ":" not in user:
            raise ValueError("url does not contain password")
        user, auth_token = user.split(":", 1)

    # check for valid path
    if not parts.path or parts.path.endswith("/"):
        raise ValueError("url path must be present and not end with '/'")

    # extract db name from path
    path, db_name = parts.path.rsplit("/", 1)
    # make sure any trailing parts in the url (e.g. reverse proxy)
    # are not interpreted as db names
    if path:
        path += "/"

    return (
        {
            "url": SplitResult(
                scheme=parts.scheme, netloc=netloc, path=path, query="", fragment=""
            ).geturl(),
            "user": user,
            "auth_token": auth_token,
        },
        db_name,
    )


VIEWS = [
    {
        "_id": "_design/summaries",
        "language": "javascript",
        "options": {"partitioned": True},
        "views": {
            "by_day": {
                "map": """function(doc) {
  if (doc.type == 'slot-info') {
    var proj_names = [];
    doc.config.projects.forEach(function(project) {
      if (!project.disabled) proj_names.push(project.name);
    });
    emit(doc.date, {
      slot: doc.slot,
      build_id: doc.build_id,
      projects: proj_names,
      platforms: doc.config.platforms
    });
  }
}
"""
            },
            "latest_builds": {
                "map": """function(doc) {
  if (doc.type == "slot-info") {
    if (doc.date)
      emit(doc.slot, [doc.build_id, new Date(doc.date).getTime()]);
  }
}
""",
                "reduce": "_stats",
            },
        },
    },
    {
        "_id": "_design/_auth",
        "language": "javascript",
        "options": {"partitioned": False},
        "validate_doc_update": """
        function(newDoc, oldDoc, userCtx, secObj) {
            // only admins or writers can edit documents
            if ((userCtx.roles.indexOf('_admin') !== -1) ||
                (userCtx.roles.indexOf('writer') !== -1)) {
                return;
            } else {
                throw({forbidden: 'Only admins or writers may modify documents.'});
            }
        }
        """,
    },
    {
        "_id": "_design/names",
        "language": "javascript",
        "options": {"partitioned": True},
        "views": {
            "platforms": {
                "map": """function(doc) {
  if (doc.type == "slot-info") {
    doc.config.platforms.forEach(function(platform) {
      if (doc.date)
        emit(platform, new Date(doc.date).getTime());
    });
  }
}
""",
                "reduce": "_stats",
            },
            "projects": {
                "map": """function(doc) {
  if (doc.type == "slot-info") {
    doc.config.projects.forEach(function(project) {
      if (doc.date)
        emit(project.name, new Date(doc.date).getTime());
    });
  }
}
""",
                "reduce": "_stats",
            },
            "slots": {
                "map": """function(doc) {
  if (doc.type == "slot-info") {
    if (doc.date)
      emit(doc.slot, new Date(doc.date).getTime());
  }
}
""",
                "reduce": "_stats",
            },
        },
    },
    {
        "_id": "_design/artifacts",
        "language": "javascript",
        "options": {"partitioned": False},
        "views": {
            "summary": {
                "map": """function(doc) {
  if (doc.type == "slot-info") {
    if (doc.checkout && doc.checkout.projects) {
      for(var name in doc.checkout.projects) {
        var info = doc.checkout.projects[name];
        if (info.artifact){
          emit(info.artifact, info);
        }
      }
    }
    if (doc.builds) {
      for(var platform in doc.builds) {
        for(var project in doc.builds[platform]) {
            var info = doc.builds[platform][project];
            if (info.artifact) {
              emit(info.artifact, info);
            }
        }
      }
    }
    if (doc.tests) {
      for(var platform in doc.tests) {
        for(var project in doc.tests[platform]) {
            var info = doc.tests[platform][project];
            if (info.artifact) {
              emit(info.artifact, info);
            }
        }
      }
    }
  }
}
""",
            },
        },
    },
    {
        "_id": "_design/state",
        "language": "javascript",
        "options": {"partitioned": False},
        "views": {
            "aborted": {
                "map": """function (doc) {
  if (doc.type == "slot-info" && doc.aborted) {
    emit(doc.config.metadata.flavour + "/" + doc.slot + "/" + doc.build_id, doc.aborted);
  }
}
"""
            }
        },
    },
    {
        "_id": "_design/mango_indexes",
        "language": "query",
        "options": {"partitioned": True},
        "views": {
            "slot-build_id": {
                "map": {
                    "fields": {"slot": "asc", "build_id": "asc"},
                    "partial_filter_selector": {},
                },
                "reduce": "_count",
                "options": {"def": {"fields": [{"slot": "asc"}, {"build_id": "asc"}]}},
            }
        },
    },
]


def init_db(db_url=None, overwrite=False):
    """
    Create and initialize a CouchDB database for use with the nightlies
    (including required views).

    If overwrite is set to True, the views are overwritten.
    """
    from urllib.parse import urlsplit

    from cloudant.client import CouchDB

    args, db_name = parse_connection_args(db_url)

    server = CouchDB(**args, connect=True, auto_renew=True)

    if db_name in server:
        db = server[db_name]
    else:
        db = server.create_database(db_name, partitioned=True)

    # FIXME: we should select which view to create for which flavour
    for doc in VIEWS:
        doc = dict(doc)
        if doc["_id"] not in db:
            db.create_document(doc)
        else:
            if overwrite:
                db_doc = db[doc["_id"]]
                db_doc.update(doc)
                db_doc.save()

    # make sure that the DB is publicly readable
    security = db.get_security_document()
    security["members"] = {}
    security.save()
    return db


class LockTakenError(Exception):
    def __str__(self):
        return "somebody already holds the lock for {}".format(*self.args)
