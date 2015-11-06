#include <stdio.h> // fprintf, FILE, sscanf
// here one should have a CAEN header as well

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include <string.h> // strlen, strcmp


#define COMMAND_NAME_LEN 32
#define COMMAND_HELP_LEN 256
#define COMMAND_RETURN_LEN 32
#define NUM_COMMANDS 4


typedef char * (* ParseParams_n_CallCAEN)(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err );


// typedef struct caen_call
// {
// 	const char command_name[COMMAND_NAME_LEN];
// 	const ParseParams_n_CallCAEN command_proc;
// 	const char command_help[COMMAND_HELP_LEN];
// } caen_call;





char read_block_cycle_name[COMMAND_NAME_LEN] = "read_block_cycle";
char * read_block_cycle_proc(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
char read_block_cycle_help[COMMAND_HELP_LEN] = "TODO";

// static caen_call read_block_cycle = {
// 	.command_name = "read_block_cycle",
// 	.command_proc = read_block_cycle_proc,
// 	.command_help = "TOD"
// };

CVAddressModifier modifier_from_ints[3][2][4] = {
	{
		{cvA16_S, cvA16_S, cvA16_S, cvA16_S},
		{cvA16_U, cvA16_U, cvA16_U, cvA16_U}
	},
	{
		{cvA24_S_BLT, cvA24_S_PGM, cvA24_S_DATA, cvA24_S_MBLT},
		{cvA24_U_BLT, cvA24_U_PGM, cvA24_U_DATA, cvA24_U_MBLT}
	},
	{
		{cvA32_S_BLT, cvA32_S_PGM, cvA32_S_DATA, cvA32_S_MBLT},
		{cvA32_U_BLT, cvA32_U_PGM, cvA32_U_DATA, cvA32_U_MBLT}
	}
};

CVDataWidth datawidth_from_ints[4] = {
	cvD8, cvD16, cvD32, cvD64
};


char read_cycle_name[COMMAND_NAME_LEN] = "read_cycle";
char * read_cycle_proc(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	CAENVME_API call_res;
	uint32_t address;

	// CVAddressModifier address_mod = cvA32_U_DATA; // default VME address modifier, 32ud
	CVAddressModifier address_mod;
	int b = 2, p = 1, m = 2; // = 32 u d = cvA32_U_DATA
	address_mod = modifier_from_ints[b][p][m]; // default VME address modifier, 32ud
	uint band; // 16, 24, 32
	band = b * 8 + 16;
	char priv; // u, s
	char mode; // d, m, b, p
	char address_mod_str[4];

	CVDataWidth data_width = cvD16; // default VME data width specifier, 16
	uint width = 16; // actual input, actual 8, 16, 32 or 64
	uint width_num_bytes = 2; // input / 8 -- in bytes: 1, 2, 4 or 8
	unsigned char bytes_to_read[8]; // 8, 16, 32 or 64 bits

	int pars_num;

	pars_num = sscanf(command_parameters, "%8x %4s %2d", &address, address_mod_str, &width);

	if ( pars_num < 1 )
	{
		fprintf(stream_err, "\tCAENVMECalls err: got no propper input, no address is provided.\n");
		fprintf(stream_out, "\tCAENVMECalls out: got no propper input, no address is provided.\n");
		return("command_fault");
	}
	else if ( pars_num < 2  )
	{
		// fprintf(stream_err, "\tCAENVMECalls err: got no propper input.\n");
		fprintf(stream_out, "\tCAENVMECalls out: got only address, calling with defaults 32ud (%d %d %d) 16 (%d),\n", b, p, m, width_num_bytes);
		// return("command_fault");
	}
	else
	{
		// checking address modifier input
		if ( strcmp(address_mod_str, "-")==0 )
		{
			fprintf(stream_out, "\tCAENVMECalls out: calling with default address modifier 32ud (%d %d %d),\n", b, p, m);
		}
		else
		{
			pars_num = sscanf(address_mod_str, "%2d%c%c", &band, &priv, &mode);
			if ( band == 16 || band == 24 || band == 32 )
			{
				b = (band - 16)/8;
			}

			if ( priv == 's' ) p = 0;
			else if ( priv == 'u' ) p = 1;
			else fprintf(stream_out, "\tCAENVMECalls out: using default u (%d = 0) for privilege specifier,\n", p);
		
			if      ( mode == 'b' ) m = 0;
			else if ( mode == 'p' ) m = 1;
			else if ( mode == 'd' ) m = 2;
			else if ( mode == 'm' ) m = 3;
			else fprintf(stream_out, "\tCAENVMECalls out: using default d (%d = 0) for mode specifier,\n", m);

			fprintf(stream_out, "\tCAENVMECalls out: (user input %d %c %c) the address modifier is %d %d %d,\n", band, priv, mode, b, p, m);
		}

		address_mod = modifier_from_ints[b][p][m]; // default VME address modifier, 32ud


		if ( pars_num > 4  )
		{
			// checking data width input
			if ( width == 8 || width == 16 || width == 32 || width == 64 )
			{
				width_num_bytes = width / 8;
				data_width = datawidth_from_ints[width_num_bytes - 1];
			}
			else fprintf(stream_out, "\tCAENVMECalls out: the data width input is unknown, using the default %d (= 16),\n", width_num_bytes*8);
			// return("command_fault");
		}
	}

	if (address_mod == cvA32_U_DATA)
	{
		fprintf(stream_err, "\terrINFO: CAENVMECall with default cvA32_U_DATA,\n");
	}
	if (data_width == cvD16)
	{
		fprintf(stream_err, "\terrINFO: CAENVMECall with default cvD16,\n");
	}

	// fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	// fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	call_res = CAENVME_ReadCycle( bridge_handler, address, bytes_to_read, address_mod, data_width );
	// TODO: check call_res
	for (int i = 0; i < width_num_bytes; ++i)
	{
		// TODO: this is really bad for performance
		fprintf(stream_out, "%x", bytes_to_read[i]);
	}
	fprintf(stream_out, "\n");
	fprintf(stream_err, "\tCAENVMECalls err: %s\n", "N0NE");
	return("all_ok");
}
char read_cycle_help[COMMAND_HELP_LEN] = "read_cycle <address> [<address mode> [<data width>]]\n\t32bit VME adress, (16|24|32)(u|s)(b|p|d|m), 8|16|32|64,\n\tdefaults 32ud 16\n\truns VME readcycle, returns nothing.\n";

// static caen_call read_cycle = {
// 	.command_name = "read_cycle",
// 	.command_proc = read_cycle_proc,
// 	.command_help = "TOD"
// };



char write_cycle_name[COMMAND_NAME_LEN] = "write_cycle";
char * write_cycle_proc(int32_t bridge_handler, char * command_parameters, FILE * stream_out, FILE * stream_err )
{
	fprintf(stream_out, "CAENVMECalls out: %s\n", "DONE");
	fprintf(stream_err, "CAENVMECalls err: %s\n", "NONE");
	return("all_ok");
}
char write_cycle_help[COMMAND_HELP_LEN] = "TODO";


// static caen_call write_cycle = {
// 	.command_name = "write_cycle",
// 	.command_proc = write_cycle_proc,
// 	.command_help = "TOD"
// };



char read_bridge_fw_name[COMMAND_NAME_LEN] = "read_bridge_fw";
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
char read_bridge_fw_help[COMMAND_HELP_LEN] = "read_bridge_fw\n\tno parameters,\n\ton success returns firmware version of the board.\n";

// static caen_call read_bridge_fw = {
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
char * CAENVME_help_proc( char * command_parameters,
	FILE * stream_sts,
	FILE * stream_out,
	FILE * stream_err )
{
	char command_name[COMMAND_NAME_LEN];
	if ( sscanf(command_parameters, "%s", command_name) < 1 )
	{
		/* print all help */
		fprintf(stream_sts, "(To exit enter quit or exit.)\n");
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
	/* if the commandname was not found -- check if it exit or quit or report */
	if ( i == NUM_COMMANDS )
	{
		if ( strcmp(command_name, "quit") == 0 || strcmp(command_name, "exit") == 0 )
		{
			fprintf(stream_sts, "Exiting..\n");
			CAENVME_API call_res;
			// fclose(stream_sts);
			// fclose(stream_out);
			// fclose(stream_err);
			fprintf(stdout, "!NFO: I/O closed..\n");
			call_res = CAENVME_End( bridge_handler );
			fprintf(stdout, "!NFO: CAENVME_END called...\n");
			fprintf(stdout, "!NFO: Bye.\n");
			exit(0); // I hope in exits the main program
		}
		fprintf(stream_out, "commandname %s was not found\n", command_name);
		ret = "no_action";
	}


	return(ret);
}
