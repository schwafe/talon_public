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
scroll_job = None
gaze_job = None


mod = Module()
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
        toggle_control(True)
        
    def turnOffMouseControl():
        """This disables controlling the mouse."""
        toggle_control(False)
                        
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
        
    def enter_command_mode():
        """Enters command mode and sets modus_operandi and mouse control"""
        global modus_operandi
        print('modus_operandi 1')
        modus_operandi = 1
        actions.mode.disable("sleep")
        actions.mode.disable("dictation")
        actions.mode.enable("command")
        actions.user.turnOnMouseControl()
        
    def enter_dictation_mode():
        """Enters dictation mode and sets modus_operandi and mouse control"""
        global modus_operandi
        print('modus_operandi 3')
        modus_operandi = 3
        actions.mode.disable("sleep")
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        actions.user.turnOffMouseControl()


def still_running():
    """If the hiss is still going, a drag motion is started"""
    global threshold_passed
    if running:
        threshold_passed = True
        if modus_operandi == 1:
            #start left drag
            actions.user.mouse_drag(0)
        elif modus_operandi == 2:
            #start right drag
            #toggle_control(not config.control_mouse)
            actions.user.mouse_drag(1)
                
 
def onHiss(active: int):
    """This handles the hiss sound."""
    global modus_operandi, running, threshold_passed
    if modus_operandi != 3:
        if active:
            print('hiss start')
            #wait and see if it's a long hiss
            if not running:
                running = True
                cron.after(setting_hiss_threshold.get(), still_running)
            else:
                print('prevented double hiss!')
        elif threshold_passed:
            print('drag end')
            #drag end
            actions.user.mouse_drag_end()
            #if modus_operandi == 2:
                #stop dragging with right click
                #toggle_control(not config.control_mouse)
            threshold_passed = False
            running = False
        else:
            #short hiss
            print('hiss end')
            toggle_control(not config.control_mouse)
            if modus_operandi == 0 or modus_operandi == 2:
                print('modus_operandi 1')
                modus_operandi = 1
            elif modus_operandi == 1:
                print('modus_operandi 2')
                modus_operandi = 2
            running = False
                
noise.register('hiss', lambda active: onHiss(active))
                    
def onPop(active: int):
    """This handles the pop sound."""
    if modus_operandi == 1:
        ctrl.mouse_click(button=0, hold=setting_mouse_click_duration.get())
    elif modus_operandi == 2:
        ctrl.mouse_click(button=1, hold=setting_mouse_click_duration.get())
    elif modus_operandi == 3:
        actions.user.enter_command_mode()

noise.register('pop', lambda active: onPop(active))

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



    