#include <stdio.h> // fprintf, FILE
// here one should have a CAEN header as well


char * CAENVMECall( char * command_name, char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls got: command : %s, parameters : %s\n", command_name, command_parameters);
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");

	return("all_ok");
}
