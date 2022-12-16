from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.tag("vscode", desc="tag for enabling vscode commands")

mod.apps.vscode = """
tag: user.vscode
"""

@mod.action_class
class Actions:
    def set_eda_tags():
        """Sets the active language mode and vscode tag"""
        ctx.tags = ["user.c","user.vscode"]

    def clear_eda_tags():
        """Clears the active language mode and vscode tag"""
        ctx.tags = []