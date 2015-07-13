#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)






int main(int argc, char *argv[]) {

    printf("Calling CAENVME_SystemReset on VME bridge\n");

    VME::BridgeVx718 * fBridge = new VME::BridgeVx718("/dev/a2818_0", VME::CAEN_V2718);

    int32_t bridge_handle = fBridge->GetHandle();
    printf("VME Bridge handle ID: %08x\n", bridge_handle);

    // Reset Call
    CAENVME_SystemReset(bridge_handle);

    printf("Reset Done.\n");

}

