/*****************************************************************************
 Excerpt from "Linux Programmer's Guide - Chapter 6"
 (C)opyright 1994-1995, Scott Burkett
 ******************************Y*********************************************** 
 MODULE: fifoserver.c
 ******************************Y*********************************************** 
 forked by xealits
 used for VME bus interface, based on CAEN library

 pipe-hub program processes the comand line options for initial configuration of the PipeHub
 -- the procedure managing the operation i/o to VME bus and configuration of it.
 Later the configartion can be changed when PipeHub runs.

 It also manages SIGINT etc.

 Supposedly pipe-hub can be implemented in shell or Python,
 if PipeHub is compiled as a shared library..
 *****************************************************************************/

#include <stdio.h> // FILE, fprintf
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

#include <linux/stat.h>

#include <string.h> // strlen, strcmp
#include <signal.h> // signal and SIGNINT

// #include <include/PipeHub.h>
#include <PipeHub.h>

//#define FIFO_FILE       "pipe"
#define FIFO_READLEN 80
#define BUFF_SIZE 80

FILE *fin;
FILE *fin_keeper;

FILE *fout;
FILE *fsts;
FILE *ferr;


//void termination_handler( int signum );



int main(int argc, char *argv[])
{
	fprintf(stdout, "1NFO: Starting the program, soon I/O will be set..\n");
	//signal(SIGINT, termination_handler);

	fsts = stdout;
	ferr = stdout;

	/*
	if (argc != 2) {
		printf("Usage: fifo-reader [fifo-filename]\n");
		exit(1);
	}
	*/
	setvbuf(fsts, NULL, _IONBF, BUFF_SIZE);
	setvbuf(ferr, NULL, _IONBF, BUFF_SIZE);
	fprintf(fsts, "INFO: No buffering on status and error streams is set.\n");

	// char readbuf[FIFO_READLEN];

        /* Create the FIFO if it does not exist */
	/* the filename of the FIFO is comming from the user
	   s/he should take care of it */
        //umask(0);
        //mknod(FIFO_FILE, S_IFIFO|0666, 0);

	fprintf(fsts, "INFO: going to process the commandline options and setup I/O streams,\n");

	fprintf(fsts, "INFO: got options: ");
	fprintf(fsts, "--> ");
	for (int i = 1; i < argc; ++i)
	{
		fprintf(fsts, "%s ", argv[i]);
	}
	fprintf(fsts, "<--\n");

	if (argc == 1) {
		fprintf(fsts, "INFO: going into stdin-stdout setup,\n");
		fin  = stdin;
		fout = stdout;
	}
	else if (argc == 2) {// TODO: add a check for --help, -h argument
		fprintf(fsts, "INFO: going into pipe-stdout setup,\n");
		if( (fin = fopen(argv[1], "r")) == NULL ) {
			char fifo_open_error_report[80];
			sprintf( fifo_open_error_report, "fopen %s", argv[1] );
			perror( fifo_open_error_report );
			exit(1);
		}
		// add a dummy keeper strem if the input is external
		fin_keeper = fopen(argv[1], "w");
		fprintf(fsts, "INFO: a keeper writer is set for input stream,\n");
		fout = stdout;
	}
	else if (argc == 3) {
		if ( strcmp(argv[1], "-") == 0 ) {
			fprintf(fsts, "INFO: going into stdin-pipe setup,\n");
			fin = stdin;
			if( (fout = fopen(argv[2], "w")) == NULL ) {
				char fifo_open_error_report[80];
				sprintf( fifo_open_error_report, "fopen %s", argv[2] );
				perror( fifo_open_error_report );
				exit(1);
			}
		}
		else {
			fprintf(fsts, "INFO: going into pipe-pipe setup,\n");
			if( (fin = fopen(argv[1], "r")) == NULL ) {
				char fifo_open_error_report[80];
				sprintf( fifo_open_error_report, "fopen %s", argv[1] );
				perror( fifo_open_error_report );
				exit(1);
			}
			// add a dummy keeper strem if the input is external
			fin_keeper = fopen(argv[1], "w");
			fprintf(fsts, "INFO: a keeper writer is set for input stream,\n");
			if( (fout = fopen(argv[2], "w")) == NULL ) {
				char fifo_open_error_report[80];
				sprintf( fifo_open_error_report, "fopen %s", argv[2] );
				perror( fifo_open_error_report );
				exit(1);
			}
		}

	}
	setvbuf(fout, NULL, _IONBF, BUFF_SIZE); // TODO: should there be a buffer size for no-buffer?
	fprintf(fsts, "INFO: the I/O streams are connected.\n");
	fprintf(fsts, "INFO: No buffering on output, status and error streams is set.\n");
	fprintf(fout, "TEST output: test-test!\n");

	// 
	PipeHub( fin, fsts, fout, ferr );

	//fclose(fin);
	//fclose(fout);
	return(0);
}

/*
// getting double free error here
void termination_handler( int signum )
{
	fprintf(fsts, "INFO: Terminating the program..\n");
	fclose(fin);
	fclose(fout);
	fclose(ferr);
	fclose(fsts);
	fprintf(stdout, "INFO: I/O closed..\n");
	fprintf(stdout, "INFO: Bye.\n");
}
*/

