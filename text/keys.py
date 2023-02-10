from talon import Context, Module, actions

mod = Module()
ctx = Context()

mod.list("modifier_key", desc="All modifier keys")
modifier_keys = {
    'alt': 'alt',  
    'alter': 'alt',
    'control': 'ctrl',
    'shift': 'shift',
    'super': 'super',
}

ctx.lists["self.modifier_key"] = modifier_keys

@mod.capture(rule="{self.modifier_key}+ {self.letter}")
def keystroke(m) -> str:
    "One keystroke"
    modifiers= "-".join(m.modifier_key_list)
    return modifiers+"-"+m.letter

@mod.action_class
class Actions:
    def hold_keys(keys: list[str]):
        "holds one or more keys down"
        for key in keys:
            actions.key(key + ":down")

    
    def release_keys(keys: list[str]):
        "releases one or more keys"
        for key in keys:
            actions.key(key + ":up")