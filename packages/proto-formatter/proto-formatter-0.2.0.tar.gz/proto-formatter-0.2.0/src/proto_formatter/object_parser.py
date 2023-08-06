import uuid
from attrdict import AttrDict
from .type_detector import ProtoTypeDetector
from .comment import CommentParser
from .constant import (
    RIGHT_BRACE,
    EQUAL_SIGN,
    LEFT_BRACE,
    SEMICOLON,
    RIGHT_ANGLE_BRACKET,
    LEFT_SQUARE_BRACKET,
    RIGHT_SQUARE_BRACKET
)
from .proto_structures import EnumElement
from .proto_structures import Extend
from .proto_structures import ExtendElement
from .proto_structures import Message
from .proto_structures import MessageElement
from .proto_structures import ProtoEnum
from .proto_structures import Service
from .proto_structures import ServiceElement
from .proto_structures import Oneof
from .protobuf import Protobuf


class ObjectParser(CommentParser):

    def __init__(self):
        super().__init__()
        self.objects = []
        self.objects_dict = {}

        self.left_brace_stack = []
        self.right_brace_stack = []

        self.obj = None
        self.current_obj = None

    @classmethod
    def _get_obj_name(cls, line):
        parts = line.strip().split(' ')
        parts = list(filter(None, parts))
        name = parts[1]
        return name

    @classmethod
    def parse_obj_field(cls, line, top_comments):
        raise NotImplementedError("Element parse not implemented.")

    def parse_and_add(self, proto_obj: Protobuf, lines):
        self.parse(lines)
        proto_obj.objects.append(self.obj)

    def parse(self, lines):
        top_comments = ProtoTypeDetector().get_top_comments(lines)
        if len(lines) == 0:
            if top_comments:
                comments = self.create_bottom_comments(top_comments)
                # add it to the comments of last one object
                self.current_obj.comments.extend(comments)
            return

        first_line = lines[0]
        if ProtoTypeDetector().is_object_start(first_line):
            self.left_brace_stack.append(LEFT_BRACE)

        proto_type = ProtoTypeDetector().get_type(first_line)
        if 'message' == proto_type or 'enum' == proto_type or 'service' == proto_type or 'extend' == proto_type or 'oneof' == proto_type:
            name = self._get_obj_name(first_line)
            top_comments = self.create_comment(first_line, top_comments)
            obj = self.create_proto_obj(proto_type, name, top_comments)
            self.objects_dict[obj.id] = obj

            if self.obj:
                self.current_obj.elements.append(obj)
                obj.parent_id = self.current_obj.id
            else:
                self.obj = obj
                obj.parent_id = None
            self.current_obj = obj  # used as a pointer

            lines.pop(0)
            return self.parse(lines)
        elif 'enum_element' == proto_type or 'message_element' == proto_type or 'service_element' == proto_type or 'oneof' == proto_type:
            element = self.parse_element(proto_type, first_line, top_comments)
            self.current_obj.elements.append(element)

            lines.pop(0)
            return self.parse(lines)
        else:
            if ProtoTypeDetector().is_object_end(first_line):
                self.right_brace_stack.append(RIGHT_BRACE)
                if top_comments:
                    comments = self.create_bottom_comments(top_comments)
                    # add it to the comments of last one element
                    self.current_obj.elements[-1].comments.extend(comments)
                if self.current_obj.parent_id is None:  # root node, finish a root level object parse
                    self.objects.append(self.current_obj)
                    self.obj = None  # finished an object and all nested inner objects(if it has) parse.
                else:
                    self.current_obj = self.objects_dict[self.current_obj.parent_id]

                lines.pop(0)
                return self.parse(lines)

    @classmethod
    def create_proto_obj(cls, proto_type, name, comments=None):
        if comments is None:
            comments = []
        obj_class = {
            'enum': ProtoEnum,
            'message': Message,
            'service': Service,
            'extend': Extend,
            'oneof': Oneof
        }[proto_type]

        obj = obj_class(name=name, elements=[], comments=comments)
        obj.id = uuid.uuid4().hex

        return obj

    @classmethod
    def parse_element(cls, proto_type, line, top_comments=None):
        if top_comments is None:
            top_comments = []
        parse_method = {
            'enum_element': cls.parse_enum_element,
            'message_element': cls.parse_message_element,
            'service_element': cls.parse_service_element,
            # 'extend_element': cls.parse_extend_element
        }[proto_type]

        return parse_method(line, top_comments=top_comments)

    @classmethod
    def parse_enum_element(cls, line, top_comments=None):
        # BAGGAGE_TYPE_CARRY_ON = 1;
        if top_comments is None:
            top_comments = []
        line = line.strip()
        equal_sign_index = line.index(EQUAL_SIGN)
        semicolon_index = line.index(SEMICOLON)
        str_before_equqal_sign = line[:equal_sign_index]
        parts = str_before_equqal_sign.split(' ')
        parts = list(filter(None, parts))
        value = line[equal_sign_index + 1:semicolon_index].strip()
        data = cls.get_number_and_annotation(value)

        comments = cls.create_comment(line, top_comments)
        return EnumElement(name=parts[0], number=data.number, annotation=data.annotation, comments=comments)

    @classmethod
    def parse_message_element(cls, line, top_comments=None):
        # common.RequestContext  request_context = 1;
        # map<string, Project> projects = 3;
        # // x must be either "foo", "bar", or "baz"
        # string x = 1 [(validate.rules).string = {in: ["foo", "bar", "baz"]}];
        if top_comments is None:
            top_comments = []
        if 'map<' in line:
            return cls.make_map_element(line, top_comments)

        line = line.strip()
        equal_sign_index = line.index(EQUAL_SIGN)
        semicolon_index = line.index(SEMICOLON)
        str_before_equqal_sign = line[:equal_sign_index]
        parts = str_before_equqal_sign.split(' ')
        parts = list(filter(None, parts))
        value = line[equal_sign_index + 1:semicolon_index].strip()
        data = cls.get_number_and_annotation(value)

        comments = cls.create_comment(line, top_comments)
        if len(parts) == 2:
            return MessageElement(type=parts[0], name=parts[1], number=data.number, annotation=data.annotation,
                                  comments=comments)
        if len(parts) == 3:
            return MessageElement(label=parts[0], type=parts[1], name=parts[2], number=data.number,
                                  annotation=data.annotation,
                                  comments=comments)

        return None

    @classmethod
    def parse_extend_element(cls, line, top_comments=None):
        # common.RequestContext  request_context = 1;
        line = line.strip()
        equal_sign_index = line.index(EQUAL_SIGN)
        semicolon_index = line.index(SEMICOLON)
        str_before_equqal_sign = line[:equal_sign_index]
        parts = str_before_equqal_sign.split(' ')
        parts = list(filter(None, parts))
        value = line[equal_sign_index + 1:semicolon_index].strip()
        data = cls.get_number_and_annotation(value)

        comments = cls.create_comment(line, top_comments)
        if len(parts) == 2:
            return ExtendElement(type=parts[0], name=parts[1], number=data.number, annotation=data.annotation,
                                 comments=comments)
        if len(parts) == 3:
            return ExtendElement(label=parts[0], type=parts[1], name=parts[2], number=data.number,
                                 annotation=data.annotation,
                                 comments=comments)

        return None

    @classmethod
    def make_map_element(cls, line, top_comments=None):
        # map<string, Project> projects = 3;
        if top_comments is None:
            top_comments = []
        right_bracket_index = line.index(RIGHT_ANGLE_BRACKET)
        equal_sign_index = line.index(EQUAL_SIGN)
        semicolon_index = line.index(SEMICOLON)
        map_type = line[:right_bracket_index + 1]
        map_type = map_type.strip().replace(' ', '')
        type_parts = map_type.split(',')
        map_type = ', '.join(type_parts)
        name = line[right_bracket_index + 1:equal_sign_index]
        name = name.strip()
        number = line[equal_sign_index + 1:semicolon_index]
        number = number.strip()
        comments = cls.create_comment(line, top_comments)

        return MessageElement(type=map_type, name=name, number=number, comments=comments)

    @classmethod
    def parse_service_element(cls, line, top_comments=None):
        # rpc SeatAvailability (SeatAvailabilityRequest) returns (SeatAvailabilityResponse);
        if top_comments is None:
            top_comments = []
        line = line.strip().replace('(', '')
        line = line.replace(')', '')

        semicolon_index = line.index(SEMICOLON)
        str_before_semicolon = line[:semicolon_index]
        parts = str_before_semicolon.split(' ')
        parts = list(filter(None, parts))
        comments = cls.create_comment(line, top_comments)

        return ServiceElement(label=parts[0], name=parts[1], request=parts[2], response=parts[4], comments=comments)

    @classmethod
    def get_number_and_annotation(cls, value):
        number = value
        annotation = ''
        if LEFT_SQUARE_BRACKET in value:
            left_brace_stack_index = value.index(LEFT_SQUARE_BRACKET)
            right_brace_stack_index = value.rindex(RIGHT_SQUARE_BRACKET)
            annotation = value[left_brace_stack_index:right_brace_stack_index + 1]
            annotation = annotation.strip()
            number = value[:left_brace_stack_index]
            number = number.strip()

        return AttrDict({
            'number': number,
            'annotation': annotation
        })
