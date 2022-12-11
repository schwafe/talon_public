import itertools
import re
from talon import ctrl, ui, Module, Context, actions, clip

mod = Module()
ctx = Context()

text_navigation_max_line_search = mod.setting(
    "text_navigation_max_line_search",
    type=int,
    default=10,
    desc="the maximum number of rows that will be included in the search for the keywords above and below in <user direction>",
)

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

    def test():
        """moves the cursor to the given column"""  
        rightSymbol = r"\)"
        rightText = get_text_down(5)
        #for index in range(0,5):
            #rightMatch = match_forward(rightSymbol,rightText)

    def jump_column(column: int):
        """moves the cursor to the given column"""  
        actions.edit.line_start()
        for index in range(0, column):
            actions.edit.right()

    def extra(descriptor: str, direction: str):
        """extend selection to specified direction until before the specified symbol"""  
        lengthLeftText=0
        lineCursorPosition=None

        if direction == "LEFT" or direction=="BOTH":
            if actions.edit.selected_text()!=None:
                #clearing selection without moving the cursor
                actions.edit.left()
                actions.edit.right()
            #saving the position in the current line; doing this twice to also include tabs
            actions.edit.extend_line_start()
            actions.edit.extend_line_start()
            lineCursorPosition=len(actions.edit.selected_text())

            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.extend_up()
            actions.edit.extend_line_start()
            lengthLeftText=len( actions.edit.selected_text())
            actions.edit.left()
            
            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.extend_down()

            #correcting cursor position before extending the selection in the current line; doing this twice to also include tabs
            actions.edit.extend_line_start()
            actions.edit.extend_line_start()

            for index in range(0, lineCursorPosition):
                actions.edit.extend_right()
                
        if direction == "RIGHT" or direction=="BOTH":
            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.extend_down()
            actions.edit.extend_line_end()

        text = actions.edit.selected_text()
        #actions.edit.select_none() moves the cursor to the end of the selection, but actions.edit.left() only clears the selection
        actions.edit.left()

        leftSymbol = r"\("
        rightSymbol = r"\)"

        leftExtend=0
        rightExtend=0

        leftMatch=None
        rightMatch=None

        #TODO amount of countermatches has to be saved for both ways, otherwise on the left '())' and on the right '(()' will not work!
        #TODO on LEFT, the resulting match seemed correct, but the resulting selection and cursor movement seemed way off (and offset to the top)
        
        if direction == "LEFT" or direction == "BOTH":
            reversedLeftText=text[lengthLeftText::-1]
            leftMatch = match_forward(leftSymbol,reversedLeftText)
            print(reversedLeftText)
            
            if leftMatch != None:
                counterText = reversedLeftText[:leftMatch.end()]
                offset=leftMatch.end()
                subText= reversedLeftText[offset:]

                counterMatch = match_forward(rightSymbol, counterText) 
                print(reversedLeftText)
                print(counterText)
                print(leftMatch)
                print(counterMatch)
                print(subText)
                

                while(leftMatch != None and counterMatch != None):
                    leftMatch = match_forward(leftSymbol,subText) 
                    print(leftMatch)
                
                    if leftMatch != None:
                        counterText = reversedLeftText[offset:offset+leftMatch.end()]
                        offset+=leftMatch.end()
                        subText= reversedLeftText[offset:]

                        counterMatch = match_forward(rightSymbol, counterText)
                        print(counterMatch) 
                        print(counterText)

                if leftMatch != None:
                    leftExtend=offset

        if direction == "RIGHT" or direction == "BOTH":
            rightText=text[lengthLeftText:]
            rightMatch = match_forward(rightSymbol,rightText)
            
            if rightMatch != None:
                counterText = rightText[:rightMatch.end()]
                offset=rightMatch.end()
                subText= rightText[offset:]

                counterMatch = match_forward(leftSymbol, counterText) 
                print(rightText)
                print(counterText)
                print(rightMatch)
                print(counterMatch)
                print(subText)
                

                while(rightMatch != None and counterMatch != None):
                    rightMatch = match_forward(rightSymbol,subText) 
                    print(rightMatch)
                
                    if rightMatch != None:
                        counterText = rightText[offset:offset+rightMatch.end()]
                        offset+=rightMatch.end()
                        subText= rightText[offset:]

                        counterMatch = match_forward(leftSymbol, counterText)
                        print(counterMatch) 
                        print(counterText)
            

                if rightMatch != None:
                    rightExtend=offset

        if leftMatch!=None:
            for index in range(0,leftExtend):
                actions.edit.left()
            for index in range(0,leftExtend):
                actions.edit.extend_right()
        
        if rightMatch != None:
            for index in range(0,rightExtend):
                actions.edit.extend_right()

        if leftMatch==None and rightMatch==None and lineCursorPosition!=None:
            #corrects the cursor position if necessary
            for index in range(0,lineCursorPosition):
                actions.edit.right()
                
        
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

    
def get_text_up():
    actions.edit.up()
    actions.edit.line_end()
    for j in range(0, text_navigation_max_line_search.get()):
        actions.edit.extend_up()
    actions.edit.extend_line_start()
    text = actions.edit.selected_text()
    actions.edit.right()
    return text


def get_cursor_position():
    #   TODO don't clear selection
    actions.edit.select_none()
    actions.edit.extend_line_start()
    cursorPosition =len(actions.edit.selected_text())
    actions.user.jump_column(cursorPosition)
    return cursorPosition

#get the rest of the line (past the cursor) and the next maxLines lines
def get_text_down(maxLines):    
    for j in range(0, maxLines):
        actions.edit.extend_down()
    actions.edit.extend_line_end()
    text = actions.edit.selected_text()

    return text

def match_forward(regex:str, text:str):
    return re.search(regex,text)

def match_backwards(regex:str, text:str):
    reversedText=text[::-1]
    return re.search(regex,reversedText)
#def match_backwards(regex, occurrence_number, subtext):
#    try:
#        match = list(re.finditer(regex,subtext))[-occurrence_number]
#        return match
#    except IndexError:
#        return

#def match_forward(regex, occurrence_number, sub_text):
#        """moves the cursor to the given column"""  
 #       try:
 #           match = next(
  #              itertools.islice(re.finditer(regex, sub_text), occurrence_number - 1, None)
   #         )
    #        return match
     #   except StopIteration:
      #      return None

