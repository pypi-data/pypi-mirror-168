from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json
from telescope_sdk.common import UserFacingDataType


class ProspectInteractionEventType(Enum):
    PROSPECT_REPLIED_POSITIVE = 'PROSPECT_REPLIED_POSITIVE'
    PROSPECT_REPLIED_NEGATIVE = 'PROSPECT_REPLIED_NEGATIVE'
    PROSPECT_REPLIED_UNKNOWN_SENTIMENT = 'PROSPECT_REPLIED_UNKNOWN_SENTIMENT'


@dataclass_json
@dataclass
class ProspectInteractionEvent(UserFacingDataType):
    owner: str
    prospect_interaction_event_campaign_id: str
    prospect_id: str
    type: ProspectInteractionEventType
    text_reply: Optional[str] = None
