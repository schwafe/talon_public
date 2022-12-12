import itertools
import re
from talon import ctrl, ui, Module, Context, actions, clip

mod = Module()
ctx = Context()

text_navigation_max_line_search = mod.setting(
    "text_navigation_max_line_search",
    type=int,
    default=2,
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

    def extend(descriptor: str, direction: str):
        """extend selection to specified direction until before the specified symbol"""  
        lengthLeftText=0
        lineCursorPosition=None

        if direction == "LEFT" or direction=="BOTH":
            selection_clear()
            #saving the position in the current line
            extend_line_start()
            lineCursorPosition=len(actions.edit.selected_text())

            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.extend_up()
            
            lengthLeftText=len( actions.edit.selected_text())
            actions.edit.left()
            
            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.extend_down()

            extend_to_column(lineCursorPosition)
                
        if direction == "RIGHT" or direction=="BOTH":
            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.extend_down()
            actions.edit.extend_line_end()

        text = actions.edit.selected_text()        
        
        if direction == "LEFT": 
            actions.edit.right()
        if direction == "RIGHT" :
            actions.edit.left()
        if direction=="BOTH":
            actions.edit.left()
            for index in range(0, text_navigation_max_line_search.get()):
                actions.edit.down()
            jump_column(lineCursorPosition)

        leftSymbolPattern = re.compile(r"\(")
        rightSymbolPattern = re.compile(r"\)")

        leftExtend=0
        rightExtend=0

        leftMatch=None
        rightMatch=None

        #TODO extending to the left or both clears the original selection, but extending to the right does not!
        
        if direction == "LEFT" or direction == "BOTH":
            print("searching for left match!")
            reversedLeftText=text[lengthLeftText-1::-1]
            leftMatch = match_forward(leftSymbolPattern,1,reversedLeftText)
            print(leftMatch)
            
            if leftMatch != None:
                counterText = reversedLeftText[:leftMatch.end()]
                offset=leftMatch.end()
                subText= reversedLeftText[offset:]

                counterMatchCount= count_matches(rightSymbolPattern, counterText) 
                print(counterMatchCount) 
                print(counterText)

                while(leftMatch != None and counterMatchCount !=0):
                    leftMatch = match_forward(leftSymbolPattern,counterMatchCount,subText)
                    print(leftMatch)
                
                    if leftMatch != None:
                        counterText = reversedLeftText[offset:offset+leftMatch.end()]
                        offset+=leftMatch.end()
                        subText= reversedLeftText[offset:]

                        counterMatchCount= count_matches(rightSymbolPattern, counterText) 
                        print(counterMatchCount) 
                        print(counterText)

                if leftMatch != None:
                    leftExtend=offset-1

        if direction == "RIGHT" or direction == "BOTH":
            print("searching for right match!")
            rightText=text[lengthLeftText:]
            rightMatch = match_forward(rightSymbolPattern,1,rightText)
            print(rightMatch)
            
            if rightMatch != None:
                counterText = rightText[:rightMatch.end()]
                offset=rightMatch.end()
                subText= rightText[offset:]

                counterMatchCount= count_matches(leftSymbolPattern, counterText) 
                print(counterMatchCount) 
                print(counterText)

                while(rightMatch != None and counterMatchCount != 0):
                    rightMatch = match_forward(rightSymbolPattern,counterMatchCount,subText) 
                    print(rightMatch)
                
                    if rightMatch != None:
                        counterText = rightText[offset:offset+rightMatch.end()]
                        offset+=rightMatch.end()
                        subText= rightText[offset:]

                        counterMatchCount= count_matches(leftSymbolPattern, counterText) 
                        print(counterMatchCount) 
                        print(counterText)
            

                if rightMatch != None:
                    rightExtend=offset-1

        if leftMatch!=None:
            for index in range(0,leftExtend):
                actions.edit.left()
            for index in range(0,leftExtend):
                actions.edit.extend_right()
        
        if rightMatch != None:
            for index in range(0,rightExtend):
                actions.edit.extend_right()                

        #correct cursor position;TODO why?
        #if direction == "BOTH" and (leftMatch!=None or rightMatch!= None):
         #   actions.edit.extend_left()                
        
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

def match_backwards(regex, occurrence_number, text):
    try:
        match = list(regex.finditer(text))[-occurrence_number]
        return match
    except IndexError:
        return

def count_matches(regex,text):
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
        og_selection_size = len(actions.edit.selected_text())

        actions.edit.extend_left()
        new_selection_size = len(actions.edit.selected_text())

        #return selection to original state
        actions.edit.extend_right()

        if(new_selection_size==1):
            #special case; og_selection might contain the whole line (which could be of an arbitrary size)
            actions.edit.extend_left()
            actions.edit.extend_left()
            actions.edit.extend_left()
            third_test_selection_size = len(actions.edit.selected_text())

            #return selection to original state
            actions.edit.extend_right()
            actions.edit.extend_right()
            actions.edit.extend_right()

            assert(third_test_selection_size==1 or third_test_selection_size==3)

            if(third_test_selection_size==1):
                #selection started from the left
                return -1
            else:
                #nothing is selected -> no actions necessary
                return 0
        elif(og_selection_size==1):
            #special case; new_selection might contain the whole line (which could be of an arbitrary size)
            actions.edit.extend_left()
            actions.edit.extend_left()
            third_test_selection_size = len(actions.edit.selected_text())

            #return selection to original state
            actions.edit.extend_right()
            actions.edit.extend_right()

            if(third_test_selection_size==1):
                #selection started from the left
                return -1
            else:
                #selection started from the right
                return 1

        elif(og_selection_size> new_selection_size):
            #selection started from the left
            return -1
        elif(new_selection_size> og_selection_size):
            #selection started from the right
            return 1


def is_start_of_line():
    direction = determine_selection_direction()

    if(direction == -1):
        selection = actions.edit.selected_text()
        return selection[len(selection)-1]=='\n'
    elif(direction == 0 or direction == 1):
        actions.edit.extend_left()
        selection = actions.edit.selected_text()
        actions.edit.extend_right()
        return selection[0]=='\n'
    else:
        raise ValueError("direction invalid: %d" %direction)

def extend_line_start():
    actions.edit.extend_line_start()
    if(not is_start_of_line()):
        actions.edit.extend_line_start()

def line_start():
    actions.edit.line_start()
    if(not is_start_of_line()):
        actions.edit.line_start()


def jump_column(column: int):
    """moves the cursor to the given column"""  
    line_start()
    if(not is_start_of_line()):
        line_start()
    
    for index in range(0, column):
        actions.edit.right()

def extend_to_column(column: int):
    """extends the selection to the given column (from the left)"""  
    #correcting cursor position before extending the selection in the current line; doing this twice to also include whitespace
    extend_line_start()

    for index in range(0, column):
        actions.edit.extend_right()

def selection_clear():
    direction = determine_selection_direction()

    if(direction == -1):
        actions.edit.left()
    elif(direction == 0):
        #nothing is selected -> no actions necessary
        return
    elif(direction == 1):
        actions.edit.right()
    else:
        raise ValueError("direction invalid: %d" %direction)