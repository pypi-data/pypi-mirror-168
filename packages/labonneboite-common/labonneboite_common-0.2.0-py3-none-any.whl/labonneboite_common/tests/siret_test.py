from unittest import TestCase
from labonneboite_common.siret import is_siret


class TestSiret(TestCase):
    def test_is_siret(self) -> None:
        self.assertTrue(is_siret("12345678901234"))
        self.assertFalse(is_siret("1234567890"))
        self.assertFalse(is_siret("AAAAAAAAAAAAAA"))
