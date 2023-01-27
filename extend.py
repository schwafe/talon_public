import itertools
import re
from talon import Module, Context, actions

mod = Module()
ctx = Context()

text_navigation_max_line_search = mod.setting(
    "text_navigation_max_line_search",
    type=int,
    default=1,
    desc="the maximum number of rows that will be included in the search for the keywords above and below in <user direction>",
)
mod.list(
    "extend_symbol_names",
    desc="names for common things to extend to",
)

ctx.lists["user.extend_symbol_names"] = [
    "parens",
    "squares",
    "braces",
    "quotes",
    "angles",
    "single quotes",
]

mod.list(
    "extend_symbol_left",
    desc="names for regular expressions for common things to extend to",
)
ctx.lists["user.extend_symbol_left"] = {
    "parens": r'\(',
    "squares": r'\[',
    "braces": r'\{',
    "quotes": r'\"',
    "angles": r'\<',
    "single quotes": r'\'',
}

mod.list(
    "extend_symbol_right",
    desc="names for regular expressions for common things to extend to",
)
ctx.lists["user.extend_symbol_right"] = {
    "parens": r'\)',
    "squares": r'\]',
    "braces": r'\}',
    "quotes": r'\"',
    "angles": r'\>',
    "single quotes": r'\'',
}

mod.list(
    "extend_direction",
    desc="directions for extending",
)

ctx.lists["user.extend_direction"] = [
    "left",
    "right",
]


@mod.action_class
class Actions:

    #TODO quotes and single quotes do not work yet
    def extend(symbol_name: str, direction: str):
        """extend selection to specified direction until before the specified symbol"""
        patternleft = re.compile(
            ctx.lists["user.extend_symbol_left"][symbol_name], re.IGNORECASE)
        patternright = re.compile(
            ctx.lists["user.extend_symbol_right"][symbol_name], re.IGNORECASE)
        extendInternal(patternleft, patternright, direction)


def extendInternal(leftSymbolPattern: re.Pattern, rightSymbolPattern: re.Pattern, direction: str):
    """extend selection to specified direction until before the specified symbol"""
    lengthleftText = 0
    lineCursorPosition = None

    # getting relevant text
    if direction == "left" or direction == "both":
        selection_clear()
        # saving the position in the current line
        extend_line_start()
        lineCursorPosition = len(actions.edit.selected_text())

        for index in range(0, text_navigation_max_line_search.get()):
            actions.edit.extend_up()

        lengthleftText = len(actions.edit.selected_text())
        actions.edit.left()

        for index in range(0, text_navigation_max_line_search.get()):
            actions.edit.extend_down()

        extend_to_column(lineCursorPosition)

    if direction == "right" or direction == "both":
        for index in range(0, text_navigation_max_line_search.get()):
            actions.edit.extend_down()
        actions.edit.extend_line_end()

    text = actions.edit.selected_text()

    if direction == "left":
        actions.edit.right()
    if direction == "right":
        actions.edit.left()
    if direction == "both":
        actions.edit.left()
        for index in range(0, text_navigation_max_line_search.get()):
            actions.edit.down()
        jump_column(lineCursorPosition)

    leftExtend = 0
    rightExtend = 0

    leftMatch = None
    rightMatch = None

    # TODO extending to the left or both clears the original selection, but extending to the right does not!

    if direction == "left" or direction == "both":
        # print("searching for left match!")
        reversedleftText = text[lengthleftText-1::-1]
        leftMatch = match_forward(leftSymbolPattern, 1, reversedleftText)
        # print(leftMatch)

        if leftMatch != None:
            counterText = reversedleftText[:leftMatch.end()]
            offset = leftMatch.end()
            subText = reversedleftText[offset:]

            counterMatchCount = count_matches(
                rightSymbolPattern, counterText)
            # print(counterMatchCount)
            # print(counterText)

            while (leftMatch != None and counterMatchCount != 0):
                leftMatch = match_forward(
                    leftSymbolPattern, counterMatchCount, subText)
                # print(leftMatch)

                if leftMatch != None:
                    counterText = reversedleftText[offset:offset +
                                                   leftMatch.end()]
                    offset += leftMatch.end()
                    subText = reversedleftText[offset:]

                    counterMatchCount = count_matches(
                        rightSymbolPattern, counterText)
                    # print(counterMatchCount)
                    # print(counterText)

            if leftMatch != None:
                leftExtend = offset-1

    if direction == "right" or direction == "both":
        # print("searching for right match!")
        rightText = text[lengthleftText:]
        rightMatch = match_forward(rightSymbolPattern, 1, rightText)
        # print(rightMatch)

        if rightMatch != None:
            counterText = rightText[:rightMatch.end()]
            offset = rightMatch.end()
            subText = rightText[offset:]

            counterMatchCount = count_matches(
                leftSymbolPattern, counterText)
            # print(counterMatchCount)
            # print(counterText)

            while (rightMatch != None and counterMatchCount != 0):
                rightMatch = match_forward(
                    rightSymbolPattern, counterMatchCount, subText)
                # print(rightMatch)

                if rightMatch != None:
                    counterText = rightText[offset:offset+rightMatch.end()]
                    offset += rightMatch.end()
                    subText = rightText[offset:]

                    counterMatchCount = count_matches(
                        leftSymbolPattern, counterText)
                    # print(counterMatchCount)
                    # print(counterText)

            if rightMatch != None:
                rightExtend = offset-1

    if leftMatch != None:
        for index in range(0, leftExtend):
            actions.edit.left()
        for index in range(0, leftExtend):
            actions.edit.extend_right()

    if rightMatch != None:
        for index in range(0, rightExtend):
            actions.edit.extend_right()


