from talon import Context, Module

mod = Module()
ctx = Context()
mod.list("letter", desc="list of letter names")

letters_dictionary = {
    'air' : 'a',
    'bat' : 'b',
    'cap' : 'c',
    'drum' : 'd',
    'each' : 'e',
    'fine' : 'f',
    'gust' : 'g',
    'harp' : 'h',
    'ice' : 'i',
    'jury' : 'j',
    'king' : 'k',
    'look' : 'l',
    'made' : 'm',
    'near' : 'n',
    'odd' : 'o',
    'pit' : 'p',
    'quench' : 'q',
    'red' : 'r',
    'sun' : 's',
    'trap' : 't',
    'urge' : 'u',
    'vest' : 'v',
    'whale' : 'w',
    'plex' : 'x',
    'yank' : 'y',
    'zip' : 'z',
}

ctx.lists["self.letter"] = letters_dictionary

@mod.capture(rule="{self.letter}+")
def letters_all_caps(m) -> int:
    """Returns a single symbol"""
    return "".join([letters_dictionary[letter] for letter in m.letters_list]).upper()

mod.list("modifier_key", desc="All modifier keys")
modifier_keys = {
    'alt': 'alt',  
    'alter': 'alt',
    'control': 'ctrl',
    'shift': 'shift',
    'super': 'super',
}

ctx.lists["self.modifier_key"] = modifier_keys

mod.list("punctuation_symbol", desc="space, period and comma")
punctuation_symbols = {
    'comma': ',',  
    'coma': ',',  
    'dot': '.',
    'period': '.',
    'space': ' ',
}

ctx.lists["self.punctuation_symbol"] = punctuation_symbols
    
@mod.capture(rule="shift {self.letter}")
def uppercase_letter(m) -> str:
    "One uppercase letter"
    return m.letter.upper()
    
@mod.capture(rule="<self.uppercase_letter>|{self.letter}")
def mixedcase_letter(m) -> str:
    "One letter, either upper- or lowercase"
    return m[0]

@mod.capture(rule="<self.mixedcase_letter>|{self.punctuation_symbol}")
def letter_or_symbol(m) -> str:
    "One letter or symbol"
    return m[0]