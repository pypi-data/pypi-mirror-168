"""Dataclass VerifiedCompany with verified values."""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, unique
from typing import List, Optional, Union


@unique
class CompanyEntityType(str, Enum):
    """Specific to cz and ARES declarations."""

    GOVERNING_BODY = "Statutární orgán"
    OTHER = "Jiný orgán"
    PARTNER = "Společnici"


@dataclass
class NaturalPerson():
    """Structure representing a natural person, are:TypFyzickaOsoba."""

    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]


@dataclass
class LegalPerson():
    """Structure representing a legal person, are:TypPravnickaOsoba."""

    vat_id: Optional[str]
    name: Optional[str]
    representative: Optional[NaturalPerson]


@dataclass
class Member:
    """Company members."""

    role: Optional[str]
    identity: Optional[Union[NaturalPerson, LegalPerson]]


@dataclass
class CompanyEntity:
    """Structure blocks of a company."""

    entity_type: Union[CompanyEntityType, str]
    name: Optional[str]
    members: Optional[List[Member]]


@dataclass
class VerifiedCompany:
    """Company name and address verified by VAT number."""

    company_name: str
    address: str
    street_and_num: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    district: Optional[str] = None
    country_code: Optional[str] = None
    company_entities: List[CompanyEntity] = field(default_factory=list)
    legal_form: Optional[int] = None
