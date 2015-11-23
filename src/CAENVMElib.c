#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"
#include "CAENVMElib.h"

#include "stdint.h"
#include "stdio.h"


unsigned char generate_a_byte(uint32_t n)
{
	unsigned char c;
	// c = (n*n*n + 23*n + 776) % 256;
	c = n % 256;

	return c;
}

CAENVME_API CAENVME_SWRelease(char *SwRel) {
	CAENVME_API res = cvSuccess;
	SwRel[0] = '1', SwRel[1] = '2', SwRel[2] = '3';
	return(res);
}

// CAENVME_API CAENVME_BoardFWRelease(long handle, char *FWRel) {
CAENVME_API CAENVME_BoardFWRelease(int32_t handle, char *FWRel) {
	CAENVME_API res = cvSuccess;
	FWRel[0] = '\11', FWRel[1] = '\22', FWRel[2] = '\33', FWRel[3] = '\0';
	return(res);
}


CAENVME_API
    CAENVME_DriverRelease(int32_t Handle, char *Rel);
CAENVME_API
    CAENVME_DeviceReset(int32_t dev);



CAENVME_API CAENVME_Init(CVBoardTypes BdType, short Link, short BdNum, int32_t *Handle){
	CAENVME_API res;
	res = cvSuccess;
	return(res);
}

CAENVME_API CAENVME_End( int32_t bridge_handler ) {
	CAENVME_API res = cvSuccess;
	return(res);
}

/*
CAENVME_API CAENVME_ReadCycle( int32_t bridge_handler,
							   uint32_t address,
							   void * Data,
							   CVAddressModifier address_mod,
							   CVDataWidth data_width ) {
	CAENVME_API res = cvSuccess;
	unsigned char * bytes_to_read = Data;
	// TODO: are these ints really converted to bytes, i.e. unsigned chars?
	bytes_to_read[0] = 128, bytes_to_read[1] = 64, bytes_to_read[2] = 32, bytes_to_read[3] = 255;
	bytes_to_read[4] = 1, bytes_to_read[5] = 255, bytes_to_read[6] = 32, bytes_to_read[7] = 16;
	return(res);	
}
*/


CAENVME_API CAENVME_ReadCycle(int32_t Handle, uint32_t Address, void *Data,
                      CVAddressModifier AM, CVDataWidth DW)
{
	unsigned char * bytes_to_read = Data;
	// for (int i = 0; bytes_to_read[i]!='\0'; ++i)
	int i = 0;
	for (i = 0; i<(DW%16); ++i)
	{
		bytes_to_read[i] = (unsigned char) i + 5;
	// i++;
	// bytes_to_read[i] = (unsigned char) i + 5;
	// i++;
	}
	// printf("%d\n", i);
	// for (int i = 0; i < (DW%16); ++i)
	// for (int i = 0; i < (DW); ++i)
	// {
		// bytes_to_read[i] = i;//generate_a_byte(i);
	// }
	// bytes_to_read[0] = 1, bytes_to_read[1] = 125, bytes_to_read[2] = 2;
	// bytes_to_read[3] = 1, bytes_to_read[4] = 125, bytes_to_read[5] = 2;
	CAENVME_API res = cvSuccess;
	return res;
}

CAENVME_API CAENVME_RMWCycle(int32_t Handle, uint32_t Address,  void *Data,
                     CVAddressModifier AM, CVDataWidth DW)
{
	// TODO: figure what does CAEN's operation do here???
	CAENVME_API res = cvSuccess;
	return res;
}


CAENVME_API CAENVME_WriteCycle(int32_t Handle, uint32_t Address, void *Data,
                       CVAddressModifier AM, CVDataWidth DW)
{
	CAENVME_API res = cvSuccess;
	return res;

}

CAENVME_API CAENVME_MultiRead(int32_t Handle, uint32_t *Addrs, uint32_t *Buffer,
                      int NCycles, CVAddressModifier *AMs, CVDataWidth *DWs, CVErrorCodes *ECs)
{
	// TODO: why the hell is Buffer uint32_t???? Why not bytes? Max data width is 64bits!?
	// unsigned char * bytes_to_read = Data;
	// for (int i = 0; bytes_to_read[i]!='\0'; ++i)
	// int i = 0;
	for (int i = 0; i < NCycles; ++i)
	{
		Buffer[i] = 5 + (DWs[i] << 16); // shift the submitted width to the high half of uint32
		/*for (u = 0; u<(DW[i]%16); ++u)
		{
			bytes_to_read[u] = (unsigned char) u + 5;
		}*/
		ECs[i] = cvSuccess;
	}

	CAENVME_API res = cvSuccess;
	return res;

}


