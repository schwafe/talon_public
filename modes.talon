not mode: sleep
-
^dictation mode$:
    user.enter_dictation_mode()
	
^command mode$:
	user.enter_command_mode()
	
^talon sleep$:
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("sleep")