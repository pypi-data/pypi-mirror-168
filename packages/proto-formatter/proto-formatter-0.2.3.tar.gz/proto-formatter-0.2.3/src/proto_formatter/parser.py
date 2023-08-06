from .comment import CommentParser
from .type_detector import ProtoTypeDetector
from .import_parser import ImportParser
from .object_parser import ObjectParser
from .option_parser import OptionParser
from .package_parser import PackageParser
from .protobuf import Protobuf
from .syntax_parser import SyntaxParser


class ProtoParser(CommentParser):
    PARSERS = {
        'syntax': SyntaxParser,
        'package': PackageParser,
        'option': OptionParser,
        'import': ImportParser,
        'message': ObjectParser,
        'enum': ObjectParser,
        'extend': ObjectParser,
        'service': ObjectParser,
        'oneof': SyntaxParser
    }

    @staticmethod
    def load(fp):
        """
        Load proto from file, deserialize it as a Protobuf object.
        :param fp: The absolute file path of the proto file.
        :return: Object of Protobuf.
        """
        lines = ProtoParser._read_lines(fp)
        return ProtoParser._parse(lines)

    @staticmethod
    def loads(proto_str):
        """
        Parse proto string, return a Protobuf object.
        :param proto_str: The proto string need to parse.
        :return: Object of Protobuf.
        """
        lines = proto_str.split('\n')
        return ProtoParser._parse(lines)

    @staticmethod
    def _read_lines(path):
        """
        Read data from file as line list, all blank and empty lines are removed before and after valid text.
        :param path: Absolute file path.
        :return: Line list of the striped file content.
        """
        with open(path) as f:
            content = f.read()
            content = content.strip()
            lines = content.split('\n')
            return lines

    @staticmethod
    def _parse(lines, protobuf_obj=None):
        """
        Parse proto content lines, deserialize them as a Protobuf object.
        :param lines: the proto content lines.
        :return: an object of Protobuf.
        """
        if protobuf_obj is None:
            protobuf_obj = Protobuf()

        top_comments = ProtoTypeDetector().get_top_comments(lines)
        if len(lines) == 0:
            return protobuf_obj

        first_line = lines[0]
        proto_type = ProtoTypeDetector().get_type(first_line)

        parser = ProtoParser.PARSERS[proto_type]()
        if parser is None:
            return protobuf_obj

        if isinstance(parser, ObjectParser):
            parser.parse(lines)
            top_comments = ProtoParser.create_comment(first_line, top_comments)
            all_comments = top_comments + parser.objects[0].comments
            parser.objects[0].comments = all_comments
            protobuf_obj.objects.extend(parser.objects)
        else:
            line = lines.pop(0)
            parser.parse_and_add(protobuf_obj, line, top_comments)

        if len(lines) == 0:
            return protobuf_obj

        return ProtoParser._parse(lines, protobuf_obj)
