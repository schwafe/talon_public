import itertools
import re
from talon import ctrl, ui, Module, Context, actions, clip

mod = Module()
ctx = Context()
mod.list(
    "target_symbol",
    desc="names for regular expressions for common things to extend to",
)
target_symbols = {
    "parens": r'\((.*?)\)',
    "squares": r'\[(.*?)\]',
    "braces": r'\{(.*?)\}',
    "quotes": r'\"(.*?)\"',
    "angles": r'\<(.*?)\>',
    "single quotes": r'\'(.*?)\''
}
ctx.lists["self.target_symbol"] = target_symbols


@mod.capture(rule="{user.target_symbol}")
def navigation_target(m) -> re.Pattern:
    """A target symbol to extend to. Returns a regular expression."""
    if hasattr(m, 'target_symbol'):
        return re.compile(m.target_symbol)
    return re.compile(re.escape(m.text), re.IGNORECASE)

@mod.action_class
class Actions:

    def extend(descriptor: str, direction: str):
        """extend selection to specified direction until specified symbol"""  
        leftExtend = 0
        leftMatch = None
        
        if descriptor == "PARENS":
            leftSymbol = r"\("
            rightSymbol = r"\)"
        else:
            leftSymbol = ""
            rightSymbol = ""
        
        leftText = get_text_left()
        startIndex = len(leftText)
        
        rightText = get_text_right()
        
        if direction == "LEFT" or direction == "BOTH":
            leftMatch = match_backwards(leftSymbol, 1, leftText)
            if leftMatch != None:
                leftExtend = startIndex-leftMatch.start()
                            
        if direction == "RIGHT" or direction == "BOTH":
            rightMatch = match_forward(rightSymbol, 1, rightText)
                
            
        if leftMatch != None:
            if direction == "LEFT" or rightMatch == None:
                #actions.edit.right()
                for index in range(0,leftExtend):
                    actions.edit.extend_left()
            else:
                for index in range(0,leftExtend):
                    actions.edit.left()
                        
                    
        if rightMatch != None:
            for index in range(0,rightMatch.start() + 1 + leftExtend):
                actions.edit.extend_right()
                
        
def get_text_left():
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_text_right():
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()
    actions.edit.left()
    return text
        
def match_backwards(regex, occurrence_number, subtext):
    try:
        match = list(re.finditer(regex,subtext))[-occurrence_number]
        return match
    except IndexError:
        return


def match_forward(regex, occurrence_number, sub_text):
    try:
        match = next(
            itertools.islice(re.finditer(regex, sub_text), occurrence_number - 1, None)
        )
        return match
    except StopIteration:
        return None
