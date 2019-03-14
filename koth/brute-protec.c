/*
*   Simple, brute-force, cross-platoform "protec.c" script
*       Reads files into memory and overwrites the file contents every second.
*   Usage: ./brute-protec /path/to/file1 /path/to/file2 ...
*   
*   Compilation:
*       gcc brute-protec.c -o brute-protec
*       i686-w64-mingw32-gcc brute-protec.c -o brute-protec.exe
*/

#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
    #include <windows.h>
#else
    #include <unistd.h>
#endif
/**
 * Cross-platform sleep function for C
 * @param int milliseconds
 */
void sleep_ms(int milliseconds)
{
    #ifdef _WIN32
        Sleep(milliseconds);
    #else
        usleep(milliseconds * 1000);
    #endif
}



int main(int argc, char* argv[]) {
    char *source = NULL;
    char **content = malloc(sizeof(char*) * (argc-1) );
    long *lens = calloc(argc-1, sizeof(long) );

    for (int i = 1; i < argc; i++) {
         
        FILE *fp = fopen(argv[i], "rb");
        if (fp != NULL) {
            /* Go to the end of the file. */
            if (fseek(fp, 0L, SEEK_END) == 0) {
                /* Get the size of the file. */
                long bufsize = ftell(fp);
                if (bufsize == -1) { /* Error */ }
                printf("Protecting %d chars in %s\n", bufsize, argv[i]);
                /* Allocate our buffer to that size. */
                content[i] = malloc(sizeof(char) * bufsize);

                /* Go back to the start of the file. */
                if (fseek(fp, 0L, SEEK_SET) != 0) { /* Error */ }

                /* Read the entire file into memory. */
                fread(content[i], sizeof(char), bufsize, fp);
                if ( ferror( fp ) == 0 ) {
                    lens[i] = bufsize;
                } else {
                    fputs("Error reading file", stderr);
                }
                
            
                fclose(fp);
            }
        }

    }

    while(1) {
        for (int i=1; i<argc; i++){
            printf("Rewriting %s\n", argv[i]);
            FILE *fp = fopen(argv[i], "wb");
            if (fp != NULL) {
                int written = fwrite(content[i], sizeof(char), lens[i], fp);
                printf("%d chars written to %s\n", written, argv[i]);
                fclose(fp);
            } else {
                printf("Could not open %s for writing\n", argv[i]);
            }
        }
        sleep_ms(1*1000);
    }

    for (int i=1; i<argc; i++){
        free(content[i]);
    }

    free(content);

}
