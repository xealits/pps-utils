#include <stdio.h>

#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include "VME_BridgeVx718.h"



void main() {

vme = new VMEReader("/dev/a2818_0", VME::CAEN_V2718, with_socket);
	vme{ fBridge = new VME::BridgeVx718(device, type); 
             enum BridgeType { CAEN_V1718, CAEN_V2718 };   }
const uint32_t tdc_address = 0x00aa0000; // V1290A (32 ch., CERN)
vme->AddTDC(tdc_address);
// TOCHECK: does a TDC require some initialization procedure?
// Or it just stores config data (fHandle etc)?
// How big is initialization procedure? Should one use TDC Class?
// ANSWERS.
// Everything needed for CAENVME_ calls to VME bus is stored.
	VMEReader::AddTDC(uint32_t address)
	{
	   VME::TDCV1x90* tdc = new VME::TDCV1x90(fBridge->GetHandle(), address, VME::TRIG_MATCH, VME::TRAILEAD);
		{   TDCV1x90::TDCV1x90(int32_t bhandle, uint32_t baseaddr, acq_mode acqm, det_mode detm) :
		    fBaseAddr(baseaddr), fHandle(bhandle),
		    am(cvA32_U_DATA), am_blt(cvA32_U_BLT)
		    {...}   }
	   tdc->GetFirmwareRev();
	   fTDCCollection.insert(std::pair<uint32_t,VME::TDCV1x90*>(address, tdc));
	}

tdc = vme->GetTDC(tdc_address);
ec = tdc->FetchEvents(); (CAENVME_BLTReadCycle) | TDCV1x90::WriteRegister (CAENVME_ReadCycle)  ...etc
	// TOCHECK: do these functions just put all configuration into CAENVME_* function call and handle errors?
	// Any other functionality? How many CAENVME_* functions are there?
	// ANSWERS.
	//    3 functions are used (at the moment): CAENVME_ReadCycle, CAENVME_WriteCycle, CAENVME_BLTReadCycle
	//    the functionality -- yes, for the moment it is just error handling
	void
	TDCV1x90::ReadRegister(mod_reg addr, uint16_t* data) const
	{
	   uint32_t address = fBaseAddr+addr;
	   if (CAENVME_ReadCycle(fHandle, address, data, am, cvD16)!=cvSuccess) {
	      std::ostringstream o; o << "Impossible to read register at 0x" << std::hex << addr;
	      throw Exception(__PRETTY_FUNCTION__, o.str(), JustWarning);
	   }
	}

}

