#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include <string.h>

using namespace std;


namespace Text_to_CAENVME_Calls {

	int32_t *bridge_handler;

	struct CAENlib_VME_Call
	{
		//CAENVME_API (* call)(long Handle, unsigned long Address, void * Data, CVAddressModifier AM, CVDataWidth DW);
		CAENVME_API (* parse_and_call)( char* arguments );
		//CAENVME_API ((CAENVME_plain_text_control::) parse_and_call)(char* arguments);
		string helpstr;
	};

	typedef map<string, CAENlib_VME_Call> TYPE_text_to_CAENlib_map;




	void print_vme_text_protocol_help( TYPE_text_to_CAENlib_map m ){
		printf("HELP_LINES\n");
		//printf("Device bridge handle ID:%d\n\n", *bridge_handler);
		for (std::map<string, CAENlib_VME_Call>::iterator iter=m.begin(); iter!=m.end(); iter++ ) {
	    	cout << iter->first << ": " << iter->second.helpstr << endl;
		}
	}


/*
	CAENVME_API process_text_command(char* input) {
		char * pch; // pure C comming in!
		pch = strtok(input, " "); // blank space is the only delimeter in out case
		// pch now points to the first token of the call,
		// it has to be a call name
		if ( text_to_CAENlib_map.find(pch) == text_to_CAENlib_map.end() ) {
			// not found
			printf("The call is not known.\n");
			return 1;
		} else {
			// found
			return text_to_CAENlib_map[pch].parse_and_call( strtok(NULL, "") );
		}
	}
*/

	CAENVME_API parse_and_call_CAENVME_ReadCycle( char* arguments ){
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		uint32_t address;
		uint16_t value;
		printf("Got arguments:\n%s\n", arguments);
		sscanf (arguments, "%x", &address);
		printf("Got address:\n%x\n", address);
		caen_api_return_value = CAENVME_ReadCycle( *bridge_handler, address, &value, cvA32_U_DATA, cvD16 );
		printf("Read value:\n%x\n", value);
		return caen_api_return_value;
	}


	CAENVME_API parse_and_call_CAENVME_BoardFWRelease( char* arguments ){
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		char FWRel[64];
		printf("Reading firmware release from device:\n(handle ID) %d\n", *bridge_handler);
		caen_api_return_value = CAENVME_BoardFWRelease(*bridge_handler, FWRel);
		printf("Read value:\n%s\n", FWRel);
		return caen_api_return_value;
	}

	map<string, CAENlib_VME_Call>  create_text_to_CAENlib_map( void ) {
		map<string, CAENlib_VME_Call> m;
		m["read_cycle"] = (CAENlib_VME_Call) {parse_and_call_CAENVME_ReadCycle,
			"Performs a single VME read cycle.\nTakes VME bus address. Returns the content.\n"};
		m["read_bridge_fw"] = (CAENlib_VME_Call) {parse_and_call_CAENVME_BoardFWRelease,
			"Permits to read the firmware release loaded into the device.\nTakes no arguments. Returns FW release.\n"};
	return m;
	}

	//text_to_CAENlib_map = create_text_to_CAENlib_map();

}

