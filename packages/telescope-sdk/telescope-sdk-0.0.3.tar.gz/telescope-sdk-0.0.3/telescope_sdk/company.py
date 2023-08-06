from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json

from telescope_sdk.common import Location, IngestedDataType


class CompanyType(Enum):
    SOLE_PROPRIETORSHIP = "SOLE_PROPRIETORSHIP"
    PUBLIC_COMPANY = "PUBLIC_COMPANY"
    GOVERNMENT_AGENCY = "GOVERNMENT_AGENCY"
    PRIVATELY_HELD = "PRIVATELY_HELD"
    PARTNERSHIP = "PARTNERSHIP"
    SELF_EMPLOYED = "SELF-EMPLOYED"
    NONPROFIT = "NONPROFIT"
    EDUCATIONAL_INSTITUTION = "EDUCATIONAL_INSTITUTION"


@dataclass_json
@dataclass
class CompanySizeRange:
    lower: Optional[int]
    upper: Optional[int]


@dataclass_json
@dataclass
class Company(IngestedDataType):
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
    last_enriched_at: Optional[str] = None
