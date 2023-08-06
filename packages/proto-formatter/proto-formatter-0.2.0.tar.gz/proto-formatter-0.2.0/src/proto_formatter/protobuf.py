import sys
from copy import deepcopy
from enum import Enum

from .proto_structures import EnumElement
from .proto_structures import ExtendElement
from .proto_structures import Extend
from .proto_structures import Import
from .proto_structures import Message
from .proto_structures import MessageElement
from .proto_structures import Option
from .proto_structures import Position
from .proto_structures import ProtoEnum
from .proto_structures import Service
from .proto_structures import ServiceElement
from .proto_structures import Oneof
from .util import to_lines


class Config:
    SPACES_BETWEEN_VALUE_COMMENT = 2
    SPACES_BEFORE_AFTER_EQUAL_SIGN = 1
    SPACES_BETWEEN_NUMBER_ANNOTATION = 1
    ONE_SPACE = ' '
    TOP_COMMENT_INDENTS = ' ' * 4

    def __init__(self,
                 indents_unit=2,
                 align_by_equal_sign=None,
                 top_comment=False,
                 flatten=False,
                 comment_max_length=None,
                 preview=False
                 ):
        self.indents_unit = indents_unit
        self.align_by_equal_sign = align_by_equal_sign
        self.top_comment = top_comment
        self.flatten = flatten
        self.comment_max_length = comment_max_length
        self.preview = preview


class Text:
    def __init__(self, text, color: int):
        self.text = text
        self.color = color

    def color_print(self):
        sys.stdout.write(u"\u001b[38;5;" + str(self.color) + "m" + self.text + u"\u001b[0m")


class ColorConfig(Enum):
    default = 15
    default_key_word = 11
    syntax_key = 11
    syntax_value = 10
    package_key = 11
    package_value = 15
    option_key = 11
    option_name = 15
    option_value = 40
    import_key = 11
    import_value = 40
    obj_key = 11
    obj_name = 15
    message_element_key = 196
    message_element_label = 11
    message_element_type = 150
    message_element_name = 140
    message_element_number = 12
    message_element_annotation = 15
    enum_element_name = 15
    enum_element_number = 12
    enum_element_annotation = 10
    service_element_lable = 11
    service_element_name = 140
    service_element_request = 15
    service_element_response = 15
    comment = 248


