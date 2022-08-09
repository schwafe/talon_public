os: windows
and app.name: ck3.exe
-
map closeup:
 user.mouse_scroll_up()
 user.mouse_scroll_up()
 user.mouse_scroll_up()
 user.mouse_scroll_up()
 user.mouse_scroll_up()
 
map overview:
 user.mouse_scroll_down()
 user.mouse_scroll_down()
 user.mouse_scroll_down()
 user.mouse_scroll_down()
 user.mouse_scroll_down()
 
parrot(posterior_click):
	print("posterior_click")
	user.mouse_toggle_gaze_scroll()