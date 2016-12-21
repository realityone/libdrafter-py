from __future__ import unicode_literals

import json
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

    def test_version(self):
        self.assertIsNotNone(self.parser.drafter_version())
        self.assertIsNotNone(self.parser.drafter_version_string())

    def test_parse(self):
        source = b"""
# My API
## GET /message
+ Response 200 (text/plain)

        Hello World!
        """
        origin_result = {
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
        result = json.loads(self.parser.drafter_parse_blueprint_to(source, sourcemap=False, drafter_format=self.parser.JSON))
        self.assertEqual(origin_result, result)
