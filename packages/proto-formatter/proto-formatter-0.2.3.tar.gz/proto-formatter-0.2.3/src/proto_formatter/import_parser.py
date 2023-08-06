from .comment import CommentParser
from .constant import SEMICOLON
from .proto_structures import Import
from .protobuf import Protobuf
from .util import strip


class ImportParser(CommentParser):

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comments):
        new_import = cls._parse(line, top_comments)
        cls._check(new_import, proto_obj)
        proto_obj.imports.append(new_import)

    @classmethod
    def _check(cls, new_import, proto_obj):
        for existing_import in proto_obj.imports:
            if existing_import.value == new_import.value:
                raise Exception(f'duplicate import detected: {new_import.value}!')

    @classmethod
    def _parse(cls, line, top_comments):
        value = cls._get_value(line)
        comments = cls.create_comment(line, top_comments)
        n_import = Import(value, comments)
        return n_import

    @classmethod
    def _get_value(cls, line):
        line = line.strip()
        value = strip(line[len('import '):line.index(SEMICOLON)])
        return value
