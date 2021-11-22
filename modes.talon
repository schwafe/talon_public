mode: all
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
	
	user.unRegAlt()
	user.unRegPrim()
	user.turnOffMouseControl()
	user.regSwitchCommand()
	
^command mode$:
	user.enter_command_mode(0)
	
^talon sleep$:
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("sleep")