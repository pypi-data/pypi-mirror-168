from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json

from telescope_sdk.common import TelescopeBaseType


class SequenceStepType(Enum):
    EMAIL = 'EMAIL'


@dataclass_json
@dataclass
class SequenceStep:
    id: str
    type: SequenceStepType
    seconds_from_previous_step: int
    subject: Optional[str] = None
    body: Optional[str] = None
    signature: Optional[str] = None


@dataclass_json
@dataclass
class Sequence(TelescopeBaseType):
    steps: list[SequenceStep]
