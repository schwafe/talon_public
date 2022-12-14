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