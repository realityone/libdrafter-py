from __future__ import unicode_literals

import cffi


class ParserError(Exception):
    pass


class Parser(cffi.FFI):
    YAML = 0
    JSON = 1
    ALL_FORMAT = {YAML, JSON}

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

    def drafter_version(self):
        return self.libdrafter.drafter_version()

    def drafter_version_string(self):
        return self.string(self.libdrafter.drafter_version_string())

    def drafter_parse_blueprint_to(self, source, sourcemap=True, drafter_format=YAML):
        if drafter_format not in self.ALL_FORMAT:
            raise ParserError("drafter must be one of {}".format(self.ALL_FORMAT))

        out = self.new('char**', self.NULL)
        options = {'sourcemap': sourcemap, 'format': drafter_format}
        ret = self.libdrafter.drafter_parse_blueprint_to(
            source,
            out,
            options
        )
        if ret != 0:
            raise ParserError("drafter parse blueprint failed: {}.".format(ret))
        return self.string(out[0])

    def drafter_parse_blueprint(self, source):
        p_drafter_result = self.new('drafter_result**', self.NULL)
        ret = self.libdrafter.drafter_parse_blueprint(
            source,
            p_drafter_result
        )
        if ret != 0:
            raise ParserError("drafter parse blueprint failed: {}.".format(ret))
        return p_drafter_result[0]

    def drafter_serialize(self, drafter_result, sourcemap=True, drafter_format=YAML):
        options = {'sourcemap': sourcemap, 'format': drafter_format}
        ret = self.libdrafter.drafter_serialize(
            drafter_result,
            options
        )
        if ret == self.NULL:
            raise ParserError("serialize drafter result failed: {}.".format(ret))
        return self.string(ret)

    def drafter_free_result(self, drafter_result):
        self.libdrafter.drafter_free_result(drafter_result)

    def drafter_check_blueprint(self, source):
        drafter_result = self.libdrafter.drafter_check_blueprint(
            source
        )
        if drafter_result == self.NULL:
            raise ParserError("drafter check blueprint failed.")
        return drafter_result
