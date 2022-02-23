app: stm32cubeide.exe
app: eclipse.exe
app: fitdp.exe
-
open declaration:
 key(f3)
 
follow include:
 key(f3)
 
complete:
 key(ctrl-space)
 
quick fix:
 key(ctrl-1)
 
quick outline:
 key(ctrl-o) 
 
quick type hierarchy:
 key(ctrl-t)
 
rename:
 key(shift-alt-r)
 
find it|search:
 key(ctrl-f)
 
resume:
 key(f8)
 
step in:
 key(f5) 

step over:
 key(f6)

step return: 
 key(f7)

terminate:
 key(ctrl-f2)
 
breakpoint toggle:
 key(ctrl-shift-b)
 
tab close:
 key(ctrl-w)
 
comment:
 key(ctrl-7)
 
references:
 key(ctrl-shift-g)
 
block mode:
 key(alt-shift-a)

project launch:
 key(ctrl-f11)
 
project debug:
 key(f11)
 
matching brace:
 key(ctrl-shift-p)
  
next match:
 key(ctrl-.)
 
previous match:
 key(ctrl-,)
 
line complete:
 key(end)
 insert(';')
 
fix indentation:
 key(ctrl-shift-f)
 
#############################
#Java

new:
 insert("new ")
 
(assign|set):
 insert(" = ")
 
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
 
todo:
 insert("TODO ")
 
string:
 insert("String ")
 
boolean:
 insert("boolean ")
 
true:
 insert("true;")
 
false:
 insert("false;")
 
private:
 insert("private ")
 
public:
 insert("public ")
 
static:
 insert("static ")
 
void:
 insert("void ")
 
if:
 insert("if (")
 
return:
 insert("return ")
 
break:
 insert("break;")
 
throw new:
 insert("throw new ")
 
javadoc:
 insert("/**")
 key(enter)

#############################
#custom keybinds
 
system explorer:
 key(ctrl-shift-alt-w)
 
project build:
 key(ctrl-shift-alt-v)
 
project build clean:
 key(ctrl-shift-alt-c)
 
suspend:
 key(ctrl-shift-alt-s)

 #key(ctrl-shift-alt-q)