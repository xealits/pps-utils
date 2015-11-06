#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"
#include "CAENVMElib.h"

#include "stdint.h"

CAENVME_API CAENVME_SWRelease(char *SwRel) {
	CAENVME_API res = cvSuccess;
	SwRel[0] = '1', SwRel[1] = '2', SwRel[2] = '3';
	return(res);
}

CAENVME_API CAENVME_Init(CVBoardTypes BdType, short Link, short BdNum, int32_t *Handle){
	CAENVME_API res;
	res = cvSuccess;
	return(res);
}

// CAENVME_API CAENVME_BoardFWRelease(long handle, char *FWRel) {
CAENVME_API CAENVME_BoardFWRelease(int32_t handle, char *FWRel) {
	CAENVME_API res = cvSuccess;
	FWRel[0] = '1', FWRel[1] = '2', FWRel[2] = '3', FWRel[3] = '\0';
	return(res);
}

CAENVME_API CAENVME_ReadCycle( int32_t bridge_handler, uint32_t address, void * Data, CVAddressModifier address_mod, CVDataWidth data_width ) {
	CAENVME_API res = cvSuccess;
	unsigned char * bytes_to_read = Data;
	bytes_to_read[0] = 128, bytes_to_read[1] = 64, bytes_to_read[2] = 32, bytes_to_read[3] = 255;
	bytes_to_read[4] = 1, bytes_to_read[5] = 255, bytes_to_read[6] = 32, bytes_to_read[7] = 16;
	return(res);	
}

CAENVME_API CAENVME_End( int32_t bridge_handler ) {
	CAENVME_API res = cvSuccess;
	return(res);
}

