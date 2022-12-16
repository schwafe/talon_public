tag: user.java
-
#Java
variable <user.prose>$: user.insert_formatted(prose+" ", "CAPITALIZE_FIRST_WORD")
name <user.word>: user.insert_formatted(word+" ", "CAPITALIZE_FIRST_WORD")

new:
 insert("new ")
 
logger token:
 insert("{}")
 
string:
 insert("String ")
 
boolean:
 insert("boolean ")
   
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