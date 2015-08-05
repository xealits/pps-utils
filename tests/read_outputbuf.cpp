#include <stdio.h>
#include <stdint.h> // uint32_t etc -- standardized integers
#include <stdlib.h>
#include <string.h> // memset

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)






int main(int argc, char *argv[]) {
/*
if (argc!=2) return 1;
else{
    //uint16_t register_address = atoi(argv[1]);
    uint16_t register_address; 
    sscanf(argv[1], "%x", &register_address);
    printf("Got register address: 0x%04x (decimal -- %d)\nStatus register:0x%04x\n", register_address, register_address, kStatus);
*/

    VME::BridgeVx718 * fBridge = new VME::BridgeVx718("/dev/a2818_0", VME::CAEN_V2718);

    int32_t bridge_handle = fBridge->GetHandle();
    printf("VME Bridge handle ID: %08x\n", bridge_handle);

    uint32_t tdcboard_base_address = 0x00aa0000;
    printf("CAEN TDC board baseaddress: %08x\n", tdcboard_base_address);

    // READING OutputBuffer
    uint32_t* fBuffer;
    fBuffer = (uint32_t *)malloc(16*1024*1024); // 16Mb of buffer!
    memset(fBuffer, 0, sizeof(uint32_t)); // fill the buffer with 0
    const int blts = 1024;
    int count=0;
    CVErrorCodes ret;
    // am_blt = cvA32_U_BLT
    //


    while (1) {
        ret = CAENVME_BLTReadCycle(bridge_handle, tdcboard_base_address + kOutputBuffer, (char*)fBuffer, blts, cvA32_U_BLT, cvD32, &count);

        // ret

        printf("Output block:\n");
        for (int i=0; i<count/4; i++) { // FIXME need to use the knowledge of the TDCEvent behaviour there...
            //TDCEvent ev(fBuffer[i]);
            //if (ev.GetType()==TDCEvent::Filler) continue; // Filter out filler data
            //ec.push_back(ev);
            printf("%08x\n", fBuffer[i]);
        }
    }

//    }

}

