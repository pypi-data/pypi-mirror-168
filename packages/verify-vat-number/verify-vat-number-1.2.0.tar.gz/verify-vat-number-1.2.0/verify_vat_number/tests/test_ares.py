import os
import xml.etree.ElementTree as ET
from datetime import date
from unittest import TestCase

import responses
from freezegun import freeze_time
from requests.exceptions import RequestException, Timeout

from verify_vat_number.ares import (NS, SERVICE_URL, VR_SERVICE_URL, check_error_code, get_from_cz_ares, get_text,
                                    get_xml_content, get_xml_doc)
from verify_vat_number.data import CompanyEntity, CompanyEntityType, LegalPerson, Member, NaturalPerson, VerifiedCompany
from verify_vat_number.exceptions import (InvalidVatNumber, ServiceTemporarilyUnavailable, UnexpectedResponseFormat,
                                          VatNotFound, VerifyVatException)
from verify_vat_number.tests.utils import get_file_bytes

DATA_DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


class TestAres(TestCase):

    logger_name = 'verify_vat_number.ares'
    logging_info = 'INFO:verify_vat_number.ares:https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico=67985726'

    def test_get_xml_content_request_exception(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=RequestException())
                with self.assertRaises(VerifyVatException) as context:
                    get_xml_content('67985726')
        self.assertEqual(context.exception.source, '')
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_content_timeout(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=Timeout())
                with self.assertRaises(ServiceTemporarilyUnavailable) as context:
                    get_xml_content('67985726')
        self.assertIsNone(context.exception.source)
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_content_response_is_not_ok(self):
        with self.assertLogs(self.logger_name, level='INFO') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', status=404, body="Page not found.")
                with self.assertRaises(VerifyVatException) as context:
                    get_xml_content('67985726')
        self.assertEqual(context.exception.source, 'Page not found.')
        self.assertEqual(logs.output, [self.logging_info])

    def test_get_xml_content(self):
        with self.assertLogs(self.logger_name, level='DEBUG') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(
                    responses.GET,
                    f'{SERVICE_URL}?ico=67985726',
                    body=get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_std_response_67985726.xml'))
                )
                content = get_xml_content('67985726')
        data = get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_std_response_67985726.xml'))
        self.assertEqual(content, data)
        self.assertEqual(logs.output, [self.logging_info, f'DEBUG:verify_vat_number.ares:{data.decode("UTF8")}'])

    def test_get_xml_content_param_url(self):
        with self.assertLogs(self.logger_name, level='DEBUG') as logs:
            with responses.RequestsMock() as rsps:
                rsps.add(
                    responses.GET,
                    f'{VR_SERVICE_URL}?ico=67985726',
                    body=get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_vr_response_67985726.xml'))
                )
                content = get_xml_content('67985726', VR_SERVICE_URL)
        data = get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_vr_response_67985726.xml'))
        self.assertEqual(content, data)
        self.assertEqual(
            logs.output,
            [
                f"INFO:verify_vat_number.ares:{VR_SERVICE_URL}?ico=67985726",
                f'DEBUG:verify_vat_number.ares:{data.decode("UTF8")}',
            ]
        )

    def test_get_xml_doc_invalid_xml(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body="<foo")
            with self.assertRaises(VerifyVatException) as context:
                get_xml_doc('67985726')
        self.assertEqual(context.exception.source, '<foo')

    def test_get_xml_doc(self):
        body = get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_std_response_67985726.xml'))
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=body)
            root, source = get_xml_doc('67985726')
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(source, body)

    def test_check_error_code_no_error(self):
        content = b"""<?xml version="1.0" encoding="UTF-8"?><Error></Error>"""
        root = ET.fromstring(content)
        check_error_code(root, NS, content)
        self.assertIsInstance(root, ET.Element)

    def test_check_error_code_only_number(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Error
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
                >
                <dtt:Error_kod>7</dtt:Error_kod>
            </are:Error>"""
        root = ET.fromstring(content)
        with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'Error code: 7') as context:
            check_error_code(root, NS, content.encode('utf-8'))
        self.assertEqual(context.exception.source, content)

    def test_check_error_code_number_and_message(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Error
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
                >
                <dtt:Error_kod>7</dtt:Error_kod>
                <dtt:Error_text>chyba logických vazeb</dtt:Error_text>
            </are:Error>"""
        root = ET.fromstring(content)
        with self.assertRaisesRegex(ServiceTemporarilyUnavailable, 'Error code: 7; chyba logických vazeb') as context:
            check_error_code(root, NS, content.encode('utf-8'))
        self.assertEqual(context.exception.source, content)

    def test_get_text_unexpected_format(self):
        content = """<?xml version="1.0" encoding="UTF-8"?><Error></Error>"""
        root = ET.fromstring(content)
        with self.assertRaisesRegex(UnexpectedResponseFormat, 'dtt:foo') as context:
            get_text('dtt:foo', root, NS, content.encode('utf-8'))
        self.assertEqual(context.exception.source, content)

    def test_get_text(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <Error xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <dtt:foo>Hello world!</dtt:foo>
            </Error>"""
        root = ET.fromstring(content)
        text = get_text('dtt:foo', root, NS, content.encode('utf-8'))
        self.assertEqual(text, 'Hello world!')

    def test_get_from_cz_ares(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f'{SERVICE_URL}?ico=67985726',
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_std_response_67985726.xml'))
            )
            response = get_from_cz_ares('67985726', parse_entities=False)
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name='CZ.NIC, z.s.p.o.',
                address='Milešovská 1136/5\n13000 Praha 3',
                street_and_num='Milešovská 1136/5',
                city='Praha 3',
                postal_code='13000',
                district='Praha 3 - Vinohrady',
                country_code='CZ',
                company_entities=[],
                legal_form=751
            )
        )

    def test_get_from_cz_ares_parse_entities(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_67985726.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_vr_response_67985726.xml")),
            )
            response = get_from_cz_ares("67985726", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán - Představenstvo",
                [
                    Member("Místopředseda představenstva", NaturalPerson("Marek", "Antoš", date(1979, 12, 18))),
                    Member("Člen představenstva", NaturalPerson("Tomáš", "Košňar", date(1965, 6, 21))),
                    Member("Člen představenstva", NaturalPerson("Martin", "Kukačka", date(1980, 10, 30))),
                    Member("Členka představenstva", NaturalPerson("Ilona", "Filípková", date(1972, 7, 8))),
                    Member("Předseda představenstva", NaturalPerson("Karel", "Taft", date(1971, 5, 26))),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.OTHER,
                "Kontrolní orgán - Dozorčí rada",
                [
                    Member("Předseda dozorčí rady", NaturalPerson("Jan", "Redl", date(1972, 3, 18))),
                    Member("Člen dozorčí rady", NaturalPerson("Vlastimil", "Pečínka", date(1975, 9, 12))),
                    Member("Člen dozorčí rady", NaturalPerson("Jan", "Gruntorád", date(1951, 10, 19))),
                ],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="CZ.NIC, z.s.p.o.",
                address="Milešovská 1136/5\n13000 Praha 3",
                street_and_num="Milešovská 1136/5",
                city="Praha 3",
                postal_code="13000",
                district="Praha 3 - Vinohrady",
                country_code="CZ",
                company_entities=entities,
                legal_form=751
            ),
        )

    def test_get_from_cz_ares_parse_entities_vr_error(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_67985726.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_vr_response_error_not_found.xml")),
            )
            with self.assertRaisesRegex(ServiceTemporarilyUnavailable, "Error code: 1"):
                get_from_cz_ares("67985726", parse_entities=True)

    def test_get_from_cz_ares_legal_entity_member(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=14347890",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_14347890.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=14347890",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_vr_response_14347890_posoba.xml")),
            )
            response = get_from_cz_ares("14347890", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán",
                [
                    Member(
                        "Jednatel",
                        LegalPerson(
                            "01407511",
                            "Profispolečnosti servis s.r.o.",
                            NaturalPerson("Michal", "Koman", date(1985, 5, 31))
                        ),
                    ),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.PARTNER,
                "Společníci",
                [Member("Společník", LegalPerson("24248525", "Profispolečnosti Praha s.r.o.", None))],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="Rumney Corp s.r.o.",
                address="Primátorská 296/38\n18000 Praha 8",
                street_and_num="Primátorská 296/38",
                city="Praha 8",
                postal_code="18000",
                district="Praha 8 - Libeň",
                country_code="CZ",
                company_entities=entities,
                legal_form=112
            ),
        )

    def test_get_from_cz_ares_expired_member(self):
        with responses.RequestsMock() as rsps, freeze_time("2022-09-6 12:00:00"):
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_67985726.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_vr_response_67985726_expired_member.xml")),
            )
            response = get_from_cz_ares("67985726", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán - Představenstvo",
                [Member("Člen představenstva", NaturalPerson("Tomáš", "Košňar", date(1965, 6, 21)))],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="CZ.NIC, z.s.p.o.",
                address="Milešovská 1136/5\n13000 Praha 3",
                street_and_num="Milešovská 1136/5",
                city="Praha 3",
                postal_code="13000",
                district="Praha 3 - Vinohrady",
                country_code="CZ",
                company_entities=entities,
                legal_form=751
            ),
        )

    def test_get_from_cz_ares_still_valid_member(self):
        with responses.RequestsMock() as rsps, freeze_time("2020-09-6 12:00:00"):
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_67985726.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_vr_response_67985726_expired_member.xml")),
            )
            response = get_from_cz_ares("67985726", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán - Představenstvo",
                [
                    Member("Člen představenstva", NaturalPerson("Tomáš", "Košňar", date(1965, 6, 21))),
                    Member("Člen představenstva", NaturalPerson("Martin", "Kukačka", date(1980, 10, 30))),
                ],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="CZ.NIC, z.s.p.o.",
                address="Milešovská 1136/5\n13000 Praha 3",
                street_and_num="Milešovská 1136/5",
                city="Praha 3",
                postal_code="13000",
                district="Praha 3 - Vinohrady",
                country_code="CZ",
                company_entities=entities,
                legal_form=751
            ),
        )

    def test_get_from_cz_ares_gov_boty_member_without_identity(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=67985726",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_67985726.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=67985726",
                body=get_file_bytes(
                    os.path.join(DATA_DIR_PATH, "ares_vr_response_67985726_gov_body_missing_identity.xml")),
            )
            response = get_from_cz_ares("67985726", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán - Představenstvo",
                [
                    Member("Člen představenstva", NaturalPerson("Tomáš", "Košňar", date(1965, 6, 21))),
                    Member("Člen představenstva", None),
                ],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="CZ.NIC, z.s.p.o.",
                address="Milešovská 1136/5\n13000 Praha 3",
                street_and_num="Milešovská 1136/5",
                city="Praha 3",
                postal_code="13000",
                district="Praha 3 - Vinohrady",
                country_code="CZ",
                company_entities=entities,
                legal_form=751
            ),
        )

    def test_get_from_cz_ares_partner_member_without_identity(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=14347890",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_14347890.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=14347890",
                body=get_file_bytes(
                    os.path.join(DATA_DIR_PATH, "ares_vr_response_14347890_partner_missing_identity.xml")),
            )
            response = get_from_cz_ares("14347890", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán",
                [
                    Member(
                        "Jednatel",
                        LegalPerson(
                            "01407511",
                            "Profispolečnosti servis s.r.o.",
                            NaturalPerson("Michal", "Koman", date(1985, 5, 31))
                        ),
                    ),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.PARTNER,
                "Společníci",
                [
                    Member("Společník", LegalPerson("24248525", "Profispolečnosti Praha s.r.o.", None)),
                    Member("Společník", None)
                ],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="Rumney Corp s.r.o.",
                address="Primátorská 296/38\n18000 Praha 8",
                street_and_num="Primátorská 296/38",
                city="Praha 8",
                postal_code="18000",
                district="Praha 8 - Libeň",
                country_code="CZ",
                company_entities=entities,
                legal_form=112
            ),
        )

    def test_get_from_cz_ares_partner_natural_person(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=14347890",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_14347890.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=14347890",
                body=get_file_bytes(
                    os.path.join(DATA_DIR_PATH, "ares_vr_response_14347890_partner_natural_person.xml")),
            )
            response = get_from_cz_ares("14347890", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán",
                [
                    Member(
                        "Jednatel",
                        LegalPerson(
                            "01407511",
                            "Profispolečnosti servis s.r.o.",
                            NaturalPerson("Michal", "Koman", date(1985, 5, 31))
                        ),
                    ),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.PARTNER,
                "Společníci",
                [Member("Společník", NaturalPerson("Michal", "Koman", date(1985, 5, 31)))],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="Rumney Corp s.r.o.",
                address="Primátorská 296/38\n18000 Praha 8",
                street_and_num="Primátorská 296/38",
                city="Praha 8",
                postal_code="18000",
                district="Praha 8 - Libeň",
                country_code="CZ",
                company_entities=entities,
                legal_form=112
            ),
        )

    def test_get_from_cz_ares_parse_entities_not_in_vr(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=18380824",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_18380824_no_vr.xml")),
            )
            response = get_from_cz_ares("18380824", parse_entities=True)
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="Gymnázium a Střední odborná škola, Podbořany, příspěvková organizace",
                address="Kpt. Jaroše 862\n44101 Podbořany",
                street_and_num="Kpt. Jaroše 862",
                city="Podbořany",
                postal_code="44101",
                district="Podbořany",
                country_code="CZ",
                company_entities=[],
                legal_form=331
            ),
        )

    def test_get_from_cz_multiple_listings_missing_vat(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=18380824",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_22795243.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=18380824",
                body=get_file_bytes(
                    os.path.join(DATA_DIR_PATH, "ares_vr_response_22795243_multiple_listings_no_vat.xml")),
            )
            response = get_from_cz_ares("18380824", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán",
                [
                    Member(
                        "Jednatel",
                        NaturalPerson("Jiří", "Richtr", date(1972, 11, 11))
                    ),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.OTHER,
                "Dozorčí rada",
                [
                    Member("Předseda dozorčí rady", NaturalPerson("Lukáš", "Trakal", date(1977, 2, 14))),
                    Member("Člen dozorčí rady", NaturalPerson("Jan", "Štědra", date(1986, 10, 21))),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.PARTNER,
                "Společníci",
                [
                    Member("Společník", NaturalPerson("Jiří", "Richtr", date(1972, 11, 11))),
                    Member("Společník", NaturalPerson("Přemysl", "Tišer", date(1979, 4, 29))),
                    Member("Společník", NaturalPerson("Lukáš", "Trakal", date(1977, 2, 14))),
                ],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="BIOSIDE s.r.o.",
                address="Rumjancevova 65/20a\n46001 Liberec",
                street_and_num="Rumjancevova 65/20a",
                city="Liberec",
                postal_code="46001",
                district="Liberec I-Staré Město",
                country_code="CZ",
                company_entities=entities,
                legal_form=112
            ),
        )

    def test_get_from_cz_listing_expired(self):
        with responses.RequestsMock() as rsps, freeze_time("2022-03-1 12:00:00"):
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=18380824",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_22795243.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=18380824",
                body=get_file_bytes(
                    os.path.join(DATA_DIR_PATH, "ares_vr_response_22795243_listing_expired.xml")),
            )
            response = get_from_cz_ares("18380824", parse_entities=True)
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="BIOSIDE s.r.o.",
                address="Rumjancevova 65/20a\n46001 Liberec",
                street_and_num="Rumjancevova 65/20a",
                city="Liberec",
                postal_code="46001",
                district="Liberec I-Staré Město",
                country_code="CZ",
                company_entities=[],
                legal_form=112
            ),
        )

    def test_get_from_cz_listing_not_expired_yet(self):
        with responses.RequestsMock() as rsps, freeze_time("2022-01-1 12:00:00"):
            rsps.add(
                responses.GET,
                f"{SERVICE_URL}?ico=18380824",
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, "ares_std_response_22795243.xml")),
            )
            rsps.add(
                responses.GET,
                f"{VR_SERVICE_URL}?ico=18380824",
                body=get_file_bytes(
                    os.path.join(DATA_DIR_PATH, "ares_vr_response_22795243_listing_expired.xml")),
            )
            response = get_from_cz_ares("18380824", parse_entities=True)
        entities = [
            CompanyEntity(
                CompanyEntityType.GOVERNING_BODY,
                "Statutární orgán",
                [
                    Member(
                        "Jednatel",
                        NaturalPerson("Jiří", "Richtr", date(1972, 11, 11))
                    ),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.OTHER,
                "Dozorčí rada",
                [
                    Member("Předseda dozorčí rady", NaturalPerson("Lukáš", "Trakal", date(1977, 2, 14))),
                    Member("Člen dozorčí rady", NaturalPerson("Jan", "Štědra", date(1986, 10, 21))),
                ],
            ),
            CompanyEntity(
                CompanyEntityType.PARTNER,
                "Společníci",
                [
                    Member("Společník", NaturalPerson("Jiří", "Richtr", date(1972, 11, 11))),
                    Member("Společník", NaturalPerson("Přemysl", "Tišer", date(1979, 4, 29))),
                    Member("Společník", NaturalPerson("Lukáš", "Trakal", date(1977, 2, 14))),
                ],
            ),
        ]
        self.assertEqual(
            response,
            VerifiedCompany(
                company_name="BIOSIDE s.r.o.",
                address="Rumjancevova 65/20a\n46001 Liberec",
                street_and_num="Rumjancevova 65/20a",
                city="Liberec",
                postal_code="46001",
                district="Liberec I-Staré Město",
                country_code="CZ",
                company_entities=entities,
                legal_form=112
            ),
        )

    def test_get_from_cz_ares_custom_namespace(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f'{SERVICE_URL}?ico=67985726',
                body=get_file_bytes(os.path.join(DATA_DIR_PATH, 'ares_std_response_67985726.xml'))
            )
            response = get_from_cz_ares('67985726', ns=NS)
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136/5\n13000 Praha 3',
            street_and_num='Milešovská 1136/5',
            city='Praha 3',
            postal_code='13000',
            district='Praha 3 - Vinohrady',
            country_code='CZ',
            company_entities=[],
            legal_form=751
        ))

    def test_get_from_cz_ares_empty_number(self):
        with self.assertRaisesRegex(InvalidVatNumber, 'Invalid number format.'):
            get_from_cz_ares('!')

    def test_get_from_cz_ares_too_long_number(self):
        with self.assertRaisesRegex(InvalidVatNumber, 'The number cannot be more than 8 digits long.'):
            get_from_cz_ares('123456789')

    def test_get_from_cz_ares_error_code(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Error
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4"
                >
                <dtt:Error_kod>7</dtt:Error_kod>
                <dtt:Error_text>chyba logických vazeb</dtt:Error_text>
            </are:Error>"""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaises(ServiceTemporarilyUnavailable) as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_pocet_zaznamu_missing(self):
        content = """<foo></foo>"""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaisesRegex(UnexpectedResponseFormat, './/are:Pocet_zaznamu') as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_pocet_zaznamu_is_not_one(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1">
                <are:Pocet_zaznamu>0</are:Pocet_zaznamu>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaises(VatNotFound) as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_adresa_ared_missing(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaisesRegex(UnexpectedResponseFormat, './/are:Adresa_ARES') as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_nazev_mestske_casti(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_mestske_casti>Praha 3</dtt:Nazev_mestske_casti>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Nazev_ulice>Milešovská</dtt:Nazev_ulice>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136\n13000 Praha 3',
            street_and_num='Milešovská 1136',
            city='Praha 3',
            postal_code='13000',
            district='Praha 3 - Vinohrady',
            country_code='CZ',
            company_entities=[]
        ))

    def test_get_from_cz_ares_nazev_obce(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Nazev_ulice>Milešovská</dtt:Nazev_ulice>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Milešovská 1136\n13000 Praha',
            street_and_num='Milešovská 1136',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ',
            company_entities=[]
        ))

    def test_get_from_cz_ares_psc(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            with self.assertRaisesRegex(UnexpectedResponseFormat, 'dtt:PSC') as context:
                get_from_cz_ares('67985726')
        self.assertEqual(context.exception.source, content)

    def test_get_from_cz_ares_nazev_ulice(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Praha 1136\n13000 Praha',
            street_and_num='Praha 1136',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ',
            company_entities=[]
        ))

    def test_get_from_cz_ares_cislo_orientacni(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Cislo_orientacni>5</dtt:Cislo_orientacni>
                    <dtt:Kod_statu>203</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Praha 1136/5\n13000 Praha',
            street_and_num='Praha 1136/5',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ',
            company_entities=[]
        ))

    def test_get_from_cz_ares_unknown_country(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
            <are:Odpoved
                xmlns:are="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1"
                xmlns:dtt="http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4">
                <are:Pocet_zaznamu>1</are:Pocet_zaznamu>
                <are:Obchodni_firma>CZ.NIC, z.s.p.o.</are:Obchodni_firma>
                <are:Adresa_ARES>
                    <dtt:Nazev_obce>Praha</dtt:Nazev_obce>
                    <dtt:Nazev_casti_obce>Vinohrady</dtt:Nazev_casti_obce>
                    <dtt:PSC>13000</dtt:PSC>
                    <dtt:Cislo_domovni>1136</dtt:Cislo_domovni>
                    <dtt:Kod_statu>0</dtt:Kod_statu>
                </are:Adresa_ARES>
            </are:Odpoved>
        """
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, f'{SERVICE_URL}?ico=67985726', body=content.encode('utf8'))
            response = get_from_cz_ares('67985726')
        self.assertEqual(response, VerifiedCompany(
            company_name='CZ.NIC, z.s.p.o.',
            address='Praha 1136\n13000 Praha',
            street_and_num='Praha 1136',
            city='Praha',
            postal_code='13000',
            district='Praha - Vinohrady',
            country_code='CZ',
            company_entities=[]
        ))