def get_text_left():
    extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_right():
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text


def get_text_up():
    actions.edit.up()
    actions.edit.line_end()
    for j in range(0, text_navigation_max_line_search.get()):
        actions.edit.extend_up()
    extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_cursor_position():
    #   TODO don't clear selection
    actions.edit.select_none()
    extend_line_start()
    cursorPosition = len(actions.edit.selected_text())
    actions.user.jump_column(cursorPosition)
    return cursorPosition

# get the rest of the line (past the cursor) and the next maxLines lines


def get_text_down(maxLines):
    for j in range(0, maxLines):
        actions.edit.extend_down()
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()

    return text


def match_backwards(regex, occurrence_number, text):
    try:
        match = list(regex.finditer(text))[-occurrence_number]
        return match
    except IndexError:
        return


def count_matches(regex, text):
    return len(regex.findall(text))


def match_forward(regex, occurrence_number, text):
    try:
        match = next(
            itertools.islice(regex.finditer(text), occurrence_number - 1, None)
        )
        return match
    except StopIteration:
        return None


def determine_selection_direction():
    selection_shift = 0
    og_selection_size = len(actions.edit.selected_text())

    actions.edit.extend_left()
    selection_shift -= 1
    new_selection_size = len(actions.edit.selected_text())

    if (new_selection_size == 1):
        # special case; og_selection might contain the whole line (which could be of an arbitrary size)
        actions.user.extend_left(2)
        selection_shift -= 2
        third_test_selection = actions.edit.selected_text()
        third_test_selection_size = len(third_test_selection)

        # TODO handle+ special case better? can't use operating system alone, but maybe in combination with WSL?("paths.c - eda (Workspace) [WSL: Ubuntu] - Visual Studio Code")
        # special case when files only use LF as line break, instead of CRLF (selection size = 2)
        assert (third_test_selection_size == 1 or third_test_selection_size == 3 or (third_test_selection_size ==
                2 and third_test_selection.endswith("\n") and not third_test_selection.endswith("\r\n")))

        extend_left_or_right(-selection_shift)
        if (third_test_selection_size == 1):
            # selection started from the left
            return -1
        else:
            # nothing is selected -> no actions necessary
            return 0
    elif (og_selection_size == 1):
        # special case; new_selection might contain the whole line (which could be of an arbitrary size)
        actions.user.extend_left(1)
        selection_shift -= 1
        third_test_selection_size = len(actions.edit.selected_text())

        extend_left_or_right(-selection_shift)
        if (third_test_selection_size == 1):
            # selection started from the left
            return -1
        else:
            # selection started from the right
            return 1

    elif (og_selection_size > new_selection_size):
        # selection started from the left
        extend_left_or_right(-selection_shift)
        return -1
    elif (new_selection_size > og_selection_size):
        # selection started from the right
        extend_left_or_right(-selection_shift)
        return 1


def is_start_of_line():
    direction = determine_selection_direction()

    if (direction == -1):
        selection = actions.edit.selected_text()
        return selection[len(selection)-1] == '\n'
    elif (direction == 0 or direction == 1):
        actions.edit.extend_left()
        selection = actions.edit.selected_text()
        actions.edit.extend_right()
        return selection[0] == '\n'
    else:
        raise ValueError("direction invalid: %d" % direction)


def extend_line_start():
    actions.edit.extend_line_start()
    if (not is_start_of_line()):
        actions.edit.extend_line_start()


def line_start():
    actions.edit.line_start()
    if (not is_start_of_line()):
        actions.edit.line_start()


def jump_column(column: int):
    """moves the cursor to the given column"""
    line_start()
    if (not is_start_of_line()):
        line_start()

    for index in range(0, column):
        actions.edit.right()

def extend_left_or_right(left_or_right_value: int):
    "extends left or right depending on the value! - values for left, + for right, 0 = nothing"
    if(left_or_right_value < 0):
        actions.user.extend_left(-left_or_right_value)
    elif(left_or_right_value > 0):
        actions.user.extend_right(left_or_right_value)

def extend_to_column(column: int):
    """extends the selection to the given column (from the left)"""
    # correcting cursor position before extending the selection in the current line; doing this twice to also include whitespace
    extend_line_start()

    for index in range(0, column):
        actions.edit.extend_right()


def selection_clear():
    direction = determine_selection_direction()

    if (direction == -1):
        actions.edit.left()
    elif (direction == 0):
        # nothing is selected -> no actions necessary
        return
    elif (direction == 1):
        actions.edit.right()
    else:
        raise ValueError("direction invalid: %d" % direction)
