from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json

from telescope_sdk.utils import convert_country_str_to_iso_code


class Source(Enum):
    PDL = "PDL"
    REVENUEBASE = "REVENUEBASE"
    USER_UPLOAD = "USER_UPLOAD"
    UNKNOWN = "UNKNOWN"


@dataclass_json
@dataclass
class TelescopeBaseType:
    """
    Base class for all top-level Telescope entities.
    """
    id: str
    created_at: str
    updated_at: str


@dataclass_json
@dataclass
class IngestedDataType(TelescopeBaseType):
    """
    Base data type for entities which are ingested from external sources (e.g. PDL, RevenueBase, etc.)
    """
    source: Source
    version: int


@dataclass_json
@dataclass
class UserFacingDataType(TelescopeBaseType):
    """
    Base data type for entities which are created by or for users and which have a defined owner.
    """
    owner: str


@dataclass_json
@dataclass
class Location:
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None

    @staticmethod
    def from_pdl(pdl_input: dict[str, any]) -> Optional['Location']:
        country = pdl_input.get('country')
        return Location(
            line_1=pdl_input.get('street_address'),
            line_2=pdl_input.get('address_line_2'),
            country=convert_country_str_to_iso_code(country) if country else None,
            state=pdl_input.get('region'),
            postal_code=pdl_input.get('postal_code'),
            city=pdl_input.get('locality')
        )
