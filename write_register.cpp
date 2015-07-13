#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)






int main(int argc, char *argv[]) {


if (argc!=3) return 1;
else{
    //uint16_t register_address = atoi(argv[1]);
    uint16_t register_address; 
    uint32_t tdcboard_base_address;// = 0x00aa0000;
    sscanf(argv[1], "%x", &tdcboard_base_address);
    sscanf(argv[2], "%x", &register_address);
    printf("Got register address: 0x%04x (decimal -- %d)\nReset register:0x%04x\n", register_address, register_address, kModuleReset);
    printf("Of board: 0x%08x\n", tdcboard_base_address);


    VME::BridgeVx718 * fBridge = new VME::BridgeVx718("/dev/a2818_0", VME::CAEN_V2718);

    int32_t bridge_handle = fBridge->GetHandle();
    printf("VME Bridge handle ID: %08x\n", bridge_handle);


    // READING Register
    uint16_t value = 0;
    //CAENVME_ReadCycle(bridge_handle, tdcboard_base_address + kStatus, &value, cvA32_U_DATA, cvD16);
    //WriteRegister(kModuleReset, static_cast<uint16_t>(0x0)); } catch (Exception& e) { e.Dump(); }
    //(CAENVME_WriteCycle(fHandle, address, fdata, am, cvD16)!=cvSuccess) {
    CAENVME_WriteCycle(bridge_handle, tdcboard_base_address + register_address, &value, cvA32_U_DATA, cvD16);
    //CAENVME_ReadCycle(bridge_handle, tdcboard_base_address + register_address, &value, cvA32_U_DATA, cvD16);

    printf("Register at 0x%04x of board 0x%08x:\n", register_address, tdcboard_base_address);
    printf("writen value   0x%04x\n", value);
    }

}

