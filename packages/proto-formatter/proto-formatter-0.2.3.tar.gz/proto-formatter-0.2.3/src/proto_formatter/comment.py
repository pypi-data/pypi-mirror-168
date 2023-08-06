from .proto_structures import Comment
from .constant import (
    SLASH_STAR,
    STAR_SLASH,
    DOUBLE_SLASH,
    STAR
)
from .proto_structures import Position
from .util import remove_prefix, remove_suffix


class CommentParser:
    def __init__(self):
        self.end_line = 0

        self.multiple_comment_start_symbol_stack = []
        self.multiple_comment_end_symbol_stack = []

    def pick_up_comment(self, lines):
        comment_lines = []
        while lines:
            line = lines.pop(0).strip()
            # comment case: /* I'am a comment */
            if self._start_with_multiple_line_comment(line) and self._end_with_multiple_line_comment(line):
                comment_lines.append(line)
                continue

            if self._start_with_multiple_line_comment(line):
                self.multiple_comment_start_symbol_stack.append(SLASH_STAR)
                comment_lines.append(line)
                continue

            if self.is_comment(line):
                comment_lines.append(line)

            if self._end_with_multiple_line_comment(line):
                self.multiple_comment_end_symbol_stack.append(STAR_SLASH)
                continue

            if line and not self.is_comment(line):
                lines.insert(0, line)  # add back
                break

        return comment_lines

    @staticmethod
    def is_not_new_line(variable):
        return variable != '\n'

    def parse(self, comment_lines):
        comment_lines = self.remove_prefix_symbol(comment_lines)

        comment_lines = list(filter(None, comment_lines))
        comment_lines = list(filter(self.is_not_new_line, comment_lines))

        return comment_lines

    def remove_prefix_symbol(self, comment_lines):
        processed_lines = []
        for line in comment_lines:
            if line.strip().startswith(DOUBLE_SLASH):
                # remove the single comment symbol if have, E.g. // I'am a comment
                processed_lines.append(line.strip()[2:].strip())
            elif self._start_with_multiple_line_comment(line) or self._end_with_multiple_line_comment(line):
                # remove the multiple comment symbol if have, E.g. /* I'am a comment */
                processed_lines.append(line.strip().replace(SLASH_STAR, "").replace(STAR_SLASH, ''))
            elif (line.strip().startswith(STAR) or line.strip().startswith(
                    STAR * 2)) and not self._end_with_multiple_line_comment(line):
                # remove the multiple comment symbol if have, E.g. * I'am a comment in multiple line comment
                # Example:
                # /*
                # **    Device information, including user agent, device proto_type and ip address.
                # */
                #
                processed_lines.append(line.strip().replace(STAR, ""))
            else:
                processed_lines.append(line.strip())

        return processed_lines

    @staticmethod
    def _start_with_single_line_comment(line):
        return line.strip().startswith(DOUBLE_SLASH)

    @staticmethod
    def _start_with_multiple_line_comment(line):
        return line.strip().startswith(SLASH_STAR)

    @staticmethod
    def _end_with_multiple_line_comment(line):
        return line.strip().endswith(STAR_SLASH)

    def _is_multiple_comment(self):
        if len(self.multiple_comment_start_symbol_stack) == 0:
            return False

        return len(self.multiple_comment_start_symbol_stack) > len(self.multiple_comment_end_symbol_stack)

    def is_comment(self, line):
        if self._is_multiple_comment():
            return True

        if self._start_with_single_line_comment(line):
            return True

        return False

    @staticmethod
    def parse_single_line_comment(line):
        comment = None
        if line.count(DOUBLE_SLASH) > 0:
            start_index = line.index(DOUBLE_SLASH)
            comment_str = line[start_index:].lstrip(DOUBLE_SLASH).strip()
            comment = Comment(comment_str, Position.Right)
        return comment

    @staticmethod
    def create_top_comments(comments):
        return CommentParser.create_comment_with_position(comments, Position.TOP)

    @staticmethod
    def create_bottom_comments(comments):
        return CommentParser.create_comment_with_position(comments, Position.BOTTOM)

    @staticmethod
    def create_comment_with_position(comments, position: Position):
        result = []
        while comments:
            comment_lines = comments.pop(0)
            text = ''.join(comment_lines)
            text = text.strip()
            text = remove_prefix(text, DOUBLE_SLASH)
            text = remove_prefix(text, SLASH_STAR)
            text = remove_suffix(text, STAR_SLASH)
            text = text.strip()
            result.append(Comment(text, position))
        return result

    @staticmethod
    def create_comment(line, top_comment_list):
        comments = CommentParser.create_top_comments(top_comment_list)
        right_comment = CommentParser.parse_single_line_comment(line)
        if right_comment is not None:
            comments.append(right_comment)
        return comments
