say [<user.formatters>] <user.text>$: user.insert_formatted(user.formatters or "", user.text)

#lsay <user.text>$: user.insert_unformatted(user.text)

num <user.number_string>: "{number_string}"

ship <user.letter_or_symbol>+$: user.insert_formatted("hammer",user.letter_or_symbol_list)
letters <user.letter_or_symbol>+$: user.insert_formatted("smash", user.letter_or_symbol_list)
keystroke <user.keystroke>$: key(keystroke)

cut that:
    edit.cut()

copy that:
    edit.copy()

clear {user.direction}:
    user.delete_text(user.direction)

clear way {user.direction}:
    user.delete_text_all_the_way(user.direction)

select {user.direction}:
    user.select_text(user.direction)

select way {user.direction}:
    user.select_text_all_the_way(user.direction)

clear line:
    edit.delete_line()

clear word left:
    edit.select_none()
    edit.extend_word_left()
    edit.delete()

clear word:
    edit.delete_word()

clear word right:
    edit.select_none()
    edit.extend_word_right()
    edit.delete()

copy line:
    edit.select_line() 
    edit.copy()   

escape:
    key(escape)

find that:
    edit.find(edit.selected_text())

file save:
    edit.save()

go down:
    edit.down()

go up:
    edit.up()

go left:
    edit.left()

go right:
    edit.right()

indent less:
    edit.indent_less()

indent more:
    edit.indent_more()

paste match: edit.paste_match_style()

paste that:
    edit.paste()

redo that:
    edit.redo()

select all:
    edit.select_all()

slap:
    edit.line_insert_down()

undo that:
    edit.undo()