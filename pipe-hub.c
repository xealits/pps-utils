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

#include <stdio.h> // FILE, fprintf, fdopen
#include <stdlib.h>
// #include <sys/stat.h>
// #include <unistd.h>

// #include <linux/stat.h>

#include <string.h> // strlen, strcmp
// #include <signal.h> // signal and SIGNINT
#include <fcntl.h> // O_WRONLY, O_NONBLOCK


// #include <include/PipeHub.h>
#include <PipeHub.h>

// for init of the CAEN lib
#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"
#include "stdint.h" // int32_t etc, used as parameters in CAEN lib, for instance in init procedure


//#define FIFO_FILE       "pipe"
#define FIFO_READLEN 80
#define BUFF_SIZE 80



FILE *fin;
int din; // descriptor of in
FILE *fin_keeper;

FILE *fout;
int dout; // descriptor of out
FILE *fout_keeper;

FILE *fsts;
int dsts;
FILE *ferr;
int derr;




// TODO: handle SIGINT?
//void termination_handler( int signum );



int main(int argc, char *argv[])
{
	PipeHub_Parameters initial_parameters;
	Status_Prompt_Levels prompt_level = all;

	initial_parameters.status_prompt_level = & prompt_level;

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
	fprintf(stdout, "1NFO: Status and Erros outputs are set to stdout.\n      No buffering on status and error streams is set.\n");

	// char readbuf[FIFO_READLEN];

        /* Create the FIFO if it does not exist */
	/* the filename of the FIFO is comming from the user
	   s/he should take care of it */
        //umask(0);
        //mknod(FIFO_FILE, S_IFIFO|0666, 0);

	fprintf(stdout, "1NFO: going to process the commandline options and setup I/O streams,\n");

	fprintf(stdout, "1NFO: got options: ");
	fprintf(stdout, "--> ");
	for (int i = 1; i < argc; ++i)
	{
		fprintf(stdout, "%s ", argv[i]);
	}
	fprintf(stdout, "<--\n");

	char error_report[80];

	if ( argc < 2)
	{
		fprintf(stderr, "1NFO: Usage:\n$ pipe-hub <devname> [<instream>] [<outstream>]\n");
		exit(1);
	}
	else {
		// initialize VME_device_handler
		// setup i/o streams
        CVBoardTypes board_type;
        board_type = cvV2718; // TODO: make it accessible
        CVErrorCodes caen_lib_ret;
        int dev = atoi(argv[1]);
        // long dev_handle; // datasheet says long, header -- int32_t
        int32_t dev_handle;
        CAENVME_API ret;

		ret = CAENVME_SWRelease(error_report);
		if (ret!=cvSuccess) {
			sprintf( error_report, "could not get the SW release of CAENVME lib" );
			perror( error_report );
			exit(1);
		}
		fprintf(stdout, "1NFO: SW release of CAENVME lib = %s\n", error_report);

        ret = CAENVME_Init(board_type, 0x0, dev, &dev_handle);
		if (ret!=cvSuccess) {
			sprintf( error_report, "could not initialize CAENVME lib for %s device", argv[1] );
			perror( error_report );
			exit(1);
		}
		fprintf(stdout, "1NFO: initialized CAENVME lib on device %s,\n      device handler = %d\n", argv[1], dev_handle);

        ret = CAENVME_BoardFWRelease(dev_handle, error_report);
		if (ret!=cvSuccess) {
			sprintf( error_report, "could not initialize CAENVME lib for %s device", argv[1] );
			perror( error_report );
			exit(1);
		}
		fprintf(stdout, "1NFO: HW release of CAENVME lib = %s\n", error_report);

		if (argc == 2) {
			fprintf(stdout, "1NFO: going into stdin-stdout setup,\n");
			fin  = stdin;
			fprintf(stdout, "1NFO: the INput stream is set to stdin,\n");
			fout = stdout;
			fprintf(stdout, "1NFO: the OUTput stream is set to stdout,\n");
		}
		else if (argc == 3) { // TODO: add a check for --help, -h argument
			fprintf(stdout, "1NFO: going into pipe-stdout setup,\n");
			if( (fin = fopen(argv[2], "r")) == NULL ) {
				sprintf( error_report, "fopen %s", argv[2] );
				perror( error_report );
				exit(1);
			}
			fprintf(stdout, "1NFO: the INput pipe %s is opened,\n", argv[2]);
			// add a dummy keeper strem if the input is external
			fin_keeper = fopen(argv[2], "w");
			fprintf(stdout, "1NFO: a keeper writer is set for input stream,\n");
			fout = stdout;
			fprintf(stdout, "1NFO: the OUTput stream is set to stdout,\n");
		}
		else if (argc == 4) {
			if ( strcmp(argv[2], "-") == 0 ) {
				fprintf(stdout, "1NFO: going into stdin-pipe setup,\n");
				fin = stdin;
				fprintf(stdout, "1NFO: the INput stream is set to stdin,\n");
				fprintf(stdout, "1NFO: going open pipe (write) and wait until it is opened from other side,\n");
				// if( (fout = fopen(argv[3], "w")) == NULL ) {
				// if ( (dout = open(argv[3], O_WRONLY | O_NONBLOCK)) < 0 ) {
				if ( (dout = open(argv[3], O_WRONLY & (~O_NONBLOCK))) < 0 ) {
				// if ( (dout = open(argv[3], O_WRONLY )) < 0 ) {
					fprintf( stdout, "open %s = %d", argv[3], dout );
					exit(1);
				}
				// fprintf( stdout, "open %s file-descr = %d", argv[3], dout );
				if( (fout = (FILE*) fdopen(dout, "w")) == NULL ) {
					sprintf( error_report, "fdopen %d (file-descr)", dout );
					perror( error_report );
					exit(1);
				}
				fout_keeper = fopen(argv[3], "r");
				fprintf(stdout, "1NFO: a keeper reader is set for output stream,\n");
				fprintf(stdout, "1NFO: the OUTput pipe %s is opened,\n", argv[3]);
			}
			else {
				fprintf(stdout, "1NFO: going into pipe-pipe setup,\n");
				fprintf(stdout, "1NFO: going open pipes (read-write) and wait until they are opened from other side,\n");
				if ( (din = open(argv[2], O_RDONLY & (~O_NONBLOCK))) < 0 ) {
					fprintf( stdout, "open %s = %d", argv[3], dout );
					exit(1);
				}
				if( (fin = (FILE*) fdopen(din, "r")) == NULL ) {
					sprintf( error_report, "fopen %s", argv[2] );
					perror( error_report );
					exit(1);
				}
				/*
				if( (fin = fopen(argv[2], "r")) == NULL ) {
					sprintf( error_report, "fopen %s", argv[2] );
					perror( error_report );
					exit(1);
				}
				*/
				// add a dummy keeper strem if the input is external
				fprintf(stdout, "1NFO: the INput pipe %s is opened,\n", argv[2]);
				int _open_flag_write_and_blocking = O_WRONLY & (~O_NONBLOCK);
				// int _open_flag_write = O_WRONLY;
				// if ( (dout = open(argv[3],  O_WRONLY )) < 0 ) {
				if ( (dout = open(argv[3], O_WRONLY & (~O_NONBLOCK))) < 0 ) {
					fprintf( stdout, "open %s = %d", argv[3], dout );
					exit(1);
				}
				if( (fout = (FILE*) fdopen(dout, "w")) == NULL ) {
					sprintf( error_report, "fdopen %s", argv[3] );
					perror( error_report );
					exit(1);
				}
				fprintf(stdout, "1NFO: the OUTput pipe %s is opened,\n", argv[3]);
				fin_keeper = fopen(argv[2], "w");
				fprintf(stdout, "1NFO: a keeper writer is set for input stream,\n");
				fout_keeper = fopen(argv[3], "r");
				fprintf(stdout, "1NFO: a keeper reader is set for output stream,\n");
			}

		}
		else
		{
			fprintf(stderr, "1NFO: Usage:\n$ pipe-hub <devname> [<instream>] [<outstream>]\n");
			exit(1);
		}
	}
	setvbuf(fout, NULL, _IONBF, BUFF_SIZE); // TODO: should there be a buffer size for no-buffer?
	fprintf(fsts, "INFO: the I/O streams are connected.\n");
	fprintf(fsts, "INFO: No buffering on output, status and error streams is set.\n");
	fprintf(fout, "TEST output: test-test!\n");

	// packing the streams into the PipeHub parameters structure and running the procedure
	initial_parameters.stream_in = fin;
	initial_parameters.stream_in_keeper = fin_keeper;
	initial_parameters.stream_sts = fsts;
	initial_parameters.stream_out = fout;
	initial_parameters.stream_out_keeper = fout_keeper;
	initial_parameters.stream_err = ferr;
	PipeHub( &initial_parameters );

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

