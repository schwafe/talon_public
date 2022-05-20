from talon import (Module, actions, imgui)

mod = Module()
mod.mode("parrot", desc="additional noises mode")


@imgui.open(x=1800, y=50)
def button_exit_parrot_mode(gui: imgui.GUI):
    if gui.button("P ON"):
        print("parrot mode is now off")
        actions.mode.disable("user.parrot")
        actions.user.show_parrot_off_button()
        
@imgui.open(x=1800, y=50)
def button_enter_parrot_mode(gui: imgui.GUI):
    if gui.button("P OFF"):
        print("parrot mode is now on")
        actions.mode.enable("user.parrot")
        actions.user.show_parrot_on_button()
        
@mod.action_class
class Actions:
    def show_parrot_on_button():
        """Shows the parrot mode ON button"""
        button_enter_parrot_mode.hide()
        button_exit_parrot_mode.show()
        
    def show_parrot_off_button():
        """Shows the parrot mode OFF button"""
        button_exit_parrot_mode.hide()
        button_enter_parrot_mode.show()
        
    def hide_parrot_buttons():
        """Hides the parrot mode button"""
        button_exit_parrot_mode.hide()
        button_enter_parrot_mode.hide()