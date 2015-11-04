/*****************************************************************************
 Excerpt from "Linux Programmer's Guide - Chapter 6"
 (C)opyright 1994-1995, Scott Burkett
 ******************************Y*********************************************** 
 MODULE: fifoserver.c
 ******************************Y*********************************************** 
 forked by xealits
 *****************************************************************************/

#include <stdio.h> // FILE, fprintf
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

#include <linux/stat.h>

#include <ctype.h> // isspace
#include <string.h> // strlen, strcmp
//#include <signal.h> // signal and SIGNINT
// #include <include/CAENVMECalls.h> // CAENVMECall
// #include <../include/CAENVMECalls.h>
#include <CAENVMECalls.h>
//#define FIFO_FILE       "pipe"
#define FIFO_READLEN 256
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



void PipeHub( FILE * fin, FILE * fsts, FILE * fout, FILE * ferr )
{

	char readbuf[FIFO_READLEN];

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

	while(1)
	{
		// since there is dummy keeper for external inputs
		// and stdin is always opened
		// the fin should always be opened when the process is running
		// fprintf(fsts, "> ");
		fgets(readbuf, FIFO_READLEN, fin);

		if (is_blank(readbuf)) { continue; }

		// if readbuf starts with set -- the command is intended for the PipeHub itself
		// it should run some reconfiguration

		// TODO: should one strip the trailing newline here? check for readbuffer overload?

		if ( readbuf[strlen(readbuf)-1] == '\n' ) {
			readbuf[strlen(readbuf)-1]='\0';
			fprintf(fsts, "INFO: Received string: %s\n", readbuf);
			// fprintf(fout, "Received string: %s\n", readbuf);
		}
		else {
			fprintf(fsts, "INFO: Received string: %s...\n", readbuf);
			// fprintf(fout, "Received string: %s...\n", readbuf);
		}

		// here the input string is forwarded to CAEN calls
		fprintf(fsts, "INFO: Calling VME with %s,\n", readbuf);
		vme_call_result = CAENVMECall( readbuf, fout, ferr );
		fprintf(fsts, "INFO: the call result is %s.\n", vme_call_result);

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

