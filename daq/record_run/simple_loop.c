#include <stdio.h>
#include <stdint.h>

#include "CAENVMElib.h"
#include "CAENVMEtypes.h"



int record(int32_t dev_handle, unsigned int n_tdcs, uint32_t* tdc_addresses)
{
/*
 * Input parameters:
 *     addresses of the boards to read from
 *     types of the boards? (when different types are supported)
 *        then question: how to start a process with a struct or vector on input? or all input is text and I have to parse?
 *                       if parsing is needed, maybe I should make a .so wirh run_record funcs and call them from python?
 *     frequency of output write-out
 *     output file/directory (it should be a directory, files are writen with time stamps)
 *     log destination (stderr for now? and then syslog for levels? journalctl for multiline log messages, like reports?)
 *
 * Report given parameters in the log.
 * For now don't do any checks of board configs -- that is done before record.
 * But later add such option with all necessary functions -- to have initialization of connection to CAEN VME bridge and config check in 1 processs.
 * Then just run in loop, reading boards and storing chunks of data with time-stamps on files.
 * Emit messages on your message queue according to the progress. (DQM etc IPC.)
 * (TODO: after all I need to find a look-up functionality for message queues, so that an admin could monitor the message queue without emptying it.
 *        maybe just read each message and write it back again to the queue?
 *        or maybe make that "hub" process for all messaging and manipulate that thing.)
 * Also assign an exit function for some ^C signal.
 */

// loop fetching their HW version or something else
//CAENVME_API CAENVME_ReadCycle(int32_t Handle, uint32_t Address, void *Data,
//                      CVAddressModifier AM, CVDataWidth DW);
CAENVME_API call_return;
char call_output_buffer[1024]; // 1KB
CVAddressModifier AM = 0; // TODO: these are per board, if I'm correct?
CVDataWidth DW = 0;
for (int i=0; i<n_tdcs; i++)
	{
	uint32_t tdc_addr = tdc_addresses[i];
	call_return = CAENVME_ReadCycle(dev_handle, tdc_addr, call_output_buffer, AM, DW);
	printf("%5d %2d %x\n", i, call_return, call_output_buffer);
	}

printf("run is finished, exiting\n");
return 0;
}

