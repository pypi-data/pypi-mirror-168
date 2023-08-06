import os

from pydantic import Extra

FORBID_EXTRA_RESULT_FIELDS = os.environ.get("RHINO_SDK_FORBID_EXTRA_RESULT_FIELDS", "").lower() in {
    "1",
    "on",
    "true",
}

RESULT_DATACLASS_EXTRA = Extra.forbid if FORBID_EXTRA_RESULT_FIELDS else Extra.ignore


class Endpoint:
    def __init__(self, session):
        self.session = session
