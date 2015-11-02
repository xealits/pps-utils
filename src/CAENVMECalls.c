#include <stdio.h> // fprintf, FILE
// here one should have a CAEN header as well


char * CAENVMECall( char * input_string, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls got: %s\n", input_string);
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");

	return("all_ok");
}
