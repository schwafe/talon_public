app: vscode
-
tag(): user.find_and_replace
tag(): user.line_commands
tag(): user.snippets
tag(): user.splits
tag(): user.tabs

# Language Features
suggest show: user.vscode("editor.action.triggerSuggest")
hint show: user.vscode("editor.action.triggerParameterHints")
definition show: user.vscode("editor.action.revealDefinition")
definition peek: user.vscode("editor.action.peekDefinition")
definition side: user.vscode("editor.action.revealDefinitionAside")
references show: user.vscode("editor.action.goToReferences")
references find: user.vscode("references-view.find")
format that: user.vscode("editor.action.formatDocument")
imports fix: user.vscode("editor.action.organizeImports")
problem next: user.vscode("editor.action.marker.nextInFiles")
problem last: user.vscode("editor.action.marker.prevInFiles")
problem fix: user.vscode("problems.action.showQuickFixes")
rename that: user.vscode("editor.action.rename")

comment: user.vscode("editor.action.commentLine")

make and run:
    user.vscode("workbench.action.terminal.focus")
    insert('make')
    key(enter)
    sleep(1)
    insert('./build/eda.out')
    key(enter)