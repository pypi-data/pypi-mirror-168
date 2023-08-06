from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json

from telescope_sdk.common import TelescopeBaseType, Location


class CompanyType(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    SUBSIDIARY = "SUBSIDIARY"
    BRANCH = "BRANCH"
    JOINT_VENTURE = "JOINT_VENTURE"
    PARTNERSHIP = "PARTNERSHIP"
    GOVERNMENT_AGENCY = "GOVERNMENT_AGENCY"
    NON_PROFIT = "NON_PROFIT"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    OTHER = "OTHER"


@dataclass_json
@dataclass
class CompanySizeRange:
    lower: Optional[int]
    upper: Optional[int]


@dataclass_json
@dataclass
class Company(TelescopeBaseType):
    name: str
    linkedin_internal_id: str
    pdl_id: Optional[str] = None
    universal_name_id: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    domain_name: Optional[str] = None
    website: Optional[str] = None
    landing_page_content: Optional[str] = None
    logo_url: Optional[str] = None
    embeddings: Optional[list[float]] = None
    linkedin_url: Optional[str] = None
    industry: Optional[str] = None
    categories: Optional[list[str]] = None
    specialties: Optional[list[str]] = None
    company_type: Optional[CompanyType] = None
    company_size_range: Optional[CompanySizeRange] = None
    company_size_on_linkedin: Optional[int] = None
    founded_year: Optional[int] = None
    hq: Optional[Location] = None
    locations: Optional[list[Location]] = None
