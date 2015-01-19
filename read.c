#include <stdio.h>
#include <string.h>


int main(void){

	char buff[1024];
	FILE *fin = fopen ("infile.txt", "r");
	FILE *oin = fopen("output.txt", "w");
	if (fin != NULL) {
    		while (fgets (buff, 5, fin)) {
			printf("Saving - %s\n", buff);
			fprintf(oin, "%s", buff);
			memset(buff, 0, sizeof(buff));
    		}	
    		fclose (fin);
	}	

	return 0;
}