CAENVME_API CAENVME_MultiWrite(int32_t Handle, uint32_t *Addrs, uint32_t *Buffer,
                       int NCycles, CVAddressModifier *AMs, CVDataWidth *DWs, CVErrorCodes *ECs)
{
	CAENVME_API res = cvSuccess;
	return res;

}

/*
      CAENVME_BLTReadCycle
      -----------------------------------------------------------------------------
      Parameters:
      [in]  Handle    : The handle that identifies the device.
      [in]  Address   : The VME bus address.
      [out] Buffer    : The data read from the VME bus.
      [in]  Size      : The size of the transfer in bytes.
      [in]  AM        : The address modifier (see CVAddressModifier enum).
      [in]  DW        : The data width.(see CVDataWidth enum).
      [out] count     : The number of bytes transferred.
      -----------------------------------------------------------------------------
      Returns:
      An error code about the execution of the function.
      -----------------------------------------------------------------------------
      Description:
      The function performs a VME block transfer read cycle. It can be used to
      perform MBLT transfers using 64 bit data width.
    */
CAENVME_API CAENVME_BLTReadCycle(int32_t Handle, uint32_t Address, void *Buffer,
                         int Size, CVAddressModifier AM, CVDataWidth DW, int *count)
{
	unsigned char * bytes_to_read = Buffer;
	int data_width_in_bytes = DW%16;
	*count = 0;
	for (int i = 0; i < Size; ++i)
	{
		for (int u = 0; u < data_width_in_bytes; ++u)
		{
			bytes_to_read[i*data_width_in_bytes+u] = 1 + i + u;
		}
		*count += 1;
	}
	CAENVME_API res = cvSuccess;
	return res;

}

/*
      Ver. 2.3 - New function

      CAENVME_FIFOBLTReadCycle
      -----------------------------------------------------------------------------
      Parameters:
      [in]  Handle    : The handle that identifies the device.
      [in]  Address   : The VME bus address.
      [out] Buffer    : The data read from the VME bus.
      [in]  Size      : The size of the transfer in bytes.
      [in]  AM        : The address modifier (see CVAddressModifier enum).
      [in]  DW        : The data width.(see CVDataWidth enum).
      [out] count     : The number of bytes transferred.
      -----------------------------------------------------------------------------
      Returns:
      An error code about the execution of the function.
      -----------------------------------------------------------------------------
      Description:
      The function performs a VME block transfer read cycle. It can be used to
      perform MBLT transfers using 64 bit data width. The Address is not 
      incremented on the VMEBus during the cycle. 
    */
CAENVME_API CAENVME_FIFOBLTReadCycle(int32_t Handle, uint32_t Address, void *Buffer,
                             int Size, CVAddressModifier AM, CVDataWidth DW, int *count)
{
	// TODO: figure what is the difference between FIFOBLT and BLT???
	//       AHA! the usual block-access on VME
	//       involves incremention of the address on SLAVE side
	//       as if you access RAM,
	//       but when the device behaves as a FIFO
	//       it automatically outputs next in the FIFO valu
	//       at the same address.
	//       Thus no address increment during the cycle.
	unsigned char * bytes_to_read = Buffer;
	int data_width_in_bytes = DW%16;
	*count = 0;
	for (int i = 0; i < Size; ++i)
	{
		for (int u = 0; u < data_width_in_bytes; ++u)
		{
			bytes_to_read[i*data_width_in_bytes+u] = 1 + i + u;
		}
		*count += 1;
	}
	CAENVME_API res = cvSuccess;
	return res;
}


/*
      CAENVME_MBLTReadCycle
      -----------------------------------------------------------------------------
      Parameters:
      [in]  Handle    : The handle that identifies the device.
      [in]  Address   : The VME bus address.
      [out] Buffer    : The data read from the VME bus.
      [in]  Size      : The size of the transfer in bytes.
      [in]  AM        : The address modifier (see CVAddressModifier enum).
      [out] count     : The number of bytes transferred.
      -----------------------------------------------------------------------------
      Returns:
      An error code about the execution of the function.
      -----------------------------------------------------------------------------
      Description:
      The function performs a VME multiplexed block transfer read cycle.
    */
