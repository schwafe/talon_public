from talon import Module, Context, noise, actions, ctrl, cron
from talon_plugins.eye_mouse import config, toggle_control
from time import sleep, time

mod = Module() 

start = 0
running = False
noise_length_threshold = "150ms"
threshold_passed = False

@mod.action_class
class MouseActions:
    def still_running():
        """If the hiss is still going, a drag motion is started"""
        global running
        global threshold_passed
        if running:
            threshold_passed = True
            #if controlling the mouse is enabled a drag motion is started
            if(config.control_mouse):
                actions.user.mouse_drag(0)
 
    def mouse_secondary_mode(is_active: int):
        """This mode is used for stopping the mouse and right clicking."""
        global start
        global running
        global threshold_passed
        if is_active:
            start = time()
            running = True
            cron.after(noise_length_threshold, MouseActions.still_running)
        else:
            running = False
            if threshold_passed:
                threshold_passed = False
                actions.user.mouse_drag_end()
            else:
                print('toggle secondary')
                actions.user.mouse_toggle_control_mouse()
                if(not config.control_mouse):
                    noise.register('pop', MouseActions.rightClick)
                else:
                    noise.unregister('pop', MouseActions.rightClick)

        
          
    def rightClick(arg: int):
        """This does a simple right click."""
        ctrl.mouse_click(button=1, hold=16000)
      
    def regSec():
        """This allows hissing to switch into the secondary mode."""
        print('register')
        noise.register('hiss', MouseActions.mouse_secondary_mode)
        
    def unRegSec():
        """This disables the switching of modes when hissing."""
        print('unregister')
        noise.unregister('hiss', MouseActions.mouse_secondary_mode)
        
    def turnOffMouseControl():
        """This disables controlling the mouse."""
        toggle_control(False)
        
    def turnOnMouseControl():
        """This enables controlling the mouse."""
        if(not config.control_mouse):
            toggle_control(True)
        
    def enter_command_mode(arg: int):
        """This switches from dictation mode to command mode."""
        if arg:
            MouseActions.unRegSwitchCommand()
            actions.mode.disable("dictation")
            actions.mode.enable("command")
            MouseActions.turnOnMouseControl()
            
            #the end of the hissing noise can trigger the secondary mode, if it's registered too early
            cron.after(noise_length_threshold, MouseActions.regSec)
        
    def regSwitchCommand():
        """This allows hissing to switch from dictation mode to command mode."""
        noise.register('hiss', MouseActions.enter_command_mode)
        
    def unRegSwitchCommand():
        """This disables hissing to switch from dictation mode to command mode."""
        noise.unregister('hiss', MouseActions.enter_command_mode)