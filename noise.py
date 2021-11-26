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
from talon_plugins.eye_mouse import config, toggle_camera_overlay, toggle_control

scroll_amount = 0
click_job = None
scroll_job = None
gaze_job = None


mod = Module()
mod.list(
    "mouse_button", desc="List of mouse button words to mouse_click index parameter"
)
setting_mouse_continuous_scroll_amount = mod.setting(
    "mouse_continuous_scroll_amount",
    type=int,
    default=80,
    desc="The default amount used when scrolling continuously",
)
setting_mouse_wheel_down_amount = mod.setting(
    "mouse_wheel_down_amount",
    type=int,
    default=120,
    desc="The amount to scroll up/down (equivalent to mouse wheel on Windows by default)",
)
setting_mouse_wheel_horizontal_amount = mod.setting(
    "mouse_wheel_horizontal_amount",
    type=int,
    default=40,
    desc="The amount to scroll left/right",
)
setting_mouse_click_duration = mod.setting(
    "mouse_click_duration",
    type=float,
    default=16000,
    desc="The default duration of a click.",
)

continuous_scoll_mode = ""

start = 0
running = False
noise_length_threshold = "150ms"
threshold_passed = False
secondary_mode = False

@mod.action_class
class MouseActions:
    def still_running():
        """If the hiss is still going, a drag motion is started"""
        global running
        global threshold_passed
        global secondary_mode
        if running:
            threshold_passed = True
            if(secondary_mode):
                MouseActions.mouse_drag(1)
            else:
                MouseActions.mouse_drag(0)
 
    def mouse_secondary_mode(is_active: int):
        """This mode is used for stopping the mouse and right clicking."""
        global start
        global running
        global threshold_passed
        global secondary_mode
        
        if is_active:
            print('hiss start')
            start = time()
            running = True
            if not config.control_mouse:
                #start dragging with right click
                toggle_control(not config.control_mouse)
            cron.after(noise_length_threshold, MouseActions.still_running)
        else:
            print('hiss stop')
            running = False
            if threshold_passed:
                threshold_passed = False
                MouseActions.mouse_drag_end()
                if secondary_mode and config.control_mouse:
                    toggle_control(not config.control_mouse)
            else:
                if secondary_mode:
                    #switch into primary mode
                    print('exit secondary')
                    if not config.control_mouse:
                        toggle_control(not config.control_mouse)
                    MouseActions.unRegSec()
                    MouseActions.regPrim()  
                    secondary_mode = False
                else:
                    #switch into secondary mode
                    print('enter secondary')
                    if config.control_mouse:
                        toggle_control(not config.control_mouse)
                    MouseActions.unRegPrim()
                    MouseActions.regSec()
                    secondary_mode = True
                    
    def leftClick(arg: int):
        """This does a simple left click."""
        ctrl.mouse_click(button=0, hold=setting_mouse_click_duration.get())
          
    def rightClick(arg: int):
        """This does a simple right click."""
        ctrl.mouse_click(button=1, hold=setting_mouse_click_duration.get())
        
    def mouse_drag(button: int):
        """Press and hold/release a specific mouse button for dragging"""
        # Clear any existing drags
        MouseActions.mouse_drag_end()

        # Start drag
        ctrl.mouse_click(button=button, down=True)
      
    def mouse_drag_end():
        """ Releases any held mouse buttons """
        buttons_held_down = list(ctrl.mouse_buttons_down())
        for button in buttons_held_down:
            ctrl.mouse_click(button=button, up=True)
      
    def regPrim():
        """This allows hissing to switch into the secondary mode."""
        print('register 1')
        noise.register('pop', MouseActions.leftClick)
        
    def unRegPrim():
        """This disables the switching of modes when hissing."""
        print('unregister 1')  
        noise.unregister('pop', MouseActions.leftClick)  
        
    def regSec():
        """This allows hissing to switch into the secondary mode."""
        print('register 2')
        noise.register('pop', MouseActions.rightClick)
        
    def unRegSec():
        """This disables the switching of modes when hissing."""
        print('unregister 2')
        noise.unregister('pop', MouseActions.rightClick)
        
    def regAlt():
        """This allows hissing to switch into the alternative mode."""
        print('register a')
        noise.register('hiss', MouseActions.mouse_secondary_mode)
        
    def unRegAlt():
        """This disallows hissing to switch into the alternative mode."""
        print('unregister a')
        noise.unregister('hiss', MouseActions.mouse_secondary_mode)
        
    def turnOnMouseControl():
        """This enables controlling the mouse."""
        toggle_control(True)
        
    def turnOffMouseControl():
        """This disables controlling the mouse."""
        toggle_control(False)
        
    def enter_command_mode(is_active: int):
        """This switches from dictation mode to command mode."""
        if not is_active:
            actions.mode.disable("sleep")
            actions.mode.disable("dictation")
            actions.mode.enable("command")
            #temporary fix for accidently registering multiple times
            actions.user.unRegPrim()
            actions.user.unRegAlt()
            
            actions.user.turnOnMouseControl()
            actions.user.unRegSec()
            actions.user.regPrim()
            actions.user.regAlt()
            #unregistering the method while still in it, seems to be a problem
            cron.after(noise_length_threshold, MouseActions.unRegSwitchCommand) 
            
        
    def regSwitchCommand():
        """This allows hissing to switch from dictation mode to command mode."""
        print('register b') 
        noise.register('pop', MouseActions.enter_command_mode)
        
    def unRegSwitchCommand():
        """This disables hissing to switch from dictation mode to command mode."""
        print('unregister b')
        noise.unregister('pop', MouseActions.enter_command_mode)
        
    def mouse_calibrate():
        """Start calibration"""
        eye_mouse.calib_start()

    def mouse_scroll_down(amount: float = 1):
        """Scrolls down"""
        mouse_scroll(amount * setting_mouse_wheel_down_amount.get())()

    def mouse_scroll_down_continuous():
        """Scrolls down continuously"""
        global continuous_scoll_mode
        continuous_scoll_mode = "scroll down continuous"
        mouse_scroll(setting_mouse_continuous_scroll_amount.get())()

        if scroll_job is None:
            start_scroll()

    def mouse_scroll_up(amount: float = 1):
        """Scrolls up"""
        mouse_scroll(-amount * setting_mouse_wheel_down_amount.get())()

    def mouse_scroll_up_continuous():
        """Scrolls up continuously"""
        global continuous_scoll_mode
        continuous_scoll_mode = "scroll up continuous"
        mouse_scroll(-setting_mouse_continuous_scroll_amount.get())()

        if scroll_job is None:
            start_scroll()

    def mouse_scroll_left(amount: float = 1):
        """Scrolls left"""
        actions.mouse_scroll(0, -amount * setting_mouse_wheel_horizontal_amount.get())

    def mouse_scroll_right(amount: float = 1):
        """Scrolls right"""
        actions.mouse_scroll(0, amount * setting_mouse_wheel_horizontal_amount.get())

    def mouse_scroll_stop():
        """Stops scrolling"""
        stop_scroll()

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global continuous_scoll_mode
        continuous_scoll_mode = "gaze scroll"

        start_cursor_scrolling()



