from enum import Enum


class Position(Enum):
    LEFT = 'left'
    Right = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'


class Comment:
    def __init__(self, text: str, position: Position):
        self.text = text
        self.position = position


class Syntax:
    key = "syntax"

    def __init__(self, value, comments: list):
        self.value = value
        self.comments = comments


class Package:
    key = "package"

    def __init__(self, value, comments: list):
        self.value = value
        self.comments = comments


class Import:
    key = "import"

    def __init__(self, value, comments: list):
        self.value = value
        self.comments = comments


class Option:
    key = "option"

    def __init__(self, name, value, comments: list):
        self.name = name
        self.value = value
        self.comments = comments


class Element:
    def __init__(self, type, name, number, annotation='', label='', comments=[]):
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class MessageElement:
    def __init__(self, type, name, number, annotation='', label='', comments=[]):
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class Message:
    key = "message"

    def __init__(self, name, elements=None, comments=None):
        if elements is None:
            elements = []
        if comments is None:
            comments = []
        self.name = name
        self.elements = elements
        self.comments = comments


class ExtendElement:
    def __init__(self, type, name, number, annotation='', label='', comments=None):
        if comments is None:
            comments = []
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class Extend:
    key = "extend"

    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []

        self.name = name
        self.elements = elements
        self.comments = comments


class OneofElement:
    def __init__(self, type, name, number, annotation='', label='', comments=None):
        if comments is None:
            comments = []
        self.label = label
        self.type = type
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class Oneof:
    key = "oneof"

    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []

        self.name = name
        self.elements = elements
        self.comments = comments


class EnumElement:
    def __init__(self, name, number, annotation='', comments=None):
        if comments is None:
            comments = []
        self.name = name
        self.number = number
        self.annotation = annotation
        self.comments = comments


class ProtoEnum:
    key = "enum"

    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []

        self.name = name
        self.elements = elements
        self.comments = comments


class ServiceElement:
    def __init__(self, label, name, request, response, comments=None):
        if comments is None:
            comments = []
        self.label = label
        self.name = name
        self.request = request
        self.response = response
        self.comments = comments


class Service:
    key = "service"

    def __init__(self, name, elements=None, comments=None):
        if comments is None:
            comments = []
        if elements is None:
            elements = []
        self.name = name
        self.elements = elements
        self.comments = comments
