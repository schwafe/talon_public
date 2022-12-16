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

    
void:
    insert("void ")
    
return:
    insert("return ")

    
for loop:
	insert("for(")
 
if statement:
 insert("if(")
 
else:
 insert("else {")
 key(enter)

 
logical and:
    insert("&& ") 
     
logical or:
    insert("|| ")   
         
equals:
    insert(" == ")

does not equal:
    insert(" != ")
    
is greater than:
    insert(" > ")
    
is lesser than:
    insert(" < ")
