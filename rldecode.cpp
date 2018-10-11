#include<stdio.h>
#include<stdlib.h>
#include <string.h>
/*Encoded file
Arguments:2 inputfile and output file
varibles:
curren_str means gets every character one by one from targetfile;
current_seq means if we find duplicated character ,we will write current_seq and then write the count number;
p_count means when we found the byte with 1 at its first bit, we will calculate the real amount number of the apperance;
*/

void decodedfile(FILE *targetfile, FILE *outputfile) {
	unsigned char current_str, current_seq;
	unsigned int use_count,p_count, i;
	p_count = 0;
	current_str = fgetc(targetfile);
	while (!feof(targetfile)){
		if ((current_str & 0x80) == 0x80 ) {
			p_count = p_count * 128 + (current_str & 0x7F);
		}
		else if ((current_str & 0x80) != 0x80 ) {
			if (p_count == 0) {
				fwrite(&current_str,sizeof(char),1,outputfile);
				current_seq = current_str;
			}
			else if (p_count != 0){
				use_count = p_count - 1;
				for (i = 0; i < use_count;i++) {
					fwrite(&current_seq,1,1,outputfile);
				}
				fwrite(&current_str, 1, 1, outputfile);
				current_seq = current_str;
				p_count = 0;
			}
			else {
				current_seq = current_str;
				fwrite(&current_seq, 1, 1, outputfile);
			}
		}
		current_str = fgetc(targetfile);
			}
	if (p_count != 0) {
		use_count = p_count - 1;
		for (i = 0; i < use_count;i++) {
			fwrite(&current_seq, 1, 1, outputfile);
		}
		p_count = 0;
		}
	}
/*Encoded file
Arguments:1 output file
varibles:
curren_str means gets every character one by one from targetfile;
current_seq means if we find duplicated character ,we will write current_seq and then write the count number;
p_count means when we found the byte with 1 at its first bit, we will calculate the real amount number of the apperance;
*/

void print_encodedfile(FILE *outputfile) {
	unsigned char current_str,current_seq;
	unsigned int p_count=0;
	current_str = fgetc(outputfile);
	while (!feof(outputfile)) {
		if ((current_str & 0x80) == 0x80) {
			p_count = p_count * 128 + (current_str & 0x7F);
		}
		else if ((current_str & 0x80) != 0x80) {
			if (p_count == 0 ) {			
				printf("%c",current_str);
				current_seq = current_str;
			}
			else if (p_count != 0) {
				printf("[%d]",(p_count-3));
				printf("%c", current_str);
				current_seq = current_str;
				p_count = 0;
			}
			else {
				current_seq = current_str;
				printf("%c", current_seq);
			}
		}
		current_str = fgetc(outputfile);
		}
	if (p_count != 0) {
		printf("[%d]", (p_count - 3));
		p_count = 0;
	}
		
	}

int main(int argc, char *argv[])
{
	if (argc == 1)
	{
		exit(0);
	}
	if (argc == 2) {
		FILE *fstream;
		if ((fstream = fopen(argv[1], "r")) == NULL)
		{
			exit(1);
		}
		print_encodedfile(fstream);
		fclose(fstream);
	}
	if (argc == 3) {
		FILE *fp1, *fp2;
		if ((fp1 = fopen(argv[1], "r")) == NULL)
		{
			exit(1);
		}
		if ((fp2 = fopen(argv[2], "wt+")) == NULL)
		{
			exit(1);
		}
		decodedfile(fp1, fp2);
		fclose(fp1);
		fclose(fp2);
	}

	return 0;
}
