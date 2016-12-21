from __future__ import unicode_literals

import json
import unittest

from libdrafter import parser


class TestEncrypt(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser()
        self.source = b"""
# My API
## GET /message
+ Response 200 (text/plain)

        Hello World!
        """
        self.origin_json_result = {
            "element": "parseResult",
            "content": [
                {
                    "element": "category",
                    "meta": {
                        "classes": [
                            "api"
                        ],
                        "title": "My API"
                    },
                    "content": [
                        {
                            "element": "category",
                            "meta": {
                                "classes": [
                                    "resourceGroup"
                                ],
                                "title": ""
                            },
                            "content": [
                                {
                                    "element": "resource",
                                    "meta": {
                                        "title": ""
                                    },
                                    "attributes": {
                                        "href": "/message"
                                    },
                                    "content": [
                                        {
                                            "element": "transition",
                                            "meta": {
                                                "title": ""
                                            },
                                            "content": [
                                                {
                                                    "element": "httpTransaction",
                                                    "content": [
                                                        {
                                                            "element": "httpRequest",
                                                            "attributes": {
                                                                "method": "GET"
                                                            },
                                                            "content": []
                                                        },
                                                        {
                                                            "element": "httpResponse",
                                                            "attributes": {
                                                                "statusCode": "200",
                                                                "headers": {
                                                                    "element": "httpHeaders",
                                                                    "content": [
                                                                        {
                                                                            "element": "member",
                                                                            "content": {
                                                                                "key": {
                                                                                    "element": "string",
                                                                                    "content": "Content-Type"
                                                                                },
                                                                                "value": {
                                                                                    "element": "string",
                                                                                    "content": "text/plain"
                                                                                }
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            },
                                                            "content": [
                                                                {
                                                                    "element": "asset",
                                                                    "meta": {
                                                                        "classes": [
                                                                            "messageBody"
                                                                        ]
                                                                    },
                                                                    "attributes": {
                                                                        "contentType": "text/plain"
                                                                    },
                                                                    "content": "Hello World!\n"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

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

    def test_version(self):
        self.assertIsNotNone(self.parser.drafter_version())
        self.assertIsNotNone(self.parser.drafter_version_string())

    def test_drafter_parse_blueprint_to(self):
        result = json.loads(self.parser.drafter_parse_blueprint_to(self.source, sourcemap=False, drafter_format=self.parser.JSON))
        self.assertEqual(self.origin_json_result, result)

    def test_parse_and_blueprint(self):
        drafter_result = self.parser.drafter_parse_blueprint(self.source)
        result = json.loads(self.parser.drafter_serialize(drafter_result, sourcemap=False, drafter_format=self.parser.JSON))
        self.assertEqual(self.origin_json_result, result)
        self.parser.drafter_free_result(drafter_result)

    def test_drafter_check_blueprint(self):
        drafter_result = self.parser.drafter_check_blueprint(self.source)
        self.assertNotEqual(self.parser.NULL, drafter_result)
