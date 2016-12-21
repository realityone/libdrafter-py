from __future__ import unicode_literals

import ctypes


class ParserError(Exception):
    pass


class Parser(object):
    @staticmethod
    def find_library():
        from ctypes.util import find_library
        libdrafter_path = find_library('drafter')
        if not libdrafter_path:
            raise ParserError('libdrafter(Drafter) not found')
        return libdrafter_path

    def __init__(self, libdrafter_path=None):
        self.libdrafter_path = libdrafter_path or self.find_library()
        self.libdrafter = ctypes.CDLL(libdrafter_path)
