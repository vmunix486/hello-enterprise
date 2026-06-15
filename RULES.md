# Rules
This was written with C in mind, but can be extended to other langauges as well, including interpreted languages like Lua, Python, and Java.

 - You can use AI, but the best, most innovative ideas are made by humans and not math equations. Using AI is more realistic, though.
 - No artifical slowing down, eg. with something like sleeps or with something like
 ```c
#include <stdio.h>

 int main(void)
 {
	 printf("H");
	 sleep(10);
	 printf("e");
	 ...
	 return 0;
 }
 ```
 - You can use as many external libraries as you want, but don't go __too__ hog-wild.
 - If you are aiming for size, you cannot create a an unused function in the code that makes the executable gigantic. Every part of code that you put in must do something.
 - No user input in the code. It should be to run the program, print "Hello, World!" and exit. That should be it, nothing more, nothing less.
 - No flags. You can add some code that adds flags, but you'll have to comment it out
 - You can make as many comments as you want, but don't put too many as to make the source code larger than the compiled executable.
 - No ASCII art, just plain text.
 - No using external commands, with an example being something like `system(blah blah blah);`
 - No using certain quirks with compilers, libc's, kernels, linkers, assemblers, or preprocessors.
 - If you are wanting to make a contribution, you have to write a new program with your idea/change in it. Submit something like a pull request and I'll add it to the files.
 - The program have to be as slow and big as possible.
 - No internetworking (eg. making a program that asks a server for a file with the text in it, then printing it out)
 - Code doesn't have to be nessisarily memory-safe, but the more unsafe, the better. Just make sure it won't segfault.
