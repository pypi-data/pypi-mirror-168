"""Load data from ARES at https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi."""
import logging
import xml.etree.ElementTree as ET
from datetime import date
from typing import Dict, List, Optional, Tuple, Union, cast

import pycountry
import requests

from .data import CompanyEntity, CompanyEntityType, LegalPerson, Member, NaturalPerson, VerifiedCompany
from .exceptions import (InvalidVatNumber, ServiceTemporarilyUnavailable, UnexpectedResponseFormat, VatNotFound,
                         VerifyVatException)
from .utils import strip_vat_id_number

SERVICE_URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi'
NS = {
      'are': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1',
      'dtt': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4',
      'udt': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/uvis_datatypes/v_1.0.1',
}
VR_NS = {
      'are': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer_vr/v_1.0.0',
      'dtt': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.6',
      'udt': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/uvis_datatypes/v_1.0.4',
}
VR_SERVICE_URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_vr.cgi'
VR_INDEX_POSITION = 1

LOGGER = logging.getLogger(__name__)


def get_xml_content(vat_ident_number: str, service_url: str = None) -> bytes:
    """Get xml content from ARES."""
    url = SERVICE_URL if service_url is None else service_url
    LOGGER.info(f'{url}?ico={vat_ident_number}')
    try:
        response = requests.get(url, params={'ico': vat_ident_number})
    except requests.exceptions.Timeout as err:
        raise ServiceTemporarilyUnavailable(err)
    except requests.exceptions.RequestException as err:
        source = err.response.content if err.response else b''
        raise VerifyVatException(err, source=source)
    if not response.ok:
        raise VerifyVatException(f'[{response.status_code}] {response.reason}', source=response.content)
    if LOGGER.level >= logging.DEBUG:
        LOGGER.debug(response.content.decode('UTF-8'))
    return response.content


def get_xml_doc(vat_ident_number: str, service_url: str = None) -> Tuple[ET.Element, bytes]:
    """Get xml document from ARES."""
    content = get_xml_content(vat_ident_number, service_url)
    try:
        return ET.fromstring(content), content
    except ET.ParseError as err:
        raise VerifyVatException(err, source=content)


def get_verified_company(
        company_name: str, address: ET.Element, legal_form: Optional[ET.Element], ns: Dict[str, str], source: bytes
        ) -> VerifiedCompany:
    """Complete address into dataclass VerifiedCompany."""
    data = VerifiedCompany(company_name=company_name, address='', country_code='CZ')
    data.city = get_text('dtt:Nazev_obce', address, ns, source)
    # Extension for Prague:
    if data.city == 'Praha':
        city_district = address.find('dtt:Nazev_mestske_casti', ns)
        if city_district is not None:
            data.city = str(city_district.text)  # Use city name with the number of the city district.

    # Include city name into the district due to compatibility with VIES.
    district = get_text('dtt:Nazev_casti_obce', address, ns, source)
    if data.city in district:
        data.district = district
    else:
        data.district = f'{data.city} - {district}'  # District does not include city name.

    query = 'dtt:PSC'
    node = address.find(query, ns)
    if node is None:
        raise UnexpectedResponseFormat(query, source=source)
    data.postal_code = str(node.text)

    query = 'dtt:Nazev_ulice'
    node = address.find(query, ns)
    if node is None:
        street_name = data.city
    else:
        street_name = str(node.text)

    house_number = get_text('dtt:Cislo_domovni', address, ns, source)

    orientation_number = None
    query = 'dtt:Cislo_orientacni'
    node = address.find(query, ns)
    if node is not None:
        orientation_number = str(node.text)

    street_and_num = f'{street_name} {house_number}'
    if orientation_number:
        street_and_num += f'/{orientation_number}'
    data.street_and_num = street_and_num

    country_code: str = get_text('dtt:Kod_statu', address, ns, source)
    country: Optional[pycountry.db.Country] = pycountry.countries.get(numeric=country_code)
    if country is not None:
        data.country_code = country.alpha_2
    data.address = f'{data.street_and_num}\n{data.postal_code} {data.city}'

    if legal_form is not None and legal_form.text:
        data.legal_form = int(legal_form.text)
    return data


def get_from_cz_ares(
    vat_ident_number: str, service_url: str = None, ns: Dict[str, str] = None, parse_entities: bool = False
) -> VerifiedCompany:
    """Verify VAT identifier number by ARES. Return company name and address."""
    vat_ident_number = strip_vat_id_number(vat_ident_number)
    if vat_ident_number == '':
        raise InvalidVatNumber('Invalid number format.')
    if len(vat_ident_number) > 8:
        raise InvalidVatNumber('The number cannot be more than 8 digits long.')
    if ns is None:
        ns = NS
    root, source = get_xml_doc(vat_ident_number, service_url)

    check_error_code(root, ns, source)  # Raise ServiceTemporarilyUnavailable if dtt:Error_kod.

    query = './/are:Pocet_zaznamu'
    node = root.find(query, ns)
    if node is None:
        raise UnexpectedResponseFormat(query, source=source)
    if int(str(node.text)) != 1:
        raise VatNotFound(source=source)

    query = './/are:Adresa_ARES'
    address = root.find(query, ns)
    if address is None:
        raise UnexpectedResponseFormat(query, source=source)

    legal_form = root.find(".//are:Pravni_forma/dtt:Kod_PF", ns)
    company_name = get_text('.//are:Obchodni_firma', root, ns, source)
    data = get_verified_company(company_name, address, legal_form, ns, source)

    extra_indexes = root.find(".//are:Odpoved/are:Zaznam/are:Priznaky_subjektu", ns)
    if parse_entities and extra_indexes is not None and cast(str, extra_indexes.text)[VR_INDEX_POSITION] == "A":
        data.company_entities = parse_entities_vr(vat_ident_number)

    return data


