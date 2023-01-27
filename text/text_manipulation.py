from talon import Context, Module, actions

ctx = Context()
mod = Module()
mod.list("direction", desc="list of directions")
ctx.lists["self.direction"] = {
    "left",
    "right",
    "down",
    "up",
}

@mod.action_class
class Actions:
    def select_text( direction: str):
        "A" 
        select_text_and_optionally_delete(False, direction, False)

    def select_text_all_the_way( direction: str):
        "A" 
        select_text_and_optionally_delete(False, direction, True)

    def delete_text( direction: str):
        "A" 
        select_text_and_optionally_delete(True, direction, False)

    def delete_text_all_the_way( direction: str):
        "A" 
        select_text_and_optionally_delete(True, direction, True)

def select_text_and_optionally_delete(delete: bool, direction: str, all_the_way: bool):
    if(direction == "left"):
        if(all_the_way):
            actions.edit.extend_line_start()
        else:
            actions.edit.extend_left()
    elif(direction == "right"):
        if(all_the_way):
            actions.edit.extend_line_end()
        else:
            actions.edit.extend_right()
    elif(direction == "down"):
        if(all_the_way):
            actions.edit.extend_file_end()
        else:
            actions.edit.extend_down()
    elif(direction == "up"):
        if(all_the_way):
            actions.edit.extend_file_start()
        else:
            actions.edit.extend_up()
    else:
        raise ValueError
    
    if(delete):
        actions.edit.delete()