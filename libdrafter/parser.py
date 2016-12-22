from __future__ import unicode_literals

import contextlib

import cffi


class ParserError(Exception):
    pass


class Parser(cffi.FFI):
    YAML = 0
    JSON = 1
    ALL_FORMAT = {YAML, JSON}

    @contextlib.contextmanager
    def memory_safe(self, p, destructor=None):
        destructor = destructor or self.free
        try:
            yield
        finally:
            if p != self.NULL:
                destructor(p)

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
void free(void *);

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
        self.drafter = self.dlopen(self.libdrafter_path)

    def drafter_version(self):
        return self.drafter.drafter_version()

    def drafter_version_string(self):
        return self.string(self.drafter.drafter_version_string())

    def drafter_parse_blueprint_to(self, source, sourcemap=True, drafter_format=YAML):
        """
        Parse API Blueprint and serialize it to given format.
        """
        if drafter_format not in self.ALL_FORMAT:
            raise ParserError("drafter must be one of {}".format(self.ALL_FORMAT))

        pout = self.new('char**', self.NULL)
        options = {'sourcemap': sourcemap, 'format': drafter_format}

        with self.memory_safe(pout, destructor=lambda p: p[0] != self.NULL and self.free(p[0])):
            ret = self.drafter.drafter_parse_blueprint_to(
                source,
                pout,
                options
            )
            if ret != 0:
                raise ParserError("drafter parse blueprint failed: {}.".format(ret))

            return self.string(pout[0])

    def free(self, p):
        return self.drafter.free(p)

    def drafter_parse_blueprint(self, source):
        """
        Pay attention to this method, you have to free `drafter_result` manually.
        Parse API Blueprint and return result, which is a opaque handle for later use.
        """
        p_drafter_result = self.new('drafter_result**', self.NULL)
        ret = self.drafter.drafter_parse_blueprint(
            source,
            p_drafter_result
        )
        if ret != 0:
            raise ParserError("drafter parse blueprint failed: {}.".format(ret))
        return p_drafter_result[0]

    def drafter_serialize(self, drafter_result, sourcemap=True, drafter_format=YAML):
        """
        Serialize result to given format.
        """
        options = {'sourcemap': sourcemap, 'format': drafter_format}
        ret = self.drafter.drafter_serialize(
            drafter_result,
            options
        )
        if ret == self.NULL:
            raise ParserError("serialize drafter result failed: {}.".format(ret))
        with self.memory_safe(ret, destructor=lambda p: self.free(p)):
            return self.string(ret)

    def drafter_free_result(self, drafter_result):
        """
        Free memory allocated for result handler.
        """
        self.drafter.drafter_free_result(drafter_result)

    def drafter_check_blueprint(self, source, serialize_result=True, **kwargs):
        """
        Pay attention to this method, you have to free `drafter_result` manually when `serialize_result` is False.
        Parse API Blueprint and return only annotations, if NULL than document is error and warning free.
        """
        drafter_result = self.drafter.drafter_check_blueprint(
            source
        )
        if not serialize_result:
            return drafter_result

        if drafter_result == self.NULL:
            return

        with self.memory_safe(drafter_result, destructor=self.drafter_free_result):
            return self.drafter_serialize(drafter_result, **kwargs)
