tag: user.cpp
-

standard: 'std'
member: '.'

type {user.cpp_types} : '{user.cpp_types} '

construct {user.cpp_constructs} :  user.call_construct(cpp_constructs)

op {user.cpp_operators}: user.call_operator(cpp_operators)

val {user.cpp_values} : '{user.cpp_values}'

(variable|var) {user.cpp_types} <user.text>$: 
    insert("{user.cpp_types} ")
    user.insert_formatted( "camel", user.text)

sym <user.symbols>: '{user.symbols}'

op in <user.text>$: 
    insert(" : ")
    user.insert_formatted( "camel", user.text)
