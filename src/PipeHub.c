/*****************************************************************************
 Excerpt from "Linux Programmer's Guide - Chapter 6"
 (C)opyright 1994-1995, Scott Burkett
 ******************************Y*********************************************** 
 MODULE: fifoserver.c
 ******************************Y*********************************************** 
 forked by xealits
 *****************************************************************************/

#include <stdio.h> // FILE, fprintf, sscanf
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

#include <linux/stat.h>

#include <ctype.h> // isspace
#include <string.h> // strlen, strcmp
//#include <signal.h> // signal and SIGNINT

#include <PipeHub.h>
#include <CAENVMECalls.h>
//#define FIFO_FILE       "pipe"
#define FIFO_READLEN 258
// TODO: don't know how to use C macro in the subspecifier of format string
// #define FIRST_WORD_READLEN 33 // should be less than FIFO_READLEN
//#define BUFF_SIZE 80

/*
FILE *fin;
FILE *fin_keeper;

FILE *fout;
FILE *fsts;
FILE *ferr;
*/

//void termination_handler( int signum );

int is_blank(const char *s);
// the function checks if the input string consists of blank characters


// void PipeHub( FILE * fin, FILE * fsts, FILE * fout, FILE * ferr )
void PipeHub( PipeHub_Parameters * parameters)
{
	FILE * fin  = parameters->stream_in;
	FILE * fsts = parameters->stream_sts;
	FILE * fout = parameters->stream_out;
	FILE * ferr = parameters->stream_err;

	Status_Prompt_Levels * status_prompt_level = parameters->status_prompt_level;


	char readbuf[FIFO_READLEN];
	// char command_word[FIRST_WORD_READLEN];
	char command_word[33]; // should be less than FIFO_READLEN
	char rest_of_input[FIFO_READLEN-33]; // should be less than FIFO_READLEN

	char * vme_call_result;


	/* if input commands (fin) come from the terminal
	   where status is prompted back (fsts)
	   than the prompt should not have newline
	   otherwise one should add a newline */
	// static char prompt_line[8] = "> ";
	// if (fin == stdout)
	// {
		 // code 
	// }

	fprintf(fsts, "INFO: The PipeHub is configured and ready.\n");
	// fprintf(fout, "TEST output: test-test!\n");
	fprintf(fsts, "INFO: reading the input command -\n> ");

	int compar_parse_count;

	while(1)
	{
		// since there is dummy keeper for external inputs
		// and stdin is always opened
		// the fin should always be opened when the process is running
		// fprintf(fsts, "> ");
		fgets(readbuf, FIFO_READLEN, fin);

		// if (is_blank(readbuf)) { continue; }

		// if readbuf starts with set -- the command is intended for the PipeHub itself
		// it should run some reconfiguration

		// TODO: should one strip the trailing newline here? check for readbuffer overload?

		if ( (compar_parse_count = sscanf(readbuf, "%32s %[^\n]", command_word, rest_of_input)) < 1 ) { continue; }
		else {
			if ( strcmp(command_word, "set") == 0 )
			{
				if (compar_parse_count < 2)
				{
					fprintf(fsts, "INFO: Did not get the reconfig task.\n");
				}
				else
				{
					/* reset some config of the PipeHub */
					fprintf(fsts, "INFO: Don't know how to reconfigure myself with %s yet.. Done.\n", rest_of_input);
				}
			}
			else if ( strcmp(command_word, "awesome!") == 0 )
			{
				fprintf(fsts, "INFO: I know!\n");
			}
			else if ( strcmp(command_word, "help") == 0 )
			{
				fprintf(fsts, "INFO: Getting help from CAENVMECalls on %s,\n", rest_of_input);
				vme_call_result = CAENVMECall( command_word, rest_of_input, fout, ferr );
				fprintf(fsts, "INFO: the call result is %s.\n", vme_call_result);
			}
			else
			{
				// strip newline and forward the input string to CAEN calls
				/*
				if ( readbuf[strlen(readbuf)-1] == '\n' ) {
					readbuf[strlen(readbuf)-1]='\0';
					// fprintf(fsts, "INFO: Received string: %s\n", readbuf);
					// fprintf(fout, "Received string: %s\n", readbuf);
				}
				*/
				if (compar_parse_count < 2)
				{
					rest_of_input[0] = '\0'; // set to empty string
				}
				fprintf(fsts, "INFO: Calling VME with %s on %s,\n", command_word, rest_of_input);
				vme_call_result = CAENVMECall( command_word, rest_of_input, fout, ferr );
				fprintf(fsts, "INFO: the call result is %s.\n", vme_call_result);
			}
		}
		/*
		if ( readbuf[strlen(readbuf)-1] == '\n' ) {
			readbuf[strlen(readbuf)-1]='\0';
			fprintf(fsts, "INFO: Received string: %s\n", readbuf);
			// fprintf(fout, "Received string: %s\n", readbuf);
		}
		else {
			// fprintf(fsts, "INFO: Received string: %s⏎\n", readbuf);
			fprintf(fsts, "INFO: Received string: %s...\n", readbuf);
			// fprintf(fout, "Received string: %s...\n", readbuf);
		}
		*/


		fprintf(fsts, "> ");
	}

	//fclose(fin);
	//fclose(fout);
	// return(0);
}

int is_blank(const char *s) {
  while (*s != '\0') {
    if (!isspace(*s))
      return 0;
    s++;
  }
  return 1;
}

