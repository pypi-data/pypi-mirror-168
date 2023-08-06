from labonneboite_common.departements import DEPARTEMENTS
from unittest import TestCase


class TestDepartements(TestCase):
    def test_deps(self) -> None:
        self.assertEqual(len(DEPARTEMENTS), 96)
        self.assertEqual(DEPARTEMENTS[0], "01")
        self.assertEqual(DEPARTEMENTS[-1], "97")
        self.assertNotIn("96", DEPARTEMENTS)
