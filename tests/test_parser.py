import unittest

from libdrafter import parser


class TestEncrypt(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser()

    def test_load(self):
        methods = [
            'drafter_parse_blueprint_to',
            'drafter_parse_blueprint',
            'drafter_serialize',
            'drafter_free_result',
            'drafter_check_blueprint',
            'drafter_version',
            'drafter_version_string'
        ]

        self.assertTrue(self.parser.libdrafter_path)
        self.assertTrue(self.parser.libdrafter)
        for m in methods:
            self.assertIsNotNone(getattr(self.parser.libdrafter, m))
