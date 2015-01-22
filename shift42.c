#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
    -Shift42 v1.0
    -Shift Cipher Program by Jacob/Gimppy Holcomb
    -September 2013
*/

void usage(char *prog){

   printf("\nEncoding Usage: %s <'Message'> <Positive Shift>\n"
          "Decoding Usage: %s <'Message'> <Negative Shift>\n\n", prog, prog);
   exit(0);
}


int inputCheck(int argc, int num){

    if (argc < num + 1){
        return 0;
    }
    else{
        return 1;
    }
}


int main(int argc, char *argv[]){
    
    if (!inputCheck(argc, 2)){
        usage(argv[0]);
    }
    char buff[strlen(argv[1])];
    char message[sizeof(buff)];
    int cShift = atoi(argv[2]);

    strncpy(buff, argv[1], strlen(argv[1]));
    
    int i;
    for (i = 0; i < strlen(buff); i++){
        snprintf(message + i, strlen(buff), "%c", (buff[i] + cShift));
    }
    
    if (cShift > 0){
        printf("\nYour encoded message is: %.*s\n\n", strlen(argv[1]), message);
    }
    else{
        printf("\nYour decoded message is: %.*s\n\n", strlen(argv[1]), message);
    }

    return 0;
}
