from typing import List

from classiq.interface.helpers.versioned_model import VersionedModel
from classiq.interface.status import Status


class AnglesResult(VersionedModel):
    status: Status
    details: List[float]


class PyomoObjectResult(VersionedModel):
    status: Status
    details: str
