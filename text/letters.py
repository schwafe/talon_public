from talon import Context, Module

mod = Module()
ctx = Context()
mod.list("letters", desc="list of letters")

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
    'space' : ' ',
}

ctx.lists["self.letters"] = letters_dictionary.keys()

@mod.capture(rule="{self.letters}+")
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

@mod.capture(rule="{self.modifier_key}+ {self.letters}")
def keystroke(m) -> str:
    "One keystroke"
    modifiers= "-".join(m.modifier_key_list)
    return modifiers+"-"+letters_dictionary[m.letters]


@mod.capture(rule="shift {self.letters}")
def uppercase_letter(m) -> str:
    "One uppercase_letter"
    return letters_dictionary[m.letters].upper()

@mod.capture(rule="(<self.uppercase_letter>| {self.letters})+")
def letters_mixed(m) -> str:
    "One or more modifier keys"
    letters =""
    for letter in m:
        if len(letter) > 1:
            #not uppercase
            letters += letters_dictionary[letter]
        else:
            letters += letter

    return letters