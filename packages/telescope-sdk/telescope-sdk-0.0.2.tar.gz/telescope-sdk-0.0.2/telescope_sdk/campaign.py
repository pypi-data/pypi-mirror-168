from dataclasses import dataclass

from dataclasses_json import dataclass_json
from telescope_sdk.common import TelescopeBaseType


class CampaignStatus:
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    ERROR = 'ERROR'


@dataclass_json
@dataclass
class Campaign(TelescopeBaseType):
    name: str
    owner: str
    status: CampaignStatus
    campaign_sequence_id: str
    replenish: bool
