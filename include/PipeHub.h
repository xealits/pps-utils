#ifndef PIPEHUB_H_
#define PIPEHUB_H_
#include <stdio.h> // FILE

// stream_in  -- input commands
// stream_sts -- status of the hub
// stream_out -- output data from VME bus
// stream_err -- errors on the bus (TODO: or the CAEN lib?)
// (in principle, errors in the program should be report by regular C means)
// (assuming the program runs without errors, 3 things act in the system:
//   * the input of the user (commands)
//   * the configuration of the hub (i/o streams, buffering, what else) and its' status at the moment
//   * the VME bus, which gets the commands and outputs either data or error code -- each has its' own output stream)

typedef enum Status_Prompt_Levels
{
	all,
	clean
} Status_Prompt_Levels;

typedef struct PipeHub_Parameters
{
	// let's keep pointers to the parameters for now,
	// as if we are running procedures with ifing on parameters all the time
	// later actual procedure pointers should be here
	// and this procedures will be run
	long * VME_device_handler;

	FILE * stream_in;
	FILE * stream_in_keeper; // TODO: maybe keepers should not be here?
	FILE * stream_sts;
	FILE * stream_out;
	FILE * stream_out_keeper;
	FILE * stream_err;

	Status_Prompt_Levels * status_prompt_level;
} PipeHub_Parameters;

// void PipeHub( FILE * stream_in, FILE * stream_sts, FILE * stream_out, FILE * stream_err );
void PipeHub( PipeHub_Parameters * );

#endif