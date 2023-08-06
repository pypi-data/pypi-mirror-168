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
__version__ = "0.2.0"


def connect(db_url=None):
    from urllib.parse import urlparse

    from cloudant.client import CouchDB

    from .database import Database
    from .utils import parse_connection_args

    args, db_name = parse_connection_args(db_url)

    if urlparse(args["url"]).scheme not in ("https", "http"):
        raise ValueError(f"URL {args['url']} not supported")

    # Note: the CouchDB client allows unauthenticated access only with
    #       admin_party set to True
    return Database(
        CouchDB(**args, connect=True, admin_party=(args["user"] is None))[db_name]
    )