CAENVME_API CAENVME_MBLTReadCycle(int32_t Handle, uint32_t Address, void *Buffer,
                          int Size, CVAddressModifier AM, int *count)
{
	// TODO: Figure out how it works. And why MultiblexedBLT does not have DataWidth modifier?
	unsigned char * bytes_to_read = Buffer;
	// int data_width_in_bytes = DW%16;
	*count = 0;
	for (int i = 0; i < Size; ++i)
	{
		bytes_to_read[i] = 1 + i;
		// for (int u = 0; u < data_width_in_bytes; ++u)
		// {
			// bytes_to_read[i*data_width_in_bytes+u] = 1 + i + u;
		// }
		*count += 1;
	}
	CAENVME_API res = cvSuccess;
	return res;

}

/*
      Ver. 2.3 - New function
        
      CAENVME_FIFOMBLTReadCycle
      -----------------------------------------------------------------------------
      Parameters:
      [in]  Handle    : The handle that identifies the device.
      [in]  Address   : The VME bus address.
      [out] Buffer    : The data read from the VME bus.
      [in]  Size      : The size of the transfer in bytes.
      [in]  AM        : The address modifier (see CVAddressModifier enum).
      [out] count     : The number of bytes transferred.
      -----------------------------------------------------------------------------
      Returns:
      An error code about the execution of the function.
      -----------------------------------------------------------------------------
      Description:
      The function performs a VME multiplexed block transfer read cycle.
      The Address is not incremented on the VMEBus during the cycle. 
    */
CAENVME_API CAENVME_FIFOMBLTReadCycle(int32_t Handle, uint32_t Address, void *Buffer,
                              int Size, CVAddressModifier AM, int *count)
{
	// TODO: and what is this?
	unsigned char * bytes_to_read = Buffer;
	// int data_width_in_bytes = DW%16;
	*count = 0;
	for (int i = 0; i < Size; ++i)
	{
		bytes_to_read[i] = 1 + i;
		// for (int u = 0; u < data_width_in_bytes; ++u)
		// {
			// bytes_to_read[i*data_width_in_bytes+u] = 1 + i + u;
		// }
		*count += 1;
	}
	CAENVME_API res = cvSuccess;
	return res;
}

/*
      CAENVME_BLTWriteCycle
      -----------------------------------------------------------------------------
      Parameters:
      [in]  Handle    : The handle that identifies the device.
      [in]  Address   : The VME bus address.
      [in]  Buffer    : The data to be written to the VME bus.
      [in]  Size      : The size of the transfer in bytes.
      [in]  AM        : The address modifier (see CVAddressModifier enum).
      [in]  DW        : The data width.(see CVDataWidth enum).
      [out] count     : The number of bytes transferred.
      -----------------------------------------------------------------------------
      Returns:
      An error code about the execution of the function.
      -----------------------------------------------------------------------------
      Description:
      The function performs a VME block transfer write cycle.
    */
CAENVME_API CAENVME_BLTWriteCycle(int32_t Handle, uint32_t Address, void *Buffer,
                          int size, CVAddressModifier AM, CVDataWidth DW, int *count)
{
	*count = 11;
	CAENVME_API res = cvSuccess;
	return res;
}

CAENVME_API CAENVME_FIFOBLTWriteCycle(int32_t Handle, uint32_t Address, void *Buffer,
                              int size, CVAddressModifier AM, CVDataWidth DW, int *count)
{
	*count = 11;
	CAENVME_API res = cvSuccess;
	return res;
}

CAENVME_API CAENVME_MBLTWriteCycle(int32_t Handle, uint32_t Address, void *Buffer,
                           int size, CVAddressModifier AM, int *count)
{
	*count = 11;
	CAENVME_API res = cvSuccess;
	return res;
}

CAENVME_API CAENVME_FIFOMBLTWriteCycle(int32_t Handle, uint32_t Address, void *Buffer,
                               int size, CVAddressModifier AM, int *count)
{
	*count = 11;
	CAENVME_API res = cvSuccess;
	return res;
}

CAENVME_API CAENVME_ADOCycle(int32_t Handle, uint32_t Address, CVAddressModifier AM)
{
	// TODO: what is it for exactly?
	CAENVME_API res = cvSuccess;
	return res;
}

CAENVME_API CAENVME_ADOHCycle(int32_t Handle, uint32_t Address, CVAddressModifier AM)
{
	// TODO: what is it for exactly? And how handshake works?
	CAENVME_API res = cvSuccess;
	return res;
}

