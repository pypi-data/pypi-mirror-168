from labonneboite_common.chunk import chunks

from unittest import TestCase


class TestChunks(TestCase):
    def test_chunks(self) -> None:
        result = chunks([1, 2], 1)
        self.assertEqual(list(result), [[1], [2]])
