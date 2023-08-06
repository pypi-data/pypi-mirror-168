from .comment import CommentParser
from .protobuf import Protobuf
from .proto_structures import Syntax
from .util import strip


class SyntaxParser(CommentParser):

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comment_list):
        cls._check(proto_obj)

        proto_obj.syntax = cls._parse(line, top_comment_list)

    @classmethod
    def _check(cls, proto_obj):
        if proto_obj.syntax is not None:
            raise Exception('duplicate package detected!')

    @classmethod
    def _parse(cls, line, top_comment_list):
        value = cls._get_value(line)
        comments = cls.create_comment(line, top_comment_list)
        syntax = Syntax(value, comments)
        return syntax

    @classmethod
    def _get_value(cls, line):
        line = line.strip().replace(' ', '')
        value = strip(line[len('syntax='):line.index(';')])
        return value
