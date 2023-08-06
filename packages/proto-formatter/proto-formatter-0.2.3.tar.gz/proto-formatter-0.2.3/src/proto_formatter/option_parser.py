from .comment import CommentParser
from .constant import EQUAL_SIGN, SEMICOLON
from .proto_structures import Option
from .protobuf import Protobuf
from .util import strip


class OptionParser(CommentParser):

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comments):
        new_option = cls._parse(line, top_comments)
        cls._check(new_option, proto_obj)
        proto_obj.options.append(new_option)

    @classmethod
    def _check(cls, new_option, proto_obj: Protobuf):
        for option in proto_obj.options:
            if option.name == new_option.name:
                raise Exception(f'duplicate option detected: {new_option.name}!')

    @classmethod
    def _parse(cls, line, top_comments):
        name, value = cls._get_value(line)
        comments = cls.create_comment(line, top_comments)
        option = Option(name, value, comments)
        return option

    @classmethod
    def _get_value(cls, line):
        line = line.strip()
        lindex = len('option ')
        equal_sign_index = line.index(EQUAL_SIGN)
        semicolon_index = line.index(SEMICOLON)
        name = strip(line[lindex:equal_sign_index])
        value = strip(line[equal_sign_index + 1:semicolon_index])

        return name, value
