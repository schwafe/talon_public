^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
	
	user.unRegSec()
	user.turnOffMouseControl()
	user.regSwitchCommand()
	
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
	
	user.unRegSwitchCommand()
	user.regSec()
	user.turnOnMouseControl()
	
^talon sleep$:
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("sleep")

	user.unRegSec()
	user.turnOffMouseControl()
	user.unRegSwitchCommand()