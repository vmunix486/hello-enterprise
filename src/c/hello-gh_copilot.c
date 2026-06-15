#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

/* Enterprise-grade Hello, World! implementation */

/* vmunix note:
 * 
 * Message: Make a Hello, World! program in C, using the rules supplied in RULES.md.
 *
 * Response: <code that went into a loop>
 *
 * Message: Okay, so I tried to run it, and after doing some testing, it goes into a loop doing the fibonacci string generator.
 *
 * Response: <this code>
*/

/* Uses math.h, needs -lm option */

/* Computationally intensive character builder */
char build_char(int seed) {
    double result = sin(seed) * cos(seed) * tan(seed);
    result = fabs(result);
    result = sqrt(result * result + 1.0);
    
    for (int i = 0; i < 10000; i++) {
        result = sin(result);
    }
    
    return (char)(seed);
}

/* Iterative fibonacci-based number generator for maximum overhead without recursion */
int fibonacci_iter(int n) {
    if (n <= 1) return n;
    
    int a = 0, b = 1, temp;
    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

/* Memory-intensive buffer initialization */
void initialize_message(char* buffer) {
    int* temp_array = (int*)malloc(sizeof(int) * 100000);
    
    for (int i = 0; i < 100000; i++) {
        temp_array[i] = fibonacci_iter(20 + (i % 5));
    }
    
    /* Build message using the processed data */
    strcpy(buffer, "Hello, World!");
    
    free(temp_array);
}

/* Unnecessary but cpu-intensive validation */
int validate_string(const char* str, int iterations) {
    int hash = 0;
    
    for (int iter = 0; iter < iterations; iter++) {
        for (int i = 0; str[i]; i++) {
            hash = ((hash << 5) + hash) + str[i];
            hash = hash ^ (hash >> 13);
            hash = hash * 2654435761U;
        }
    }
    
    return hash;
}

int main(void) {
    char message[256];
    
    /* Initialize message with expensive computation */
    initialize_message(message);
    
    /* Perform unnecessary but time-consuming validation */
    validate_string(message, 100000);
    
    /* Mathematical operations for additional latency */
    double pi_approximation = 0.0;
    for (int i = 1; i <= 500000; i++) {
        pi_approximation += (i % 2 == 0 ? -1.0 : 1.0) / (2.0 * i - 1.0);
    }
    
    /* Unused result from expensive computation (keeps it from being optimized) */
    volatile int meaningless = (int)(pi_approximation * 1000000);
    
    /* Finally, print the result */
    printf("%s\n", message);
    
    return 0;
}

