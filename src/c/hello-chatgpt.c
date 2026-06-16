#include <stdio.h>

/* vmunix message
 *
 * For whatever reason, ChatGPT just did not want to make a program like Copilot. It heavily insisted to keep it pretty simple instead.
 *
 * First message: Make a Hello, World! program in C using the rules in the supplied RULES.md.
 *
 * ChatGPT: This is pretty unusual, but here's a Hello, World program <basic ahh hello world>
 *
 * Me: Here is an example of a program one of your colleagues, Github Copilot made. You might get the gist of it once you read it. Just don't do the exact same thing they did. <attached hello-gh_copilot.c>
 *
 * ChatGPT: <this program> ... <out of file attachments>
*/

/* WARNING: THIS CRAP DOESN'T WORK!!! */

int main(void)
{
    const char message[] = "Hello, World!";
    unsigned long checksum = 0;
    int i;

    /*
     * Walk over the message multiple times.
     * The checksum is actually used, so the work is not dead code.
     */
    for (i = 0; i < sizeof(message) - 1; i++) {
        checksum += message[i];
    }

    /*
     * Use the computed value in a harmless way.
     * This keeps the compiler from removing the loop.
     */
    if (checksum != 1161)
        return 1;

    puts(message);

    return 0;
}
