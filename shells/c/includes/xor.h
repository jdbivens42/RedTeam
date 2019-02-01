#ifndef XOR_H
#define XOR_H
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
//xor s (in place) by key t
//returns pointer to s
char* xor(char* s, char* t) {
    int t_len = strlen(t);
    for (int i=0; i<strlen(s); i++){
        s[i] ^= t[i % t_len];
    }
   return s;
}

//https://stackoverflow.com/questions/3408706/hexadecimal-string-to-byte-array-in-c
//convert hex string s in place
//Returns pointer to s
char* from_hex(char* s) {
    char* pos = s;
    char* t;
    t = (char*) malloc(strlen(s) + 1);
    int i;
    for (i = 0; i < strlen(s) / 2; i++) {
        sscanf(pos, "%2hhx", t+i);
        pos += 2;
    }
    //Terminate the string (which is half as long as the original)
    t[i] = 0;
    strcpy(s, t);
    free(t);
    return s;
}
#endif
