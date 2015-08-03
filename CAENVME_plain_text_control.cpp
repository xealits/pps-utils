#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include <string.h>

using namespace std;


struct CAENlib_VME_Call // True only for some calls, For ReadCycle and WriteCycle for instance
{
	//CAENVME_API (* call)(long Handle, unsigned long Address, void * Data, CVAddressModifier AM, CVDataWidth DW);
	CAENVME_API (* parse_and_call)( int32_t bridge_handle, char* arguments);
	//CAENVME_API ((CAENVME_plain_text_control::) parse_and_call)(char* arguments);
	string helpstr;
};

struct help_record
{
	char command_name[32];
	char arguments_names[128];
	char description[128];
};




class CAENVME_plain_text_control
	{
	public:
		CAENVME_plain_text_control(int32_t);
		~CAENVME_plain_text_control();

		CAENVME_API parse_and_call(char* commandname, char* arguments);

		void print_vme_text_protocol_help(){
			printf("HELP_LINES\n");
			//printf("Device bridge handle ID:%d\n\n", bridge_handle);
			for (std::map<string, help_record>::iterator iter=help_page.begin(); iter!=help_page.end(); iter++ ) {
				cout << iter->second.command_name << " " << iter->second.arguments_names << ":\n\t" << iter->second.description << endl;
			}
		};

	private:
		int32_t bridge_handler;
		map<string, help_record> help_page;
		CAENVME_API read_cycle(char* arguments);
		CAENVME_API read_bridge_fw(char* arguments);
	};


CAENVME_plain_text_control::CAENVME_plain_text_control(int32_t handler)
	{
		bridge_handler = handler;

		help_page["read_cycle"] = (help_record) {"read_cycle", "<VME address>",
		 "Performs a single VME read cycle.\nTakes VME bus address. Returns the content.\n"};
		help_page["read_bridge_fw"] = (help_record) {"read_bridge_fw", "",
		 "Permits to read the firmware release loaded into the device.\nTakes no arguments. Returns FW release.\n"};
	}


CAENVME_API CAENVME_plain_text_control::parse_and_call(char* commandname, char* arguments)
	{
		if ( strcmp(commandname, "read_cycle") == 0) { read_cycle(arguments); }
		else if ( strcmp(commandname, "read_bridge_fw") == 0 ) { read_bridge_fw(arguments); }
		else if ( strcmp(commandname, "read_bridge_fw") == 0 ) { read_bridge_fw(arguments); }
		else printf("The call is not known.\n");
	}



CAENVME_API CAENVME_plain_text_control::read_cycle( char* arguments )
	{
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		uint32_t address;
		uint16_t value;
		printf("Got arguments:\n%s\n", arguments);
		sscanf (arguments, "%x", &address);
		printf("Got address:\n%x\n", address);
		caen_api_return_value = CAENVME_ReadCycle( bridge_handler, address, &value, cvA32_U_DATA, cvD16 );
		printf("Read value:\n%x\n", value);
		return caen_api_return_value;
	}


CAENVME_API CAENVME_plain_text_control::read_bridge_fw( char* arguments ){
	// parse string, call CAENVMElib function
	CAENVME_API caen_api_return_value;
	char FWRel[64];
	printf("Reading firmware release from device:\n(handle ID) %d\n", bridge_handler);
	caen_api_return_value = CAENVME_BoardFWRelease(bridge_handler, FWRel);
	printf("Read value:\n%s\n", FWRel);
	return caen_api_return_value;
}




// namespace Text_to_CAENVME_Calls {

// 	//int32_t bridge_handle = 55;

// 	struct CAENlib_VME_Call // True only for some calls, For ReadCycle and WriteCycle for instance
// 	{
// 		//CAENVME_API (* call)(long Handle, unsigned long Address, void * Data, CVAddressModifier AM, CVDataWidth DW);
// 		CAENVME_API (* parse_and_call)( int32_t bridge_handle, char* arguments);
// 		//CAENVME_API ((CAENVME_plain_text_control::) parse_and_call)(char* arguments);
// 		string helpstr;
// 	};

// 	typedef map<string, CAENlib_VME_Call> TYPE_text_to_CAENlib_map;




// 	void print_vme_text_protocol_help( TYPE_text_to_CAENlib_map m ){
// 		printf("HELP_LINES\n");
// 		//printf("Device bridge handle ID:%d\n\n", bridge_handle);
// 		for (std::map<string, CAENlib_VME_Call>::iterator iter=m.begin(); iter!=m.end(); iter++ ) {
// 			cout << iter->first << ": " << iter->second.helpstr << endl;
// 		}
// 	}


// /*
// 	CAENVME_API process_text_command(char* input) {
// 		char * pch; // pure C comming in!
// 		pch = strtok(input, " "); // blank space is the only delimeter in out case
// 		// pch now points to the first token of the call,
// 		// it has to be a call name
// 		if ( text_to_CAENlib_map.find(pch) == text_to_CAENlib_map.end() ) {
// 			// not found
// 			printf("The call is not known.\n");
// 			return 1;
// 		} else {
// 			// found
// 			return text_to_CAENlib_map[pch].parse_and_call( strtok(NULL, "") );
// 		}
// 	}
// */

// 	CAENVME_API parse_and_call_CAENVME_ReadCycle( int32_t bridge_handle, char* arguments){
// 		// parse string, call CAENVMElib function
// 		CAENVME_API caen_api_return_value;
// 		uint32_t address;
// 		uint16_t value;
// 		printf("Got arguments:\n%s\n", arguments);
// 		sscanf (arguments, "%x", &address);
// 		printf("Got address:\n%x\n", address);
// 		caen_api_return_value = CAENVME_ReadCycle( bridge_handle, address, &value, cvA32_U_DATA, cvD16 );
// 		printf("Read value:\n%x\n", value);
// 		return caen_api_return_value;
// 	}


// 	CAENVME_API parse_and_call_CAENVME_BoardFWRelease( int32_t bridge_handle, char* arguments){
// 		// parse string, call CAENVMElib function
// 		CAENVME_API caen_api_return_value;
// 		char FWRel[64];
// 		printf("Reading firmware release from device:\n(handle ID) %d\n", bridge_handle);
// 		caen_api_return_value = CAENVME_BoardFWRelease(bridge_handle, FWRel);
// 		printf("Read value:\n%s\n", FWRel);
// 		return caen_api_return_value;
// 	}

// 	map<string, CAENlib_VME_Call>  create_text_to_CAENlib_map( void ) {
// 		map<string, CAENlib_VME_Call> m;
// 		m["read_cycle"] = (CAENlib_VME_Call) {parse_and_call_CAENVME_ReadCycle,
// 			"Performs a single VME read cycle.\nTakes VME bus address. Returns the content.\n"};
// 		m["read_bridge_fw"] = (CAENlib_VME_Call) {parse_and_call_CAENVME_BoardFWRelease,
// 			"Permits to read the firmware release loaded into the device.\nTakes no arguments. Returns FW release.\n"};
// 	return m;
// 	}

// 	//text_to_CAENlib_map = create_text_to_CAENlib_map();

// }

