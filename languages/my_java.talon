tag: user.java
-
#Java
variable <user.prose>$: user.insert_formatted(prose+" ", "CAPITALIZE_FIRST_WORD")
name <user.word>: user.insert_formatted(word+" ", "CAPITALIZE_FIRST_WORD")

open:
 key(end)
 insert('{')
 key(enter)

new:
 insert("new ")

 
equals:
 insert(" == ")

does not equal:
 insert(" != ")
 
is greater than:
 insert(" > ")
 
is lesser than:
 insert(" < ")
 
logger token:
 insert("{}")
 
string:
 insert("String ")
 
boolean:
 insert("boolean ")
   
and:
 insert("&& ") 
  
or:
 insert("|| ") 

null:
 insert("null ")
 
private:
 insert("private ")
 
public:
 insert("public ")
 
static:
 insert("static ")
 
final:
 insert("final ")
 
void:
 insert("void ")
 
if:
 insert("if(")
 
for: 
 insert("for(")
 
else:
 insert("else {")
 key(enter)
 
return:
 insert("return ")
 
break:
 insert("break;")
 
throw new:
 insert("throw new ")
 
javadoc:
 insert("/**")
 key(enter)
 
hash set:
 insert("HashSet<>();")
 
hash map:
 insert("HashMap<>();")