from time import sleep, time
import os

from talon import (
    Module,
    actions,
    app,
    clip,
    cron,
    ctrl,
    imgui,
    noise,
    ui,
)
from talon_plugins import eye_mouse, eye_zoom_mouse
from talon_plugins.eye_mouse import config, toggle_camera_overlay

tracking = actions.tracking

scroll_amount = 0
scroll_job = None
gaze_job = None


mod = Module()
setting_mouse_click_duration = mod.setting(
    "mouse_click_duration",
    type=float,
    default=16000,
    desc="The default duration of a click.",
)
setting_hiss_threshold = mod.setting(
    "hiss_threshold",
    type=str,
    default="150ms",
    desc="Threshold for a hiss to count as long.",
)

continuous_scoll_mode = ""
#0 = inactive, 1 = left click, 2 = right click, 3 = exit dictation mode and enter command mode
modus_operandi = 0
running = False
threshold_passed = False

@mod.action_class
class Actions:

    def mouse_set_primary_mode():
        """Set modus_operandi to 1, meaning that a pop sound will click the left mouse button and a hiss will set the modus_operandi to 2"""
        global modus_operandi
        modus_operandi = 1
        
    def mouse_set_tertiary_mode():
        """Set modus_operandi to 3, meaning that a hiss does nothing and a pop sound will enter command mode and modus_operandi 1"""
        global modus_operandi
        modus_operandi = 3
        
    def mouse_drag(button: int):
        """Press and hold/release a specific mouse button for dragging"""
        # Clear any existing drags
        actions.user.mouse_drag_end()

        # Start drag
        ctrl.mouse_click(button=button, down=True)
      
    def mouse_drag_end():
        """ Releases any held mouse buttons """
        buttons_held_down = list(ctrl.mouse_buttons_down())
        for button in buttons_held_down:
            ctrl.mouse_click(button=button, up=True)
            
    def turnOnMouseControl():
        """This enables controlling the mouse."""
        tracking.control_toggle(True)
        #deprecated toggle_control(True)
        
    def turnOffMouseControl():
        """This disables controlling the mouse."""
        tracking.control_toggle(False)
        #deprecated toggle_control(False)


def still_running():
    """If the hiss is still going, a drag motion is started"""
    global threshold_passed
    if running:
        threshold_passed = True
        if modus_operandi == 1:
            #start left drag
            #print('left drag')
            actions.user.mouse_drag(0)
        elif modus_operandi == 2:
            #start right drag
            #print('right drag')
            #toggle_control(not config.control_mouse)
            actions.user.mouse_drag(1)
                
 
def onHiss(active: int):
    """This handles the hiss sound."""
    global modus_operandi, running, threshold_passed
    if modus_operandi != 3:
        if active:
            #print('hiss start')
            #wait and see if it's a long hiss
            if not running:
                running = True
                cron.after(setting_hiss_threshold.get(), still_running)
            else:
                print('prevented double hiss!')
        elif threshold_passed:
            threshold_passed = False
            running = False
            #print('drag end')
            #drag end
            actions.user.mouse_drag_end()
            #if modus_operandi == 2:
                #stop dragging with right click
                #toggle_control(not config.control_mouse)
        else:
            running = False
            #short hiss
            print('hiss end')
            tracking.control_toggle()
            #deprecated toggle_control(not config.control_mouse)
            if modus_operandi == 0 or modus_operandi == 2:
                #print('modus_operandi 1')
                modus_operandi = 1
            elif modus_operandi == 1:
                #print('modus_operandi 2')
                modus_operandi = 2
                
noise.register('hiss', lambda active: onHiss(active))
                    
def onPop(active: int):
    """This handles the pop sound."""
    if modus_operandi == 1:
        ctrl.mouse_click(button=0, hold=setting_mouse_click_duration.get())
    elif modus_operandi == 2:
        ctrl.mouse_click(button=1, hold=setting_mouse_click_duration.get())
    elif modus_operandi == 3:
        actions.user.enter_command_mode()
        actions.user.turnOnMouseControl()
        actions.user.mouse_set_primary_mode()

noise.register('pop', lambda active: onPop(active))