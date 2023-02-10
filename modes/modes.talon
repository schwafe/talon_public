not mode: user.deep_sleep
-

^dictation mode$:
	user.mouse_set_tertiary_mode()
    user.enter_dictation_mode()
	user.turnOffMouseControl()
	
^command mode$:
	user.enter_command_mode_with_mouse_control()

^parrot mode on$:
	print("enabling parrot mode")
	mode.enable("user.parrot")
	user.show_parrot_on_button()
	
^parrot mode off$:
	print("disabling parrot mode")
	mode.disable("user.parrot")
	user.hide_parrot_buttons()
	
^talon deep sleep$:
    mode.disable("dictation")
    mode.disable("command")
    mode.enable("user.deep_sleep")
	user.show_exit_deep_sleep_button()