#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
//#include <map>
//#include <std.h>
using namespace std;
//using std::string;

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)


#define MAX_INPUT_SIZE 256

VME::BridgeVx718 * bridge;
int32_t bridge_handle;

void print_vme_text_protocol_help( void );


struct CAENlib_VME_Call // True only for some calls, For ReadCycle and WriteCycle for instance
 {
    //CAENVME_API (* call)(long Handle, unsigned long Address, void * Data, CVAddressModifier AM, CVDataWidth DW);
    CAENVME_API (* parse_and_call)(char* arguments);
    string helpstr;
 } read_cycle;

CAENVME_API parse_CAENVME_ReadCycle(char* arguments);

map<string, CAENlib_VME_Call> CAENlib_VME_Calls;



int main(int argc, char *argv[]) {

read_cycle.parse_and_call = parse_CAENVME_ReadCycle;
read_cycle.helpstr = "Performs a single VME read cycle.\nTakes VME bus address. Returns the content.\n";

CAENlib_VME_Calls["readcycle"] = read_cycle;

if (argc!=2){
     printf("One argument is required -- VME bridge device filename.\n");
     return 1;
    }
else{
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
    printf("Initialized the VME Bridge at handle ID: %08x\n", bridge_handle);

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
         else if ( strcmp(input, "help") == 0 ) { print_vme_text_protocol_help(); }
         else if ( strcmp(input, "") == 0 ) { ; }
         else {
               char * pch; // pure C comming in!
               pch = strtok(input, " "); // blank space is the only delimeter in out case
               // pch now points to the first token of the call,
               // it has to be a call name
               if ( CAENlib_VME_Calls.find(pch) == CAENlib_VME_Calls.end() ) {
                   // not found
                   printf("The call is not known.\n");
               } else {
                   // found
                   CAENlib_VME_Calls[pch].parse_and_call( strtok(NULL, "") );
               }              }
         printf (prompt);
    }

    delete bridge;
    }

}



void print_vme_text_protocol_help( void ) {
    printf("HELP_LINES\n");
    for (std::map<string, CAENlib_VME_Call>::iterator iter=CAENlib_VME_Calls.begin(); iter!=CAENlib_VME_Calls.end(); iter++ ) {
        cout << iter->first << ": " << iter->second.helpstr << endl;
    }
}


CAENVME_API parse_CAENVME_ReadCycle(char* arguments){
    // parse string, call CAENVMElib function
    uint32_t address;
    uint16_t value;
    printf("Got arguments:\n%s\n", arguments);
    sscanf (arguments, "%x", str, &address);
    printf("Got address:\n%x\n", address);
    CAENVME_ReadCycle( bridge_handle, address, &value, cvA32_U_DATA, cvD16 );
    printf("Read value:\n%x\n", value);
}

