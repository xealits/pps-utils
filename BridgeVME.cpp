#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)


#define MAX_INPUT_SIZE 256

void print_vme_text_protocol_help( void );
void process_input(char *input);


int main(int argc, char *argv[]) {

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


    VME::BridgeVx718 * bridge = new VME::BridgeVx718(bridge_device_filename, VME::CAEN_V2718);

    int32_t bridge_handle = bridge->GetHandle();
    printf("Initialized the VME Bridge at handle ID: %08x\n", bridge_handle);

    char input[MAX_INPUT_SIZE];
    while (1) { // read stdin, run CAEN call
         printf ("Enter the VME Call (or help, quit): ");
         fgets (input, MAX_INPUT_SIZE, stdin);
         if ((strlen(input)>0) && (input[strlen (input) - 1] == '\n'))
         input[strlen (input) - 1] = '\0';
         // scanf ("%63s", input);
         if ( strcmp(input, "quit") = 0) { delete bridge; return 0; }
         else if ( strcmp(input, "help") = 0) { print_vme_text_protocol_help(); }
         else { process_input(input); }
    }

    // READING Register
    // uint16_t value;
    //CAENVME_ReadCycle(bridge_handle, tdcboard_base_address + kStatus, &value, cvA32_U_DATA, cvD16);
    // CAENVME_ReadCycle(bridge_handle, tdcboard_base_address + register_address, &value, cvA32_U_DATA, cvD16);

    // printf("Register at 0x%04x of board 0x%08x:\n", register_address, tdcboard_base_address);
    // printf("value = 0x%04x\n", value);
    delete bridge;
    }

}


// struct CAENlib_VME_call
// {
    // 
// };



void print_vme_text_protocol_help( void ) {
    printf("HELP_LINES\n");
}


void process_input(char *input) {
    printf("Sorry, only 'quit' and 'help' are available now.\n");
}
