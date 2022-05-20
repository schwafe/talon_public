mode: user.parrot
-
parrot(cluck):
	print("cluck")
	
parrot(closed-mouth cluck):
	mouse_click(0)
	mouse_click(0)
	print("closed-mouth cluck")
	
parrot(frontal_click):
	print("frontal_click") 

parrot(posterior_click):
	print("posterior_click")
	user.mouse_toggle_gaze_scroll()
	
parrot(high_whistle):
	print("high_whistle")

parrot(low_whistle):
	print("low_whistle")
	
parrot(hiss):
	print("hiss")

parrot(pop):
	print("pop")
