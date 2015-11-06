#include <stdio.h> // fprintf, FILE
// here one should have a CAEN header as well

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include <string.h> // strlen, strcmp


#define COMMAND_NAME_LEN 32
#define COMMAND_HELP_LEN 128
#define COMMAND_RETURN_LEN 32
#define NUM_COMMANDS 5


typedef char * (* ParseParams_n_CallCAEN)( char * command_parameters, FILE * stream_out, FILE * stream_err );


// typedef struct caen_call
// {
// 	const char command_name[COMMAND_NAME_LEN];
// 	const ParseParams_n_CallCAEN command_proc;
// 	const char command_help[COMMAND_HELP_LEN];
// } caen_call;


const char read_block_cycle_name[COMMAND_NAME_LEN] = "read_block_cycle";
char * read_block_cycle_proc( char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
const char read_block_cycle_help[COMMAND_HELP_LEN] = "TODO";

// static const caen_call read_block_cycle = {
// 	.command_name = "read_block_cycle",
// 	.command_proc = read_block_cycle_proc,
// 	.command_help = "TOD"
// };


const char read_cycle_name[COMMAND_NAME_LEN] = "read_cycle";
char * read_cycle_proc( char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
const char read_cycle_help[COMMAND_HELP_LEN] = "TODO";

// static const caen_call read_cycle = {
// 	.command_name = "read_cycle",
// 	.command_proc = read_cycle_proc,
// 	.command_help = "TOD"
// };



const char write_cycle_name[COMMAND_NAME_LEN] = "write_cycle";
char * write_cycle_proc( char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
const char write_cycle_help[COMMAND_HELP_LEN] = "TODO";


// static const caen_call write_cycle = {
// 	.command_name = "write_cycle",
// 	.command_proc = write_cycle_proc,
// 	.command_help = "TOD"
// };

const char help_name[COMMAND_NAME_LEN] = "help";
char * help_proc( char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
const char help_help[COMMAND_HELP_LEN] = "TODO";

// static const caen_call help = {
// 	.command_name = "help",
// 	.command_proc = help_proc,
// 	.command_help = "TOD"
// };


const char read_bridge_fw_name[COMMAND_NAME_LEN] = "read_bridge_fw";
char * read_bridge_fw_proc( char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
const char read_bridge_fw_help[COMMAND_HELP_LEN] = "TODO";

// static const caen_call read_bridge_fw = {
// 	.command_name = "read_bridge_fw",
// 	.command_proc = read_bridge_fw_proc,
// 	.command_help = "TOD"
// };




char * command_names[NUM_COMMANDS] = {
	read_block_cycle_name, read_cycle_name, write_cycle_name,
	help_name, read_bridge_fw_name
};

ParseParams_n_CallCAEN command_procs[NUM_COMMANDS] = {
	read_block_cycle_proc, read_cycle_proc, write_cycle_proc,
	help_proc, read_bridge_fw_proc
};

char * command_helps[NUM_COMMANDS] = {
	read_block_cycle_help, read_cycle_help, write_cycle_help,
	help_help, read_bridge_fw_help
};



// static const caen_call caen_calls_commands[NUM_COMMANDS] = {
// 	read_block_cycle, read_cycle, write_cycle,
// 	help, read_bridge_fw
// };



// char ret[COMMAND_RETURN_LEN];
char * ret;

char * CAENVMECall( char * command_name, char * command_parameters, FILE * stream_out, FILE * stream_err )
{

	fprintf(stream_out, "CAENVMECalls got: command : %s, parameters : %s\n", command_name, command_parameters);
	// fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	// fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");

	for (int i = 0; i < NUM_COMMANDS; ++i)
	{
		// if (strcmp(command_name, caen_calls_commands[i].command_name) == 0)
		// {
			// ret = caen_calls_commands[i].command_proc( command_parameters, stream_out, stream_err );
			// break;
		// }
		if (strcmp(command_name, command_names[i]) == 0)
		{
			ret = command_procs[i]( command_parameters, stream_out, stream_err );
			break;
		}
	}

	return(ret);
}
