#include <stdio.h>
#include <stdint.h>

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"

#include "CAEN_VME_TDC_addresses.h" // listing of addresses on TDC board (for instance kStatus)






uint16_t read_tdc_register(uint32_t tdcboard_base_address, uint16_t reg_address) {

VME::BridgeVx718 * fBridge = new VME::BridgeVx718("/dev/a2818_0", VME::CAEN_V2718);

int32_t bridge_handle = fBridge->GetHandle();

// uint32_t tdcboard_base_address = 0x00aa0000;

// READING Register
uint16_t value;
CAENVME_ReadCycle(bridge_handle, tdcboard_base_address + reg_address, &value, cvA32_U_DATA, cvD16);

printf("%d\n", value);

return value;
}

