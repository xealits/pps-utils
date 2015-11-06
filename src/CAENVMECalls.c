#include <stdio.h> // fprintf, FILE, sscanf
// here one should have a CAEN header as well

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include <string.h> // strlen, strcmp


#define COMMAND_NAME_LEN 32
#define COMMAND_HELP_LEN 128
#define COMMAND_RETURN_LEN 32
#define NUM_COMMANDS 4


typedef char * (* ParseParams_n_CallCAEN)(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err );


// typedef struct caen_call
// {
// 	const char command_name[COMMAND_NAME_LEN];
// 	const ParseParams_n_CallCAEN command_proc;
// 	const char command_help[COMMAND_HELP_LEN];
// } caen_call;


const char read_block_cycle_name[COMMAND_NAME_LEN] = "read_block_cycle";
char * read_block_cycle_proc(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err )
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
char * read_cycle_proc(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err )
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
char * write_cycle_proc(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err )
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



const char read_bridge_fw_name[COMMAND_NAME_LEN] = "read_bridge_fw";
char * read_bridge_fw_proc(int32_t bridge_handler,
	char * command_parameters,
	FILE * stream_out,
	FILE * stream_err )
{
	CAENVME_API call_res;
	char FWRel[64];

	call_res = CAENVME_BoardFWRelease(bridge_handler, FWRel);
	// TODO: check call_res
	fprintf(stream_out, "%s\n", FWRel);
	fprintf(stream_err, "\tCAENVMECalls err: %s\n", "N0NE");
	return("all_ok");
}
const char read_bridge_fw_help[COMMAND_HELP_LEN] = "read_bridge_fw\n\tno parameters,\n\ton success returns firmware version of the board.\n";

// static const caen_call read_bridge_fw = {
// 	.command_name = "read_bridge_fw",
// 	.command_proc = read_bridge_fw_proc,
// 	.command_help = "TOD"
// };




char * command_names[NUM_COMMANDS] = {
	read_block_cycle_name, read_cycle_name,
	write_cycle_name, read_bridge_fw_name
};

ParseParams_n_CallCAEN command_procs[NUM_COMMANDS] = {
	read_block_cycle_proc, read_cycle_proc,
	write_cycle_proc, read_bridge_fw_proc
};

char * command_helps[NUM_COMMANDS] = {
	read_block_cycle_help, read_cycle_help,
	write_cycle_help, read_bridge_fw_help
};

// const char help_name[COMMAND_NAME_LEN] = "help";
// TODO: it seems the help command should output to status stream?
// char * help_proc( char *, FILE *, FILE * );
// const char help_help[COMMAND_HELP_LEN] = "TODO";

// static const caen_call help = {
// 	.command_name = "help",
// 	.command_proc = help_proc,
// 	.command_help = "TOD"
// };

// TODO: it seems the help command should output to status stream?
//       should I separate it from other commands?
char * CAENVME_help_proc(char * command_parameters, FILE * stream_sts, FILE * stream_out, FILE * stream_err )
{
	char command_name[COMMAND_NAME_LEN];
	if ( sscanf(command_parameters, "%s", command_name) < 1 )
	{
		/* print all help */
		for (int i = 0; i < NUM_COMMANDS; ++i)
		{
			fprintf(stream_sts, "%s:\n\t%s\n\n", command_names[i], command_helps[i]);
		}
	
	}
	else
	{
		/* print the help on the given commandname */
		int i = 0;
		for (i = 0; i < NUM_COMMANDS; ++i)
		{
			if (strcmp(command_name, command_names[i]) == 0)
			{
				fprintf(stream_sts, "%s:\n\t%s\n", command_names[i], command_helps[i]);
				break;
			}
		}
		/* if the commandname was not found -- report */
		if ( i == NUM_COMMANDS )
		{
			fprintf(stream_sts, "command %s was not found in help strings\n", command_name);
			fprintf(stream_sts, "help usage:\n\thelp [<commandname>]\nlist of known command names:\n\t");
			// print list of commandnames
			for (int i = 0; i < NUM_COMMANDS - 1; ++i)
			{
				fprintf(stream_sts, "%s, ", command_names[i]);
			}
			fprintf(stream_sts, "%s.\n", command_names[NUM_COMMANDS - 1]);
		}
	}
	// fprintf(stream_sts, "CAENVMECalls out: %s\n", "DONE");
	// fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}

// static const caen_call caen_calls_commands[NUM_COMMANDS] = {
// 	read_block_cycle, read_cycle, write_cycle,
// 	help, read_bridge_fw
// };



// char ret[COMMAND_RETURN_LEN];
char * ret;

char * CAENVMECall( int32_t bridge_handler,
	char * command_name,
	char * command_parameters,
	FILE * stream_sts,
	FILE * stream_out,
	FILE * stream_err )
{

	// the output log should contain the issued commands
	// TODO: but what to do in case of stream reading the boards?
	fprintf(stream_out, "CAENVMECalls got: command : %s, parameters : %s\n", command_name, command_parameters);
	// fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	// fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");

	int i;
	for (i = 0; i < NUM_COMMANDS; ++i)
	{
		// if (strcmp(command_name, caen_calls_commands[i].command_name) == 0)
		// {
			// ret = caen_calls_commands[i].command_proc( command_parameters, stream_out, stream_err );
			// break;
		// }
		if (strcmp(command_name, command_names[i]) == 0)
		{
			ret = command_procs[i](bridge_handler, command_parameters, stream_out, stream_err );
			break;
		}
	}
	/* if the commandname was not found -- report */
	if ( i == NUM_COMMANDS )
	{
		fprintf(stream_out, "commandname %s was not found\n", command_name);
		ret = "no_action";
	}


	return(ret);
}
