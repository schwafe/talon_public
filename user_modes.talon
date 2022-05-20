not mode: user.deep_sleep
-
^parrot mode$:
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