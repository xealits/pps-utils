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
	FWRel[0] = '1', FWRel[1] = '2', FWRel[2] = '3';
	return(res);
}
