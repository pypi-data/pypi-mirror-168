from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json

from telescope_sdk.common import TelescopeBaseType


class RecommendationStatus(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SAVED = 'SAVED'
    PENDING = 'PENDING'


class RecommendationRejectionReason(Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    SAVED = 'SAVED'
    PENDING = 'PENDING'


@dataclass_json
@dataclass
class Recommendation(TelescopeBaseType):
    campaign_id: str
    person_id: str
    status: RecommendationStatus
    relevance: float
    rejection_reason: Optional['RecommendationRejectionReason'] = None
