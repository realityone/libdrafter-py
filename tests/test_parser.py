import unittest

from libdrafter import parser


class TestEncrypt(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser()

    def test_load(self):
        self.assertTrue(self.parser.libdrafter_path)
        self.assertTrue(self.parser.libdrafter)
