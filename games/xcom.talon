app: XCOM: Enemy Within
os: windows
-
trap:
  #mouse seems to follow eye movement, but actually does not move
  user.mouse_drag(0)
  sleep(50ms)
  user.mouse_drag_end()