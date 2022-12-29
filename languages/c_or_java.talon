tag: user.java
tag: user.c
-

line complete:
    key(end)
    insert(';')

open:
    key(end)
    insert('{')
    key(enter)
	
(assign|set):
	insert(" = ")
	
true:
	insert("true;")
 
false:
	insert("false;")
	
semi:
	insert(';')
	
increment:
	insert('++')

decrement:
    insert('--')
    
void:
    insert("void ")
    
return:
    insert("return ")

    
for loop:
	insert("for(")
 
state if:
 insert("if(")
 
else:
 insert("else {")
 key(enter)

(logical|lodge) and:
    insert("&& ") 
     
(logical|lodge) or:
    insert("|| ")   
         
equals:
    insert(" == ")

does not equal:
    insert(" != ")
    
[is] greater than:
    insert(" > ")
    
[is] lesser than:
    insert(" < ")

[is] greater or equal:
    insert(" >= ")

[is] lesser or equal:
    insert(" <= ")