COMPANY_ENTITY_SELECTORS = {
    CompanyEntityType.GOVERNING_BODY: "are:StatutarniOrgan",
    CompanyEntityType.OTHER: "are:JinyOrgan",
    CompanyEntityType.PARTNER: "are:Spolecnici",
}


def parse_natural_person(person_elm: ET.Element) -> NaturalPerson:
    """Parse are:TypFyzickaOsoba."""
    fname_elm = person_elm.find("are:jmeno", VR_NS)
    lname_elm = person_elm.find("are:prijmeni", VR_NS)
    date_of_birth_elm = person_elm.find("are:datumNarozeni", VR_NS)
    return NaturalPerson(
        fname_elm.text.title() if fname_elm is not None and fname_elm.text else None,
        lname_elm.text.title() if lname_elm is not None and lname_elm.text else None,
        date.fromisoformat(date_of_birth_elm.text) if date_of_birth_elm is not None and date_of_birth_elm.text else None
    )


def parse_legal_person(person_elm: ET.Element) -> LegalPerson:
    """Parse are:TypPravnickaOsoba."""
    representative_elm = person_elm.find("are:Zastoupeni/.are:fosoba", VR_NS)
    representative = parse_natural_person(representative_elm) if representative_elm is not None else None
    vat_num_elm = person_elm.find("are:Ico/dtt:value", VR_NS)
    name_elm = person_elm.find("are:ObchodniFirma/dtt:value", VR_NS)
    return LegalPerson(
        vat_num_elm.text if vat_num_elm is not None else None,
        name_elm.text if name_elm is not None else None,
        representative,
    )


def _check_listing(listing: ET.Element) -> bool:
    """Heuristic checks if retrieved listing is a valid corporation."""
    if listing.find("are:ZakladniUdaje/are:Ico", VR_NS) is None:
        return False

    if (
        removed := listing.find("are:ZakladniUdaje/are:DatumVymazu", VR_NS)
    ) is not None and removed.text:
        if date.fromisoformat(removed.text) < date.today():
            return False

    return True


def parse_entities_vr(vat_ident_number: str) -> List[CompanyEntity]:
    """Parse entities are:TypJinyOrganDatum, are:TypStatutarniOrganDatum", are:TypSpolecnikDatum."""
    root, source = get_xml_doc(vat_ident_number, VR_SERVICE_URL)
    check_error_code(root, VR_NS, source)
    listings = [listing for listing in root.findall(".//are:Vypis_VR", VR_NS) if _check_listing(listing)]
    extracted = []
    for listing in listings:
        entities = {
            entity_type: listing.findall(selector, VR_NS) for entity_type, selector in COMPANY_ENTITY_SELECTORS.items()
        }
        for entity_type, entities_elements in entities.items():
            for entity_elm in entities_elements:
                members = []
                for member_elm in entity_elm.findall("are:Clen", VR_NS):
                    if (
                        expiration := member_elm.find("are:clenstvi/are:zanikClenstvi", VR_NS)
                    ) is not None and expiration.text:
                        if date.fromisoformat(expiration.text) < date.today():
                            # skip this member
                            continue
                    identity: Optional[Union[LegalPerson, NaturalPerson]] = None
                    role_elm = member_elm.find("are:funkce/are:nazev", VR_NS)
                    if (person_elm := member_elm.find("are:fosoba", VR_NS)) is not None:
                        identity = parse_natural_person(person_elm)
                    elif (person_elm := member_elm.find("are:posoba", VR_NS)) is not None:
                        identity = parse_legal_person(person_elm)
                    members.append(
                        Member(role_elm.text.capitalize() if role_elm is not None and role_elm.text else None, identity)
                    )
                for member_elm in entity_elm.findall("are:Spolecnik", VR_NS):
                    identity = None
                    if (person_elm := member_elm.find("are:fosoba", VR_NS)) is not None:
                        identity = parse_natural_person(person_elm)
                    elif (person_elm := member_elm.find("are:posoba", VR_NS)) is not None:
                        identity = parse_legal_person(person_elm)
                    members.append(Member("Společník", identity))
                entity_name = entity_elm.find("are:Nazev", VR_NS)
                extracted.append(
                    CompanyEntity(entity_type, entity_name.text if entity_name is not None else None, members)
                )
    return extracted


def check_error_code(root: ET.Element, ns: Dict[str, str], source: bytes) -> None:
    """Check if message has an Error code."""
    query = './/dtt:Error_kod'
    node = root.find(query, ns)
    if node is not None:
        message = f'Error code: {node.text}'
        query = './/dtt:Error_text'
        node = root.find(query, ns)
        if node is not None:
            message += f'; {node.text}'
        raise ServiceTemporarilyUnavailable(message, source=source)


def get_text(query: str, root: ET.Element, ns: Dict[str, str], source: bytes) -> str:
    """Get text from node.text selected by query."""
    node = root.find(query, ns)
    if node is None:
        raise UnexpectedResponseFormat(query, source=source)
    return str(node.text)
