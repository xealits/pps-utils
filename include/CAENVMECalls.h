#ifndef CAENVMECALLS_H_
#define CAENVMECALLS_H_
#include <stdio.h> // FILE

// input_string -- input string, to be tokenized and turned into a CAENlib VME call
// stream_out   -- output data from VME bus
// stream_err   -- errors on the bus (TODO: or the CAEN lib?)
// (VME bus gets the commands and outputs either data or error code -- each has its' own output stream)
// output is a report string
char * CAENVMECall( int32_t bridge_handler,
	char * command_name,
	char * command_parameters,
	FILE * stream_sts,
	FILE * stream_out,
	FILE * stream_err );

char * CAENVME_help_proc( char * command_parameters,
	FILE * stream_sts,
	FILE * stream_out,
	FILE * stream_err );

#endif