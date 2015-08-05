#include <stdio.h>
//#include <stdint.h> // standard integers: uint16_t etc
#include <stdlib.h>
#include <string.h> // strtok,
//#include <map>
//#include <std.h>
using namespace std;
//using std::string;

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)

#include "CAENVME_plain_text_control.cpp" // Nobody expects Spanish inquisition!


#define MAX_INPUT_SIZE 256

VME::BridgeVx718 * bridge;
int32_t bridge_handle;

map<string, Text_to_CAENVME_Calls::CAENlib_VME_Call> text_to_calls_map = Text_to_CAENVME_Calls::create_text_to_CAENlib_map();




int main(int argc, char *argv[]) {

if (argc!=2){
     printf("One argument is required -- VME bridge device filename.\n");
     return 1;
    }
else {
    //uint16_t register_address = atoi(argv[1]);
    char bridge_device_filename[100];
    sscanf(argv[1], "%s", bridge_device_filename);
    // sscanf(argv[2], "%x", &register_address);

    printf("Got device filename %s\n", bridge_device_filename);

    // printf("Got register address: 0x%04x (decimal -- %d)\nCAEN TDC Status register:0x%04x\n", register_address, register_address, kStatus);
    // printf("Of board: 0x%08x\n", tdcboard_base_address);


    // the program handles one bridge -- the values are global to whole program
    bridge = new VME::BridgeVx718(bridge_device_filename, VME::CAEN_V2718);
    bridge_handle = bridge->GetHandle();
    * Text_to_CAENVME_Calls::bridge_handler = bridge_handle;
    printf("Initialized the VME Bridge at handle ID: %08x\n", * Text_to_CAENVME_Calls::bridge_handler);
    //CAENVME_plain_text_control text_to_CAENVME_call( bridge_handle );
    //Text_to_CAENVME_Calls::bridge_handle = bridge_handle;

    char input[MAX_INPUT_SIZE];

    char prompt[64] = "Enter the VME Call (or help, quit): ";
    printf (prompt);
    while ( fgets(input, MAX_INPUT_SIZE, stdin) ) { // read stdin, run CAEN call
         //printf ("Enter the VME Call (or help, quit): ");
         //fgets(input, MAX_INPUT_SIZE, stdin);
         if ((strlen(input)>0) && (input[strlen (input) - 1] == '\n')) // removing a newline character from input
            { input[strlen (input) - 1] = '\0'; }
         // scanf ("%63s", input);
         if ( strcmp(input, "quit") == 0) { delete bridge; return 0; }
         else if ( strcmp(input, "help") == 0 ) {
		Text_to_CAENVME_Calls::print_vme_text_protocol_help(text_to_calls_map);
	 }
         else if ( strcmp(input, "") == 0 ) { ; }
	else { //text_to_CAENVME_call.process_text_command( input ); }
		char * pch; // pure C comming in!
		pch = strtok(input, " "); // blank space is the only delimeter in out case
		// pch now points to the first token of the call,
		// it has to be a call name
		if ( text_to_calls_map.find(pch) == text_to_calls_map.end() ) {
			// not found
			printf("The call is not known.\n");
		} else {
			// found
			text_to_calls_map[pch].parse_and_call( strtok(NULL, "") );
		}
	}
	printf (prompt);
    };

    delete bridge;
}

}







