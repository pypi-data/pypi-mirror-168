from tests.tools.test_tools_utils import *


class TextElement():
    def __init__(self, text: str = None, color: str = None, seperator: str = None, seperator_direction: str = None) -> None:
        self._text = text
        self._color = color
        # self._seperator = seperator
        # self._seperator_direction = seperator_direction

    def __str__(self) -> str:
        return colored(self._text, self._color)

    def set_text(self, text: str = None):
        self._text = text

    def set_color(self, color: str = None):
        self._color = color

    def get_text(self, text: str = None):
        return text

    def get_color(self, color: str = None):
        return color


class LineElement():
    def __init__(self, text_element: Union[TextElement, List[TextElement]] = None) -> None:
        if isinstance(text_element) == list:
            self._text_element_list = text_element
        elif isinstance(text_element) == TextElement:
            self._text_element_list = [text_element]

    def __str__(self) -> str:
        return ''.join([str(text_element) for text_element in self._text_element_list])

    def add_text_element(self, text_element: TextElement):
        self._text_element_list.append(text_element)

# class TableElement():
#     def __init__(self, text_element_list: List[List[TextElement]] = None) -> None:
#         self._text_element_list = text_element_list

#     def __str__(self) -> str:
#         return '\n'.join([str(text_element_list) for text_element_list in self._text_element_list])

#     def add_text_element_list(self, text_element_list: List[TextElement]):
#         self._text_element_list.append(text_element_list)


class Printer():
    def __init__(self, width: int = None, height: int = None, outside_border_width: int = None) -> None:
        self._width = width
        self._height = height
        # 1 = '─', 2 = '━', 3 = '┄', 4 = '┅'
        self._outside_border_width = outside_border_width

        self._line_element_list: List[LineElement] = []

    def add_line_element(self, element: Union[LineElement, TextElement]) -> None:
        if isinstance(element) == TextElement:
            self._line_element_list.append(LineElement(element))
        elif isinstance(element) == LineElement:
            self._line_element_list.append(element)

    def print(self):

        # ─ │ ┌ ┐ ┘ └ ├ ┬ ┤ ┴ ┼ ━ ┃ ┏ ┓ ┛ ┗ ┣ ┳ ┫ ┻ ╋ ┠ ┯ ┨ ┷ ┿ ┝ ┰ ┥ ┸ ╂ ┒ ┑
        # ┚ ┙ ┖ ┕ ┎ ┍ ┞ ┟ ┡ ┢ ┦ ┧ ┩ ┪ ┭ ┮ ┱ ┲ ┵ ┶ ┹ ┺ ┽ ┾ ╀ ╁ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊

        print_element = []
        if self._outside_border_width == 1:
            border = {
                'up_down_side': '─',
                'left_right_side': '│',
                'left_up_corner': '┌',
                'right_up_corner': '┐',
                'left_down_corner': '└',
                'right_down_corner': '┘',
            }
        elif self._outside_border_width == 2:
            border = {
                'up_down_side': '━',
                'left_right_side': '┃',
                'left_up_corner': '┏',
                'right_up_corner': '┓',
                'left_down_corner': '┗',
                'right_down_corner': '┛',
            }
        print_element.append(str(LineElement(TextElement(
            f'''{border["left_up_corner"]}{"":{border["up_down_side"]}{self._width-2}}{border["right_up_corner"]}''', 'yellow'))))

        for line_element in len(self._line_element_list):
            print_element.append(
                f'{border["left_right_side"]}{str(line_element)}{border["left_right_side"]}')
            SOPTEST_LOG_DEBUG('+', end='')


if __name__ == '__main__':
    printer = Printer(width=10, height=10)
    printer.add_line_element(TextElement(text='Hello', color='red'))
    printer.print()
