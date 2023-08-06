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
import datetime
import logging
from contextlib import contextmanager
from socket import gethostname
from time import sleep
from typing import Iterable, Optional, Tuple, Union

from lb.nightly.configuration import Slot

from .utils import LockTakenError

MAX_TIME_BETWEEN_CONNECTIONS = datetime.timedelta(minutes=5)


class Database:
    """
    Wrapper around a CouchDB database providing common utilities.
    """

    def __init__(self, db):
        assert db.metadata()["props"].get(
            "partitioned"
        ), "the database must be partitioned"

        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self._db_instance = db
        self._db_last_access = datetime.datetime.now()

    @property
    def _db(self):
        """
        Wrapper around the CouchDB database instance to make sure the connection
        is always valid.
        """
        now = datetime.datetime.now()
        time_since_connection = now - self._db_last_access
        if time_since_connection > MAX_TIME_BETWEEN_CONNECTIONS:
            self._log.debug(
                "reconnecting to %s after %s",
                self._db_instance.client.server_url,
                time_since_connection,
            )
            self._db_instance.client.connect()
            self._db_last_access = now
        return self._db_instance

    @staticmethod
    def docname(slot: Union[Slot, str, Tuple[str, str, int]]):
        """
        Return the document name for a given slot, or the argument if that is a
        string.

        >>> Database.docname(Slot('some-slot', build_id=123))
        'nightly:some-slot:123'
        >>> Database.docname('testing:example:0')
        'testing:example:0'
        >>> Database.docname(('special', 'test', 42))
        'special:test:42'
        """
        if isinstance(slot, Slot):
            return f"{slot.flavour}:{slot.name}:{slot.build_id}"
        elif isinstance(slot, tuple) and len(slot) == 3:
            return "{}:{}:{}".format(*slot)
        elif isinstance(slot, str):
            return slot
        raise TypeError(f"invalid argument, expected Slot, str or tuple")

    def exists(self, slot):
        """
        True if the given slot is in the database.
        """
        return self.docname(slot) in self._db

    def __getitem__(self, slot):
        """
        Return the database document for the given slot.
        """
        return self._db[self.docname(slot)]

    def __contains__(self, slot):
        """
        Check if a given slot build (or slot key) is in the database.
        """
        return self.docname(slot) in self._db

    def getAll(self, slots: Iterable[Union[Slot, str, Tuple[str, str, int]]]):
        """
        Get multiple docs in one go.
        """
        for row in self._db.all_docs(
            keys=[self.docname(slot) for slot in slots], include_docs=True
        )["rows"]:
            yield row["doc"]

    @staticmethod
    def _slot2doc(slot: Slot):
        """
        Return the CouchDB document for a given slot.
        """
        return {
            "_id": Database.docname(slot),
            "type": "slot-info",
            "slot": slot.name,
            "build_id": slot.build_id,
            "date": str(datetime.date.today()),
            "config": slot.toDict(),
        }

    def add(self, slot: Slot):
        """
        Add the slot object to the database.

        If the slot build id is not set, the next available one is used.

        Return the slot instance that was passed, possibly modified with the
        set build id.
        """
        from cloudant.error import CloudantDatabaseException

        if slot.build_id:
            self._db.create_document(self._slot2doc(slot), throw_on_exists=True)
            return slot
        else:
            slot.build_id = self.lastBuildId(slot.name, slot.flavour) + 1
            while True:
                try:
                    return self.add(slot)
                except CloudantDatabaseException as err:
                    if "exists" not in str(err):
                        raise
                    slot.build_id += 1

    def lastBuildId(self, name: str, flavour: str = "nightly"):
        """
        Return the last build id in the database for a given slot, 0 if the slot
        is not present.
        """
        for entry in self._db.get_partitioned_view_result(
            flavour,
            "_design/summaries",
            "latest_builds",
            group=True,
            key=name,
        ):
            return entry["value"][0]["max"]
        return 0

    def slotBuilds(self, name: str, flavour: str = "nightly", min_id: int = -1):
        """
        Return all builds (id and date) of a given slots, with id greater or equal to min_id.
        """
        return [
            (entry["build_id"], entry["date"])
            for entry in self._db.get_partitioned_query_result(
                flavour,
                selector={"slot": name, "build_id": {"$gte": min_id}},
                fields=["build_id", "date"],
            )
        ]

    def latestSlotsBuilt(self, flavour: str = "nightly", since: datetime.date = None):
        """
        Return the latest builds of the known slots, optionally keeping
        only those more recent than 'since'.

        The format of the output is::

            {<slot name>: {'build_id': <build id>, 'id': <document id>}, ...}
        """
        if since is not None:
            # Note: timestamps in JS are in milliseconds
            since = int((since - datetime.date.fromtimestamp(0)).total_seconds() * 1000)
        else:
            since = 0

        return {
            entry["key"]: {
                "build_id": entry["value"][0]["max"],
                "id": Database.docname(
                    (flavour, entry["key"], entry["value"][0]["max"])
                ),
            }
            for entry in self._db.get_partitioned_view_result(
                flavour,
                "_design/summaries",
                "latest_builds",
                group=True,
            )
            if entry["value"][1]["max"] >= since
        }

    def slotsForDay(self, day: Union[str, datetime.date], flavour: str = "nightly"):
        """
        Get basic infos for the slots built in a day.

        Each entry has the form::

            {'slot': '<slot name>',
             'build_id': <build id of the slot>,
             'projects': [<list of project names>],
             'platforms': [<list of platform names>]}
        """
        return [
            row["value"]
            for row in self._db.get_partitioned_view_result(
                flavour, "_design/summaries", "by_day", key=str(day)
            )
        ]

    def slotsSinceDay(self, day: Union[str, datetime.date], flavour: str = "nightly"):
        """
        Get basic infos for the slots built since a day.

        Each entry has the form::

            (date,
             {'slot': '<slot name>',
              'build_id': <build id of the slot>,
              'projects': [<list of project names>],
              'platforms': [<list of platform names>])
        """
        return [
            (row["key"], row["value"])
            for row in self._db.get_partitioned_view_result(
                flavour, "_design/summaries", "by_day", startkey=str(day)
            )
        ]

    def slotDocs(self, name: str, flavour: str = "nightly"):
        """
        Return, as a query result, all documents for a given slot in
        reverse build_id order.

        The returned object can be sliced to reduce the amount of data retrieved.
        """
        return self._db.get_partitioned_query_result(
            flavour, selector={"slot": name}, sort=[{"build_id": "desc"}]
        )

    @staticmethod
    def apply(func, doc):
        """
        Apply changes to a doc and save changes, retrying if conflicts.
        """
        from requests import HTTPError

        while True:
            func(doc)
            try:
                doc.save()
                break
            except HTTPError as err:
                if "Conflict" not in str(err):
                    raise
                doc.fetch()

    def checkout_start(self, project, worker_task_id):
        def update(doc):
            if "checkout" not in doc:
                doc["checkout"] = {"projects": {}}
            elif "projects" not in doc["checkout"]:
                doc["checkout"]["projects"] = {}

            previous = doc["checkout"]["projects"].get(project.name)

            if previous:
                self._log.warning(
                    "overriding checkout of %s: %r", project.name, previous
                )

            doc["checkout"]["projects"][project.name] = {
                "started": str(datetime.datetime.now()),
                "hostname": gethostname(),
                "worker_task_id": worker_task_id,
            }

            if previous:
                doc["checkout"]["projects"][project.name]["previous"] = previous

        self.apply(update, self[project.slot])

    def set_dependencies(self, project):
        dependencies = project.dependencies()

        def update(doc):
            for proj in doc["config"]["projects"]:
                if proj["name"] == project.name:
                    if proj["dependencies"] != dependencies:
                        proj["dependencies"] = dependencies
                    break

        self.apply(update, self[project.slot])

    def checkout_complete(
        self,
        project,
        artifact,
        report,
        worker_task_id,
    ):
        def update(doc):
            proj = doc["checkout"]["projects"][project.name]
            assert (
                proj["hostname"] == gethostname()
            ), "trying to complete a checkout started by somebody else"
            assert (
                proj["worker_task_id"] == worker_task_id
            ), "trying to complete a checkout started by somebody else"
            proj["completed"] = str(datetime.datetime.now())
            proj["merges"] = report.merges
            proj["submodules"] = report.submodules
            proj["tree"] = report.tree
            proj["warnings"] = []
            proj["errors"] = []
            proj["artifact"] = artifact
            try:
                proj["dependencies"] = project.dependencies()
            except AttributeError:
                # 'Package' object has no attribute 'dependencies'
                proj["dependencies"] = []

            for level in ("warning", "error"):
                proj[f"{level}s"] = [
                    r["text"] for r in report.records if r["level"] == level
                ]

        self.apply(update, self[project.slot])

    def reuse_checkout(self, project, artifact):
        """
        Set checkout summary details from another checkout that produced the
        same artifact.

        Return True if such summary could be found, False otherwise.
        """
        summary = self.get_artifact_summary(artifact)

        if summary:

            def update_summary(doc):
                if "checkout" not in doc:
                    doc["checkout"] = {}
                if "projects" not in doc["checkout"]:
                    doc["checkout"]["projects"] = {}
                doc["checkout"]["projects"][project.name] = summary
                for prj in doc["config"]["projects"]:
                    if prj["name"] == project.name:
                        prj["dependencies"] = summary["dependencies"]
                        break

            self.apply(update_summary, self[project.slot])

            return True

        else:
            return False

    def build_start(self, project, platform, worker_task_id):
        def update(doc):
            if "builds" not in doc:
                doc["builds"] = {}
            if platform not in doc["builds"]:
                doc["builds"][platform] = {}

            previous = doc["builds"][platform].get(project.name)

            if previous:
                self._log.warning(
                    "overriding build of %s %s: %r", project.name, platform, previous
                )

            doc["builds"][platform][project.name] = {
                "started": str(datetime.datetime.now()),
                "hostname": gethostname(),
                "worker_task_id": worker_task_id,
            }

            if previous:
                doc["builds"][platform][project.name]["previous"] = previous

        self.apply(update, self[project.slot])

    def build_complete(self, project, platform, artifact, reports, worker_task_id):
        def update(doc):
            proj = doc["builds"][platform][project.name]
            assert (
                proj["hostname"] == gethostname()
            ), "trying to complete a build started by somebody else"
            assert (
                proj["worker_task_id"] == worker_task_id
            ), "trying to complete a build started by somebody else"
            proj["completed"] = str(datetime.datetime.now())
            proj["warnings"] = reports["warnings"]
            proj["errors"] = reports["errors"]
            proj["retcode"] = reports["retcode"]
            proj["artifact"] = artifact

        self.apply(update, self[project.slot])

    def tests_start(self, project, platform, worker_task_id):
        def update(doc):
            if "tests" not in doc:
                doc["tests"] = {}
            if platform not in doc["tests"]:
                doc["tests"][platform] = {}

            previous = doc["tests"][platform].get(project.name)

            if previous:
                self._log.warning(
                    "overriding test of %s %s: %r", project.name, platform, previous
                )

            doc["tests"][platform][project.name] = {
                "started": str(datetime.datetime.now()),
                "hostname": gethostname(),
                "worker_task_id": worker_task_id,
            }

            if previous:
                doc["tests"][platform][project.name]["previous"] = previous

        self.apply(update, self[project.slot])

    def tests_complete(self, project, platform, artifact, reports, worker_task_id):
        def update(doc):
            proj = doc["tests"][platform][project.name]
            assert (
                proj["hostname"] == gethostname()
            ), "trying to complete a test started by somebody else"
            assert (
                proj["worker_task_id"] == worker_task_id
            ), "trying to complete a test started by somebody else"
            proj["completed"] = str(datetime.datetime.now())
            proj["artifact"] = artifact
            proj["results"] = reports["results"]

        self.apply(update, self[project.slot])

    def get_artifact_summary(self, artifact):
        """
        Return the task summary for the job that produced a given artifact, or
        None if the artifact is unknown.
        """
        # FIXME: we do not really care which of the possible summaries we get
        result = self._db.get_view_result(
            "_design/artifacts",
            "summary",
            key=artifact,
            limit=1,
        ).all()

        return result[0]["value"] if result else None

    @contextmanager
    def lock(self, id: str, info: Optional[dict] = None):
        """
        CouchDB backed resource lock.

        The context manager raises LockTakenError if the lock "id" is already taken.
        """
        from cloudant.error import CloudantDatabaseException

        doc_id = f"lock:{id}"
        try:
            self._db.create_document(
                {
                    "_id": doc_id,
                    "type": "lock",
                    "acquired": str(datetime.datetime.now()),
                    "info": info,
                },
                throw_on_exists=True,
            )
        except CloudantDatabaseException:
            # somebody already holds the lock
            raise LockTakenError(doc_id)

        try:
            yield doc_id

        finally:
            self._db[doc_id].delete()

    def reuse_artifact(self, project, artifact, platform=None, stage=None):
        """
        Set summary details from another checkout/build/test that produced the
        same artifact.

        Return True if such summary could be found, False otherwise.
        """
        doc_name = f"{stage}s" if stage else "checkout"
        subdoc_name = platform or "projects"

        summary = self.get_artifact_summary(artifact)

        if summary:

            def update_summary(doc):
                if doc_name not in doc:
                    doc[doc_name] = {}
                if subdoc_name not in doc[doc_name]:
                    doc[doc_name][subdoc_name] = {}
                doc[doc_name][subdoc_name][project.name] = summary
                if not platform and not stage:
                    # need to update dependencies in case of updating checkout
                    for prj in doc["config"]["projects"]:
                        if prj["name"] == project.name:
                            prj["dependencies"] = summary["dependencies"]
                            break

            self.apply(update_summary, self[project.slot])

            return True

        else:
            return False
