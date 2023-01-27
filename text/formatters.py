import logging
import re
from typing import Union

from talon import Context, Module, actions
from talon.grammar import Phrase

ctx = Context()

words_to_keep_lowercase = (
    "a an the at by for in is of on to up and as but or nor".split()
)

# Internally, a formatter is a pair (sep, fn).
#
# - sep: a boolean, true iff the formatter should leave spaces between words.
#   We use SEP & NOSEP for this for clarity.
#
# - fn: a function (i, word, is_end) --> formatted_word, called on each `word`.
#   `i` is the word's index in the list, and `is_end` is True iff it's the
#   last word in the list.
SEP = True
NOSEP = False

# Formatter helpers
def surround(by):
    return lambda i, word, last: (by if i == 0 else "") + word + (by if last else "")


def words_with_joiner(joiner):
    """Pass through words unchanged, but add a separator between them."""
    return (NOSEP, lambda i, word, _: ("" if i == 0 else joiner) + word)


def first_vs_rest(first_func, rest_func=lambda w: w):
    """Supply one or two transformer functions for the first and rest of
    words respectively.

    Leave second argument out if you want all but the first word to be passed
    through unchanged.
    Set first argument to None if you want the first word to be passed
    through unchanged.
    """
    first_func = first_func or (lambda w: w)
    return lambda i, word, _: first_func(word) if i == 0 else rest_func(word)


def every_word(word_func):
    """Apply one function to every word."""
    return lambda i, word, _: word_func(word)


formatters_dict = {
    "NOOP": (SEP, lambda i, word, _: word),
    "DOUBLE_UNDERSCORE": (NOSEP, first_vs_rest(lambda w: f"__{w}__")),
    "PRIVATE_CAMEL_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w.lower(), lambda w: w.capitalize()),
    ),
    "PROTECTED_CAMEL_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w.lower(), lambda w: w.capitalize()),
    ),
    "PUBLIC_CAMEL_CASE": (NOSEP, every_word(lambda w: w.capitalize())),
    "SNAKE_CASE": (
        NOSEP,
        first_vs_rest(lambda w: w.lower(), lambda w: "_" + w.lower()),
    ),
    "NO_SPACES": (NOSEP, every_word(lambda w: w)),
    "DASH_SEPARATED": words_with_joiner("-"),
    "TERMINAL_DASH_SEPARATED": (
        NOSEP,
        first_vs_rest(lambda w: " --" + w.lower(), lambda w: "-" + w.lower()),
    ),
    "DOUBLE_COLON_SEPARATED": words_with_joiner("::"),
    "ALL_CAPS": (SEP, every_word(lambda w: w.upper())),
    "ALL_LOWERCASE": (SEP, every_word(lambda w: w.lower())),
    "DOUBLE_QUOTED_STRING": (SEP, surround('"')),
    "SINGLE_QUOTED_STRING": (SEP, surround("'")),
    "SPACE_SURROUNDED_STRING": (SEP, surround(" ")),
    "DOT_SEPARATED": words_with_joiner("."),
    "DOT_SNAKE": (NOSEP, lambda i, word, _: "." + word if i == 0 else "_" + word),
    "SLASH_SEPARATED": (NOSEP, every_word(lambda w: "/" + w)),
    "CAPITALIZE_FIRST_WORD": (SEP, first_vs_rest(lambda w: w.capitalize())),
    "CAPITALIZE_ALL_WORDS": (
        SEP,
        lambda i, word, _: word.capitalize()
        if i == 0 or word not in words_to_keep_lowercase
        else word,
    ),
}

# This is the mapping from spoken phrases to formatters
formatters_words = {
    "all cap": formatters_dict["ALL_CAPS"],
    #"all down": formatters_dict["ALL_LOWERCASE"],
    "camel": formatters_dict["PRIVATE_CAMEL_CASE"],
    "dotted": formatters_dict["DOT_SEPARATED"],
    "hammer": formatters_dict["PUBLIC_CAMEL_CASE"],
    "kebab": formatters_dict["DASH_SEPARATED"],
    #"packed": formatters_dict["DOUBLE_COLON_SEPARATED"],
    "pascal": formatters_dict["PUBLIC_CAMEL_CASE"],
    "sentence": formatters_dict["CAPITALIZE_FIRST_WORD"],
    #slasher": formatters_dict["SLASH_SEPARATED"],
    "smash": formatters_dict["NO_SPACES"],
    "snake": formatters_dict["SNAKE_CASE"],
    #"string": formatters_dict["SINGLE_QUOTED_STRING"],
    "title": formatters_dict["CAPITALIZE_ALL_WORDS"],
}

mod = Module()
mod.list("formatters", desc="list of formatters")
ctx.lists["self.formatters"] = formatters_words.keys()

@mod.capture(rule="{self.formatters}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m.formatters_list)

@mod.capture(rule="<phrase>+")
def text(m) -> list[str]:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    words = []
    
    for phrase in m.phrase_list:
        words.extend(
            actions.dictate.replace_words(actions.dictate.parse_words(phrase))
        )
    return words


@mod.action_class
class Actions:
    
    def insert_formatted(formatters: str,text: list[str]):
        "Formats the text and returns a string"
        actions.insert(format_text(formatters.split(","),text))

    def insert_unformatted(text: list[str]):
        "Formats the text and returns a string"
        actions.insert(" ".join(text))


def format_text(formatters: list[str],word_list: list[str]):
    words = []
    separator_to_use = " "

    if(len(formatters) == 1 and formatters[0] == ""):
        formatters= []
    for i, word in enumerate(word_list):
        for name in reversed(formatters):
            does_formatter_use_separator, formatter_function = formatters_words[name]
            word = formatter_function(i, word, i == len(word_list) - 1)
            if not does_formatter_use_separator:
                separator_to_use = ""
        words.append(word)
    return separator_to_use.join(words)