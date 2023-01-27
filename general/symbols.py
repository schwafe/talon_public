from talon import Context, Module

mod = Module()
ctx = Context()
mod.list("symbols", desc="list of symbols")

symbols_dictionary = {
    "amper": "&",
    "arrow": "->",
    "at sign": "@",
    'backslash':'\\',
    "bang": "!",
    "caret": "^",
    'coma':',',
    'comma':',',
    'colon':':',
    'dot':'.',
    'double quote':'\"\"',
    'down score':'_',
    'enter':'\n',
    "equals": "=",
    "greater than": ">",
    'hash':'#',
    "left angle": "<",
    'left brace':'{',
    'left paren':'(',
    'left square':'[',
    "less than": "<",
    'minus':'-',
    "percent": "%",
    "pipe": "|",
    "plus": "+",
    'question':'?',
    "right angle": ">",
    'right brace':'}',
    'right paren':')',
    'right square':']',
    'semi':';',
    'single quote':'\'\'',
    'slash':'/',
    'space':' ',
    "star": "*",
    "tilde": "~",
    "underscore": "_",
    # Currencies
    "dollar": "$",
    "pound": "£",
    "euro": "€",
}

ctx.lists["self.symbols"] = symbols_dictionary.keys()

@mod.capture(rule="{self.symbols}")
def symbols(m) -> int:
    """Returns a single symbol"""
    return symbols_dictionary[m[0]]