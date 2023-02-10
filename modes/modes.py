from talon import (
    Module,
    actions,
    imgui,
    app
)

mod = Module()
mod.mode("deep_sleep", desc="deep sleep mode, can't awaken without mouse")

@imgui.open(x=1800, y=200)
def button_exit_deep_sleep(gui: imgui.GUI):
    if gui.button("Exit deep sleep"):
        print("exiting deep sleep!")
        actions.mode.disable("user.deep_sleep")
        actions.mode.enable("command")
        button_exit_deep_sleep.hide()
        
        
@mod.action_class
class Actions:
        
    def enter_command_mode():
        """Enters command mode"""
        actions.mode.disable("sleep")
        actions.mode.disable("user.deep_sleep")
        actions.mode.disable("dictation")
        actions.mode.enable("command")
        
    def enter_dictation_mode():
        """Enters dictation mode"""
        actions.mode.disable("sleep")
        actions.mode.disable("user.deep_sleep")
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        
    def toggle_parrot_mode():
        """Toggles the parrot mode on and off."""
        actions.mode.toggle("user.parrot")
        
    def show_exit_deep_sleep_button():
        """Shows the "Exit deep sleep" button"""
        button_exit_deep_sleep.show()

    def enter_command_mode_with_mouse_control():
        """Enters command mode and sets modus_operandi and mouse control"""
        actions.user.mouse_set_primary_mode()
        actions.user.enter_command_mode()
        actions.user.turnOnMouseControl()

    app.register("ready",enter_command_mode_with_mouse_control )