from __future__ import unicode_literals

import cffi


class ParserError(Exception):
    pass


class Parser(cffi.FFI):
    @staticmethod
    def find_library():
        from ctypes.util import find_library
        libdrafter_path = find_library('drafter')
        if not libdrafter_path:
            raise ParserError('libdrafter(Drafter) not found')
        return libdrafter_path

    def __init__(self, libdrafter_path=None, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)

        self.cdef(
            """
typedef struct drafter_result drafter_result;

typedef enum {
    DRAFTER_SERIALIZE_YAML = 0,
    DRAFTER_SERIALIZE_JSON
} drafter_format;

typedef struct {
    bool sourcemap;
    drafter_format format;
} drafter_options;

int drafter_parse_blueprint_to(const char* source,
                               char** out,
                               const drafter_options options);
int drafter_parse_blueprint(const char* source, drafter_result** out);
char* drafter_serialize(drafter_result *res, const drafter_options options);
void drafter_free_result(drafter_result* result);
drafter_result* drafter_check_blueprint(const char* source);
unsigned int drafter_version(void);
const char* drafter_version_string(void);
"""
        )

        self.libdrafter_path = libdrafter_path or self.find_library()
        self.libdrafter = self.dlopen(self.libdrafter_path)