def mouse_scroll(amount):
    def scroll():
        global scroll_amount
        if continuous_scoll_mode:
            if (scroll_amount >= 0) == (amount >= 0):
                scroll_amount += amount
            else:
                scroll_amount = amount
        actions.mouse_scroll(y=int(amount))

    return scroll


def scroll_continuous_helper():
    global scroll_amount
    # print("scroll_continuous_helper")
    if scroll_amount and (
        eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_IDLE
    ):  # or eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_SLEEP):
        actions.mouse_scroll(by_lines=False, y=int(scroll_amount / 10))


def start_scroll():
    global scroll_job
    scroll_job = cron.interval("60ms", scroll_continuous_helper)
    # if eye_zoom_mouse.zoom_mouse.enabled and eye_mouse.mouse.attached_tracker is not None:
    #    eye_zoom_mouse.zoom_mouse.sleep(True)


def gaze_scroll():
        x, y = ctrl.mouse_pos()
        # the rect for the window containing the mouse
        rect = None

        # on windows, check the active_window first since ui.windows() is not z-ordered
        if app.platform == "windows" and ui.active_window().rect.contains(x, y):
            rect = ui.active_window().rect
        else:
            windows = ui.windows()
            for w in windows:
                if w.rect.contains(x, y):
                    rect = w.rect
                    break

        if rect is None:
            # print("no window found!")
            return

        midpoint = rect.y + rect.height / 2
        amount = int(((y - midpoint) / (rect.height / 10)) ** 3)
        actions.mouse_scroll(by_lines=False, y=amount)

    # print(f"gaze_scroll: {midpoint} {rect.height} {amount}")


def stop_scroll():
    global scroll_amount, scroll_job, gaze_job, continuous_scoll_mode
    scroll_amount = 0
    if scroll_job:
        cron.cancel(scroll_job)

    if gaze_job:
        cron.cancel(gaze_job)
    
    scroll_job = None
    gaze_job = None

    continuous_scoll_mode = ""


def start_cursor_scrolling():
    global scroll_job, gaze_job
    stop_scroll()
    gaze_job = cron.interval("60ms", gaze_scroll)



    