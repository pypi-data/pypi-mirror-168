from .comment import CommentParser
from .proto_structures import Package
from .protobuf import Protobuf


class PackageParser(CommentParser):

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comments):
        cls._check(proto_obj)
        proto_obj.package = cls._parse(line, top_comments)

    @classmethod
    def _check(cls, proto_obj):
        if proto_obj.package is not None:
            raise Exception('duplicate package detected!')

    @classmethod
    def _parse(cls, line, top_comments):
        value = cls._get_value(line)
        comments = CommentParser.create_comment(line, top_comments)
        package = Package(value, comments)
        return package

    @classmethod
    def _get_value(cls, line):
        line = line.strip()
        value = line[len('package '):line.index(';')].strip()
        return value
