from talon import Context, Module, actions, app

is_mac = app.platform == "mac"

ctx = Context()
mac_ctx = Context()
mod = Module()
mod.apps.vscode = """
os: linux
and app.name: Code
os: linux
and app.name: code-oss
os: linux
and app.name: code-insiders
os: linux
and app.name: VSCodium
os: linux
and app.name: Codium
"""
mod.apps.vscode = """
os: windows
and app.name: Visual Studio Code
os: windows
and app.name: Visual Studio Code Insiders
os: windows
and app.name: Visual Studio Code - Insiders
os: windows
and app.exe: Code.exe
os: windows
and app.exe: Code-Insiders.exe
os: windows
and app.name: VSCodium
os: windows
and app.exe: VSCodium.exe
"""

ctx.matches = r"""
app: vscode
"""


@ctx.action_class("app")
class AppActions:
    # talon app actions
    def tab_open():
        actions.user.vscode("workbench.action.files.newUntitledFile")

    def tab_close():
        actions.user.vscode("workbench.action.closeActiveEditor")

    def tab_next():
        actions.user.vscode("workbench.action.nextEditorInGroup")

    def tab_previous():
        actions.user.vscode("workbench.action.previousEditorInGroup")

    def tab_reopen():
        actions.user.vscode("workbench.action.reopenClosedEditor")

    def window_close():
        actions.user.vscode("workbench.action.closeWindow")

    def window_open():
        actions.user.vscode("workbench.action.newWindow")


@ctx.action_class("code")
class CodeActions:
    # talon code actions
    def toggle_comment():
        actions.user.vscode("editor.action.commentLine")


@ctx.action_class("edit")
class EditActions:
    # talon edit actions
    def indent_more():
        actions.user.vscode("editor.action.indentLines")

    def indent_less():
        actions.user.vscode("editor.action.outdentLines")

    def save_all():
        actions.user.vscode("workbench.action.files.saveAll")

    def line_insert_down():
        actions.user.vscode("editor.action.insertLineAfter")

    def line_insert_up():
        actions.user.vscode("editor.action.insertLineBefore")

    def jump_line(n: int):
        actions.user.vscode("workbench.action.gotoLine")
        actions.insert(str(n))
        actions.key("enter")
        #actions.edit.line_start()

    def select_none():
        actions.key("escape")


@ctx.action_class("win")
class WinActions:
    def filename():
        title = actions.win.title()
        result = title.split(" - ")[0]

        if "." in result:
            return result

        return ""


@mod.action_class
class Actions:
    def vscode_terminal(number: int):
        """Activate a terminal by number"""
        actions.user.vscode(f"workbench.action.terminal.focusAtIndex{number}")

    def command_palette():
        """Show command palette"""
        actions.key("ctrl-shift-p")


# @ctx.action_class("user")
# class UserActions:

#     def tab_jump(number: int):
#         if number < 10:
#             actions.key(f"alt-{number}")
#         else:
#             actions.user.vscode_with_plugin(
#                 "workbench.action.openEditorAtIndex", number
#             )

#     def tab_final():
#         actions.key("alt-0")

#     # find_and_replace.py support begin

#     def find(text: str):
#         """Triggers find in current editor"""
#         actions.key("ctrl-f")

#         if text:
#             actions.insert(text)

#     def find_next():
#         actions.user.vscode("editor.action.nextMatchFindAction")

#     def find_previous():
#         actions.user.vscode("editor.action.previousMatchFindAction")

#     def find_everywhere(text: str):
#         """Triggers find across project"""
#         actions.key("ctrl-shift-f")

#         if text:
#             actions.insert(text)


#     def select_previous_occurrence(text: str):
#         actions.edit.find(text)
#         actions.sleep("100ms")
#         actions.key("shift-enter esc")

#     def select_next_occurrence(text: str):
#         actions.edit.find(text)
#         actions.sleep("100ms")
#         actions.key("esc")
