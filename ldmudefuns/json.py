from .common import check_arg
import ldmud, json

class LPCEncoder(json.JSONEncoder):
    """Class to encode LDMud specific types."""
    def default(self, obj):
        if isinstance(obj, ldmud.Array):
            return list(obj)
        if isinstance(obj, ldmud.Mapping):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)

class LPCDecoder(json.JSONDecoder):
    """Class to decode JSON objects and arrays to LDMud mappings and arrays"""
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs)

        self.orig_parse_array = self.parse_array
        self.orig_parse_object = self.parse_object

        self.parse_array = LPCDecoder.parse_array.__get__(self, LPCDecoder)
        self.parse_object = LPCDecoder.parse_object.__get__(self, LPCDecoder)

        self.scan_once = json.scanner.py_make_scanner(self)

    def parse_array(self, *args, **kwargs):
        (val, end) = self.orig_parse_array(*args, **kwargs)
        return (ldmud.Array(val), end)

    def parse_object(self, *args, **kwargs):
        (val, end) = self.orig_parse_object(*args, **kwargs)
        return (ldmud.Mapping(val), end)

def efun_json_serialize(value) -> str:
    """
    SYNOPSIS

            string json_serialize(mixed <data>)

    DESCRIPTION
            This efun creates a JSON object from the given LPC variable and
            returns the object encoded as a LPC string. For container types like.
            arrays, mappings and structs, this will be done recursively.

            Only the following LPC types are serialized. All other LPC types cause
            a  runtime error.
            <int>        -> JSON int
            <float>      -> JSON double
            <string>     -> JSON string
            <mapping>    -> JSON objects
            <array>      -> JSON arrays
            <struct>     -> JSON objects

            The function is available only if the driver is compiled with Iksemel
            support. In that case, __JSON__ is defined..

    LIMITATIONS.
            Only mappings with a width of 1 value per key and only string keys
            can be serialized.

    EXAMPLES
            json_serialize(42)              -> "42"
            json_serialize(42.0)            -> "42.0"
            json_serialize("hello world\n") -> "\"hello world\\n\""
            json_serialize(({1,2,3,4,5,6})) -> "[ 1, 2, 3, 4, 5, 6 ]"
            json_serialize(([ "test 1": 42, "test 2": 42.0 ]))
                                    -> "{ \"test 2\": 42.000000, \"test 1\": 42 }"

    SEE ALSO
            json_parse(E)

    """
    return json.dumps(value, cls=LPCEncoder)

def efun_json_parse(text: str):
    """
    SYNOPSIS

            mixed json_parse(string jsonstring)

    DESCRIPTION
            This efun parses the JSON object encoded as string in <jsonstr> into a
            suitable LPC type.

            Handles the following JSON types:
            <null>        -> int (0)
            <boolean>     -> int (0 or 1)
            <int | int64> -> int
            <double>      -> float
            <string>      -> string
            <object>      -> mapping
            <array>       -> arrays
            All other JSON types cause a runtime error.

            The JSON object can nest other JSON objects.

            The function is available only if the driver is compiled with Iksemel
            support. In that case, __JSON__ is defined..

    EXAMPLES
            json_parse("42")              -> 42
            json_parse("42.0")            -> 42.0
            json_parse("\"hello world\\n\"")   -> "hello world\n"
            json_parse("[ 1, 2, 3, 4, 5, 6 ]") -> ({1,2,3,4,5,6})
            json_parse("{ \"test 2\": 42.000000, \"test 1\": 42 }")
                                          -> ([ "test 1": 42, "test 2": 42.0 ])

    SEE ALSO
            json_serialize(E)
    """
    return json.loads(text, cls=LPCDecoder)

def register():
    ldmud.register_efun("json_serialize", efun_json_serialize)
    ldmud.register_efun("json_parse", efun_json_parse)
