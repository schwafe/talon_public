not mode: sleep
-
^parrot mode$:
	print("enabling parrot mode")
	mode.enable("user.parrot")
	user.show_parrot_on_button()

^dictation mode$:
    user.enter_dictation_mode()
	
^command mode$:
	user.enter_command_mode()
	
^talon sleep$:
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("sleep")