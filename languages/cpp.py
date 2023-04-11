
from talon import Module, Context, actions

mod = Module()
ctx = Context()
ctx.matches = r'''
tag: user.cpp
'''

mod.list(
    'cpp_types',
    desc='types in cpp',
)
ctx.lists['user.cpp_types'] = {
    'vector': 'std::vector',
    'integer': 'int',
    'string': 'std::string',
    'auto': 'auto',
    'void': 'void',
}

mod.list(
    'cpp_values',
    desc='values in cpp',
)
ctx.lists['user.cpp_values'] = {
    'true': 'true',
    'false': 'false',
    'null': 'nullptr',
}

mod.list(
    'cpp_constructs',
    desc='constructs in cpp',
)
ctx.lists['user.cpp_constructs'] = {
    'if',
    'for',
    'while',
    'do while',
}

mod.list(
    'cpp_operators',
    desc='operators in cpp',
)
ctx.lists['user.cpp_operators'] = {
    'open', 'complete', 'equals', 'does not equal', 'todo', 'scope', 'increment', 'set','assign','reference','ref','args', 'and','or'}


@mod.action_class
class Actions:
    def call_operator(operator: str):
        'calls functions for given operator'
        if (operator == 'open'):
            actions.edit.line_end()
            actions.insert('{')
            actions.key('enter')
        elif (operator == 'complete'):
            actions.edit.line_end()
            actions.insert(';')
        elif (operator == 'equals'):
            actions.insert(' == ')
        elif (operator == 'does not equal'):
            actions.insert(' != ')
        elif (operator == 'todo'):
            actions.insert('TODO ')
        elif (operator == 'scope'):
            actions.insert('::')
        elif (operator == 'increment'):
            actions.insert('++')
        elif (operator == 'set'or operator == 'assign'):
            actions.insert(' = ')
        elif (operator == 'reference'or operator == 'ref'):
            actions.insert('&')
        elif (operator == 'args'):
            actions.insert('(')
        elif (operator == 'and'):
            actions.insert(' && ')
        elif (operator == 'or'):
            actions.insert(' || ')


    def call_construct(construct: str):
        'calls functions for given construct'
        if (construct == 'if'):
            actions.insert('if(')
        elif (construct == 'for'):
            actions.insert('for(')
        elif (construct == 'while'):
            actions.insert('while(')
        elif (construct == 'do while'):
            actions.insert('do {\n')
            actions.edit.down()
            actions.insert('while()')
            actions.edit.left()