class Protobuf:

    def __init__(self):
        self.syntax = None
        self.package = None
        self.options = []
        self.imports = []
        self.objects = []
        self.text_list = []

        self.config = Config()

    def to_string(self,
                  indents=2,
                  align_by_equal_sign=None,
                  top_comment=False,
                  flatten=False,
                  comment_max_length=None,
                  preview=False
                  ):
        self.config = Config(
            indents_unit=indents,
            align_by_equal_sign=align_by_equal_sign,
            top_comment=top_comment,
            flatten=flatten,
            comment_max_length=comment_max_length,
            preview=preview
        )
        if self.config.flatten:
            self.flatten_objects()

        syntax_string = self.syntax_string()
        package_string = self.package_string()
        option_string = self.options_string()
        imports_string = self.imports_string()

        all_lines = []
        for obj in self.objects:
            lines = []
            self.format_object_without_comment(obj, lines, indents=0)
            max_length = self.get_max_length(lines)
            extra = self.get_max_lengths(lines)
            new_lines = []
            self.format_object(obj, new_lines, 0, extra)
            all_lines.append('\n'.join(new_lines))

        object_string = '\n\n'.join(all_lines)
        contents = [syntax_string, package_string, option_string, imports_string, object_string]
        contents = list(filter(None, contents))
        content = '\n\n'.join(contents)
        content = content + '\n'
        if self.config.preview:
            self.print_with_color()
        return content

    def print_with_color(self):
        print()
        for text in self.text_list:
            text.color_print()
        print()

    def flatten_objects(self):
        new_objects = []

        for obj in self.objects:
            new_obj = deepcopy(obj)
            new_obj.elements = []
            for element in obj.elements:
                if isinstance(element, (Message, ProtoEnum, Service)):
                    self.flatten_object(element, new_objects)
                else:
                    new_obj.elements.append(element)

            new_objects.append(new_obj)

        self.objects = new_objects

    def flatten_object(self, obj, new_objects: list):
        new_obj = deepcopy(obj)
        new_obj.elements = []

        for element in obj.elements:
            if isinstance(element, (Message, ProtoEnum, Service)):
                self.flatten_object(element, new_objects)
            else:
                new_obj.elements.append(element)

        new_objects.append(new_obj)

    @staticmethod
    def get_max_length(lines):
        length = 0
        for line in lines:
            if length < len(line):
                length = len(line)

        return length

    def get_max_lengths(self, lines):
        max_equal_sign_index = 0
        max_length_of_number = 0
        max_length_of_object_line = 0
        max_length_of_service_element_line = 0
        s1 = ''
        s2 = ''
        for line in lines:
            if '=' in line:
                equa_sign_index = line.index('=')
                if max_equal_sign_index < equa_sign_index:
                    max_equal_sign_index = equa_sign_index
                    s1 = line[:equa_sign_index]

                semicolon_index = line.index(';')
                number_str = line[equa_sign_index + 1:semicolon_index].strip()
                number_length = len(number_str)
                if max_length_of_number < number_length:
                    max_length_of_number = number_length
                    s2 = number_str
            elif line.strip().startswith('rpc'):
                if max_length_of_service_element_line < len(line):
                    max_length_of_service_element_line = len(line)
            else:
                if max_length_of_object_line < len(line):
                    max_length_of_object_line = len(line)

        max_length_sample = f'{s1.rstrip()}{self.config.ONE_SPACE * self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN}={self.config.ONE_SPACE * self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN}{s2};'
        max_length = max(len(max_length_sample), max_length_of_service_element_line, max_length_of_object_line)

        return {
            'max_length': max_length,
            'max_equal_sign_index': max_equal_sign_index,
            'max_length_of_number': max_length_of_number,
            'max_length_of_object_line': max_length_of_object_line
        }

    def syntax_string(self):
        if not self.syntax:
            return ''

        line = f'{self.syntax.key} = "{self.syntax.value}";'
        color_text_list = [
            Text(self.syntax.key, ColorConfig.syntax_key.value),
            Text(" ", ColorConfig.default.value),
            Text("=", ColorConfig.default.value),
            Text(" ", ColorConfig.default.value),
            Text('"', ColorConfig.default.value),
            Text(self.syntax.value, ColorConfig.syntax_value.value),
            Text('"', ColorConfig.default.value),
            Text(";", ColorConfig.default.value),
        ]

        syntax_string = self.make_string(line, 0, self.syntax.comments, self.config.SPACES_BETWEEN_VALUE_COMMENT,
                                         color_text_list)
        self.text_list.append(Text("\n", ColorConfig.default.value))
        return syntax_string

    def package_string(self):
        if not self.package:
            return ''

        line = f'{self.package.key} {self.package.value};'
        color_text_list = [
            Text(self.package.key, ColorConfig.package_key.value),
            Text(" ", ColorConfig.default.value),
            Text(self.package.value, ColorConfig.syntax_value.value),
            Text(";", ColorConfig.default.value)
        ]

        package_string = self.make_string(line, 0, self.package.comments, self.config.SPACES_BETWEEN_VALUE_COMMENT,
                                          color_text_list)
        self.text_list.append(Text("\n", ColorConfig.default.value))
        return package_string

    def options_string(self):
        if not self.options:
            return ''

        max_length = self.max_length_of_option()

        string_list = []
        for option in self.options:
            string = self.option_string(option, max_length)
            string_list.append(string)

        self.text_list.append(Text("\n", ColorConfig.default.value))
        return '\n'.join(string_list)

    def max_length_of_option(self):
        max_length = 0
        for option in self.options:
            if option.value == 'true' or option.value == 'false':
                line = f'{option.key} {option.name} = {option.value};'
            else:
                line = f'{option.key} {option.name} = "{option.value}";'

            if max_length < len(line):
                max_length = len(line)

        return max_length

    def option_string(self, option: Option, max_length):
        if option.value == 'true' or option.value == 'false':
            line = f'{option.key} {option.name} = {option.value};'
            color_text_list = [
                Text(option.key, ColorConfig.option_key.value),
                Text(" ", ColorConfig.default.value),
                Text(option.name, ColorConfig.option_name.value),
                Text(" ", ColorConfig.default.value),
                Text("=", ColorConfig.default.value),
                Text(" ", ColorConfig.default.value),
                Text(option.value, ColorConfig.option_value.value),
                Text(";", ColorConfig.default.value)
            ]
        else:
            line = f'{option.key} {option.name} = "{option.value}";'
            color_text_list = [
                Text(option.key, ColorConfig.option_key.value),
                Text(" ", ColorConfig.default.value),
                Text(option.name, ColorConfig.option_name.value),
                Text(" ", ColorConfig.default.value),
                Text("=", ColorConfig.default.value),
                Text(" ", ColorConfig.default.value),
                Text('"', ColorConfig.default.value),
                Text(option.value, ColorConfig.option_value.value),
                Text('"', ColorConfig.default.value),
                Text(";", ColorConfig.default.value)
            ]

        space_between_number_comment = max_length - len(line) + self.config.SPACES_BETWEEN_VALUE_COMMENT

        return self.make_string(line, 0, option.comments, space_between_number_comment, color_text_list)

    def imports_string(self):
        if not self.imports:
            return ''

        max_length = self.max_length_of_import()

        string_list = []
        for obj in self.imports:
            string = self.import_string(obj, max_length)
            string_list.append(string)

        self.text_list.append(Text("\n", ColorConfig.default.value))
        return '\n'.join(string_list)

    def max_length_of_import(self):
        max_length = 0
        for obj in self.imports:
            line = f'{obj.key} "{obj.value}";'

            if max_length < len(line):
                max_length = len(line)

        return max_length

    def import_string(self, import_obj: Import, max_length):
        line = f'{import_obj.key} "{import_obj.value}";'
        color_text_list = [
            Text(import_obj.key, ColorConfig.import_key.value),
            Text(" ", ColorConfig.default.value),
            Text('"', ColorConfig.default.value),
            Text(import_obj.value, ColorConfig.import_value.value),
            Text('"', ColorConfig.default.value),
            Text(";", ColorConfig.default.value)
        ]
        space_between_number_comment = max_length - len(line) + self.config.SPACES_BETWEEN_VALUE_COMMENT

        return self.make_string(line, 0, import_obj.comments, space_between_number_comment, color_text_list)

    def create_object_header(self, obj, indents, no_comment, max_length):
        line = f'{obj.key} {obj.name} ' + "{"
        color_text_list = [
            Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
            Text(obj.key, ColorConfig.obj_key.value),
            Text(" ", ColorConfig.default.value),
            Text(obj.name, ColorConfig.obj_name.value),
            Text(" ", ColorConfig.default.value),
            Text("{", ColorConfig.default.value)
        ]

        space_between_number_comment = 2
        if max_length:
            space_between_number_comment = max_length - len(line) + self.config.SPACES_BETWEEN_VALUE_COMMENT

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            comments = [comment for comment in obj.comments if comment.position is not Position.BOTTOM]
            return self.make_string(line, indents, comments, space_between_number_comment, color_text_list)

    def create_object_rear(self, obj, indents):
        bottom_comments = [comment for comment in obj.comments if comment.position == Position.BOTTOM]
        color_text_list = [
            Text("}", ColorConfig.default.value)
        ]

        rear = self.make_string('}', indents, bottom_comments, self.config.SPACES_BETWEEN_VALUE_COMMENT,
                                color_text_list)
        self.text_list.append(Text("\n", ColorConfig.default.value))
        return rear

    @staticmethod
    def get_object_element_class(obj):
        classes = {
            'message': MessageElement,
            'enum': EnumElement,
            'service': ServiceElement,
            'extend': MessageElement,
            'oneof': MessageElement
        }
        return classes[obj.key]

    def get_make_object_element_string_method(self, obj):
        methods = {
            Message.key: self.message_element_string,
            ProtoEnum.key: self.enum_element_string,
            Service.key: self.service_element_string,
            Extend.key: self.extend_element_string,
            Oneof.key: self.message_element_string
        }
        return methods[obj.key]

    def format_object(self, obj, string_list, indents, extra):
        max_length = extra['max_length']
        max_equal_sign_index = extra['max_equal_sign_index']
        max_length_of_number = extra['max_length_of_number']
        max_length_of_object_line = extra['max_length_of_object_line']

        message_header = self.create_object_header(obj, indents, False, max_length - indents)
        string_list.append(message_header)
        element_class = self.get_object_element_class(obj)
        element_str_method = self.get_make_object_element_string_method(obj)

        for element in obj.elements:
            if isinstance(element, element_class):
                line = element_str_method(
                    element,
                    indents + self.config.indents_unit,
                    True,
                    self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.config.SPACES_BETWEEN_VALUE_COMMENT
                )

                if self.config.align_by_equal_sign:
                    line_without_number = line.split('=')[0].rstrip()
                    space_between_name_equal_sign = max_equal_sign_index - len(line_without_number)

                    if hasattr(element, 'number'):
                        space_between_number_comment = max_length - max_equal_sign_index - len('=') - len(';') - len(
                            element.number) - len(
                            element.annotation) - self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN - self.config.SPACES_BETWEEN_NUMBER_ANNOTATION + self.config.SPACES_BETWEEN_VALUE_COMMENT

                        if element.annotation == '':
                            # the space between number and rules is tripped, so shouldn't count it
                            space_between_number_comment = space_between_number_comment + self.config.SPACES_BETWEEN_NUMBER_ANNOTATION

                    elif line.strip().startswith('rpc'):
                        space_between_number_comment = max_length - len(line) + self.config.SPACES_BETWEEN_VALUE_COMMENT
                    else:
                        space_between_number_comment = max_length - len(
                            line) - self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN + self.config.SPACES_BETWEEN_VALUE_COMMENT

                    string = element_str_method(
                        element,
                        indents + self.config.indents_unit,
                        False,
                        space_between_name_equal_sign,
                        self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        space_between_number_comment
                    )
                else:
                    space_between_number_comment = max_length - len(line) + self.config.SPACES_BETWEEN_VALUE_COMMENT
                    string = element_str_method(
                        element,
                        indents + self.config.indents_unit,
                        False,
                        self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        space_between_number_comment
                    )

                string_list.append(string)
            else:
                self.format_object(element, string_list, indents + self.config.indents_unit, extra)

        message_rear = self.create_object_rear(obj, indents)
        string_list.append(message_rear)

    def format_object_without_comment(self, obj, string_list, indents):
        message_header = self.create_object_header(obj, no_comment=True, indents=indents, max_length=None)
        string_list.append(message_header)
        element_class = self.get_object_element_class(obj)
        element_str_method = self.get_make_object_element_string_method(obj)

        for element in obj.elements:
            if isinstance(element, element_class):
                string = element_str_method(
                    element,
                    indents + self.config.indents_unit,
                    True,
                    self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.config.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.config.SPACES_BETWEEN_VALUE_COMMENT
                )
                string_list.append(string)
            else:
                self.format_object_without_comment(element, string_list, indents=indents + self.config.indents_unit)

        message_rear = self.make_indented_line('}', indents=indents)
        string_list.append(message_rear)

    def message_element_string(
            self,
            message_element: MessageElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        line = f'{message_element.label} {message_element.type} {message_element.name}{self.config.ONE_SPACE * space_between_name_equal_sign}={self.config.ONE_SPACE * space_between_equal_sign_number}{message_element.number}{self.config.ONE_SPACE * self.config.SPACES_BETWEEN_NUMBER_ANNOTATION}{message_element.annotation}'
        line = line.strip()  # remove prefix space when obj.label is empty string or rules is empty.
        line = f'{line};'
        color_text_list = [
            Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
            Text(message_element.label, ColorConfig.message_element_label.value),
            Text(" ", ColorConfig.default.value),
            Text(message_element.type, ColorConfig.message_element_type.value),
            Text(" ", ColorConfig.default.value),
            Text(message_element.name, ColorConfig.message_element_name.value),
            Text(self.config.ONE_SPACE * space_between_name_equal_sign, ColorConfig.default.value),
            Text("=", ColorConfig.default.value),
            Text(self.config.ONE_SPACE * space_between_equal_sign_number, ColorConfig.default.value),
            Text(message_element.number, ColorConfig.message_element_number.value),
            Text(self.config.ONE_SPACE * self.config.SPACES_BETWEEN_NUMBER_ANNOTATION, ColorConfig.default.value),
            Text(message_element.annotation, ColorConfig.message_element_annotation.value)
        ]
        if message_element.label.strip() == "":
            del color_text_list[1]
            del color_text_list[1]
        if message_element.annotation.strip() == "":
            del color_text_list[-1]
            del color_text_list[-1]
        color_text_list.append(Text(";", ColorConfig.default.value))

        if no_comment:
            return self.make_indented_line(line, indents)
        else:
            return self.make_string(line, indents, message_element.comments, space_between_number_comment,
                                    color_text_list)

    def extend_element_string(
            self,
            extend_element: ExtendElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        # using the message element making string
        return self.message_element_string(extend_element,
                                           indents,
                                           no_comment,
                                           space_between_name_equal_sign,
                                           space_between_equal_sign_number,
                                           space_between_number_comment)

    def enum_element_string(
            self,
            enum_element: EnumElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        line = f'{enum_element.name}{self.config.ONE_SPACE * space_between_name_equal_sign}={self.config.ONE_SPACE * space_between_equal_sign_number}{enum_element.number}{self.config.ONE_SPACE * self.config.SPACES_BETWEEN_NUMBER_ANNOTATION}{enum_element.annotation}'
        line = line.strip()  # remove prefix space when rules is empty.
        line = f'{line};'
        color_text_list = [
            Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
            Text(enum_element.name, ColorConfig.enum_element_name.value),
            Text(self.config.ONE_SPACE * space_between_name_equal_sign, ColorConfig.default.value),
            Text("=", ColorConfig.default.value),
            Text(self.config.ONE_SPACE * space_between_equal_sign_number, ColorConfig.default.value),
            Text(enum_element.number, ColorConfig.enum_element_number.value),
            Text(self.config.ONE_SPACE * self.config.SPACES_BETWEEN_NUMBER_ANNOTATION, ColorConfig.default.value),
            Text(enum_element.annotation, ColorConfig.enum_element_annotation.value),
        ]
        if enum_element.annotation.strip() == "":
            del color_text_list[-1]
            del color_text_list[-1]
        color_text_list.append(Text(";", ColorConfig.default.value))

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, enum_element.comments, space_between_number_comment, color_text_list)

    def service_element_string(
            self,
            service_element: ServiceElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        # rpc SeatAvailability (SeatAvailabilityRequest) returns (SeatAvailabilityResponse);
        line = f'{service_element.label} {service_element.name} ({service_element.request}) returns ({service_element.response});'
        color_text_list = [
            Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
            Text(service_element.label, ColorConfig.service_element_lable.value),
            Text(" ", ColorConfig.default.value),
            Text(service_element.name, ColorConfig.service_element_name.value),
            Text(" ", ColorConfig.default.value),
            Text("(", ColorConfig.default.value),
            Text(service_element.request, ColorConfig.service_element_request.value),
            Text(")", ColorConfig.default.value),
            Text(" ", ColorConfig.default.value),
            Text("returns", ColorConfig.default_key_word.value),
            Text(" ", ColorConfig.default.value),
            Text("(", ColorConfig.default.value),
            Text(service_element.response, ColorConfig.service_element_response.value),
            Text(")", ColorConfig.default.value),
            Text(";", ColorConfig.default.value)
        ]

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, service_element.comments, space_between_number_comment,
                                    color_text_list)

    def make_string(self, value_line, indents, comments, space_between_number_comment, color_text_list):
        if self.config.top_comment:
            formatted_comments = self.to_top_comment_lines(comments)
        else:
            formatted_comments = self.to_comment_lines(comments)
        top_comment_lines = formatted_comments["top"]
        bottom_comment_lines = formatted_comments["bottom"]
        right_comment = formatted_comments["right"]

        indented_top_comment_lines = []
        if top_comment_lines:
            comment_results = self.to_comment_lines_with_comment_slash(top_comment_lines, indents)
            indented_top_comment_lines = comment_results["indented_comment_lines"]
            comment_text_list = comment_results["comment_text_list"]
            color_text_list = comment_text_list + color_text_list

        indented_bottom_comment_lines = []
        if bottom_comment_lines:
            comment_results = self.to_comment_lines_with_comment_slash(bottom_comment_lines, indents)
            indented_bottom_comment_lines = comment_results["indented_comment_lines"]
            comment_text_list = comment_results["comment_text_list"]
            color_text_list = comment_text_list + color_text_list

        lines = indented_top_comment_lines
        if right_comment:
            line = f'{value_line}{self.config.ONE_SPACE * space_between_number_comment}// {right_comment}'
            lines.append(line)
            color_comment_text_list = [
                Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
                Text(self.config.ONE_SPACE * space_between_number_comment, ColorConfig.default.value),
                Text("//", ColorConfig.comment.value),
                Text(" ", ColorConfig.default.value),
                Text(right_comment, ColorConfig.comment.value),
                Text("\n", ColorConfig.default.value)
            ]
            color_text_list = color_text_list + color_comment_text_list
            self.text_list.extend(color_text_list)
        else:
            lines.append(value_line)
            color_text_list.insert(0, Text(self.config.ONE_SPACE * indents, ColorConfig.default.value))
            color_text_list.append(Text("\n", ColorConfig.default.value))

            self.text_list.extend(color_text_list)

        if indented_bottom_comment_lines:
            lines.extend(indented_bottom_comment_lines)

        indented_lines = [f'{self.config.ONE_SPACE * indents}{line}' for line in lines]
        string = '\n'.join(indented_lines)

        return string

    def make_indented_line(self, line, indents=0):
        return f'{self.config.ONE_SPACE * indents}{line}'

    def convert_to_lines(self, comment):
        """
        convert comment text to multiple lines if the comment_max_length flag is set and the length of the text exceeds
        it.
        :param comment: comment object.
        :return: string lines of comment text.
        """
        text_lines = [line.strip() for line in comment.text.split('\n')]

        new_text_lines = []
        if self.config.comment_max_length is not None:
            for line in text_lines:
                new_text_lines.extend(to_lines(line, self.config.comment_max_length))
            text_lines = new_text_lines
        return text_lines

    def to_top_comment_lines(self, comments):
        """
        convert right comment to top comment lines:
        (1) keep top comments. If the comment_max_length flag is set and the length of one original line exceeds it,
            this line will be converted to multiple lines.
        (2) convert right comment to multiple lines, append it to top comments lines.
        (3) convert bottom comments(the comments under the last element or follow the message etc.) to multiple lines.
            If the comment_max_length flag is set and the length of one original line exceeds it, this line will be
            converted to multiple lines. This lines will not be appended to top comments lines.
        :param comments: all comments of an object.
        :return: formatted comments lines.
        """
        top_comment_lines = []
        right_comment = ''
        bottom_comment_lines = []
        for comment in comments:
            if comment.position == Position.TOP:
                top_comment_lines.extend(self.convert_to_lines(comment))
            if comment.position == Position.BOTTOM:
                bottom_comment_lines.extend(self.convert_to_lines(comment))
            if comment.position == Position.Right:
                line = comment.text
                text_lines = [line]

                new_text_lines = []
                if self.config.comment_max_length is not None:
                    for l in text_lines:
                        new_text_lines.extend(to_lines(l, self.config.comment_max_length))

                if self.config.comment_max_length is not None:
                    top_comment_lines.extend(new_text_lines)
                else:
                    top_comment_lines.extend(text_lines)

                right_comment = ''
        results = {
            "top": top_comment_lines,
            "right": right_comment,
            "bottom": bottom_comment_lines
        }
        return results

    def to_comment_lines(self, comments):
        """
        convert right comment to comment lines:
        (1) keep top comments. If the comment_max_length flag is set and the length of one original line exceeds it,
            this line will be converted to multiple lines.
        (2) convert right comment to multiple lines, append it to top comments lines.
        (3) convert bottom comments(the comments under the last element or follow the message etc.) to multiple lines.
            If the comment_max_length flag is set and the length of one original line exceeds it, this line will be
            converted to multiple lines. This lines will not be appended to top comments lines.
        :param comments: all comments of an object.
        :return: formatted comments lines.
        """
        top_comment_lines = []
        right_comment = ''
        bottom_comment_lines = []
        for comment in comments:
            if comment.position == Position.TOP:
                top_comment_lines.extend(self.convert_to_lines(comment))
            if comment.position == Position.BOTTOM:
                bottom_comment_lines.extend(self.convert_to_lines(comment))
            if comment.position == Position.Right:
                right_comment = comment.text
        results = {
            "top": top_comment_lines,
            "right": right_comment,
            "bottom": bottom_comment_lines
        }
        return results

    def to_comment_lines_with_comment_slash(self, comment_lines, indents):
        indented_comment_lines = []
        comment_text_list = []
        for comment_line in comment_lines:
            indented_comment_lines.append(f'**{self.config.TOP_COMMENT_INDENTS}{comment_line}')
            one_comment_text_list = [
                Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
                Text("**", ColorConfig.comment.value),
                Text(self.config.TOP_COMMENT_INDENTS, ColorConfig.default.value),
                Text(comment_line, ColorConfig.comment.value),
                Text("\n", ColorConfig.default.value)
            ]
            comment_text_list = comment_text_list + one_comment_text_list
        indented_comment_lines.insert(0, '/*')
        indented_comment_lines.append('*/')

        comment_header_text_list = [
            Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
            Text("/*", ColorConfig.comment.value),
            Text("\n", ColorConfig.default.value)
        ]
        comment_rear_text_list = [
            Text(self.config.ONE_SPACE * indents, ColorConfig.default.value),
            Text("*/", ColorConfig.comment.value),
            Text("\n", ColorConfig.default.value)
        ]
        comment_text_list = comment_header_text_list + comment_text_list + comment_rear_text_list
        result = {
            "indented_comment_lines": indented_comment_lines,
            "comment_text_list": comment_text_list
        }
        return result
