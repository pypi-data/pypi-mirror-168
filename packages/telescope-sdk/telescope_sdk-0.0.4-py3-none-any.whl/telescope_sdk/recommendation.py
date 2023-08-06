from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json

from telescope_sdk.common import UserFacingDataType


class RecommendationStatus(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SAVED = 'SAVED'
    PENDING = 'PENDING'


# TODO: iterate on these field values
class RecommendationRejectionReason(Enum):
    EXISTING_CUSTOMER = 'EXISTING_CUSTOMER'
    NOT_QUALIFIED = 'NOT_QUALIFIED'
    OTHER = 'OTHER'


@dataclass_json
@dataclass
class Recommendation(UserFacingDataType):
    campaign_id: str
    person_id: str
    status: RecommendationStatus
    relevance: float
    rejection_reason: Optional[RecommendationRejectionReason] = None
