from unittest import TestCase
from labonneboite_common.encoding import sanitize_string, strip_french_accents


class TestEncoding(TestCase):
    def test_sanitize_string(self) -> None:
        result = "é"

        self.assertIsNone(sanitize_string(None))
        self.assertEqual(sanitize_string(result), result)
        self.assertEqual(sanitize_string(result.encode("utf-8")), result)
        self.assertEqual(sanitize_string(b"\xc3\xa3\xa9"), "é")
        self.assertEqual(sanitize_string(b"\xc3\xa3\xa0"), "à")
        self.assertEqual(sanitize_string(result.encode("latin1")), result)
        self.assertRaises(Exception, sanitize_string, 1)

    def test_strip_french_accents(self) -> None:
        self.assertEqual(strip_french_accents("é"), "e")
