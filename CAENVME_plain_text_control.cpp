#include "CAENVMElib.h"
#include "CAENVMEoslib.h"
#include "CAENVMEtypes.h"

#include <string.h> // strtok,
#include <stdint.h> // standard integers: uint16_t etc

using namespace std;


namespace Text_to_CAENVME_Calls {

	int32_t *bridge_handler;

	struct VMECall_help_record
	{
		string command_name;
		string arguments;
		string description;
	};

	struct CAENlib_VME_Call
	{
		//CAENVME_API (* call)(long Handle, unsigned long Address, void * Data, CVAddressModifier AM, CVDataWidth DW);
		CAENVME_API (* parse_and_call)( char* arguments );
		//CAENVME_API ((CAENVME_plain_text_control::) parse_and_call)(char* arguments);
		VMECall_help_record help_record;
	};

	typedef map<string, CAENlib_VME_Call> TYPE_text_to_CAENlib_map;




	void print_vme_text_protocol_help( TYPE_text_to_CAENlib_map m ){
		printf("HELP_LINES\n");
		//printf("Device bridge handle ID:%d\n\n", *bridge_handler);
		for (std::map<string, CAENlib_VME_Call>::iterator iter=m.begin(); iter!=m.end(); iter++ ) {
	    	cout
	    		<< iter->second.help_record.command_name
	    		<< " "
	    		<< iter->second.help_record.arguments
	    		<< "\n\t"
	    		<< iter->second.help_record.description
	    		<< endl;
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

	CAENVME_API parse_and_call_CAENVME_BoardFWRelease( char* arguments ){
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		char FWRel[64];
		printf("Reading firmware release from device:\n(handle ID) %d\n", *bridge_handler);
		caen_api_return_value = CAENVME_BoardFWRelease(*bridge_handler, FWRel);
		printf("Read value:\n%s\n", FWRel);
		return caen_api_return_value;
	}

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



	CAENVME_API parse_and_call_CAENVME_WriteRegister( char* arguments ){
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		uint32_t address; // TODO CVRegisters !
		unsigned short value;// uint16_t value; // TODO unsigned short
		CVRegisters reg_address;

		// parse register address and input value
		char * pch;
		pch = strtok(arguments, " "); // blank space is the only delimeter in out case
		sscanf (pch, "%x", &address);
		reg_address = static_cast<CVRegisters>( address ); // uint32_t to enum
		sscanf (strtok(NULL, " "), "%x", &value);

		printf("Writing %x to register @ %x of the bridge device, handle ID = %d\n", value, address, *bridge_handler);
		caen_api_return_value = CAENVME_WriteRegister(*bridge_handler, reg_address, value);
		printf("Done\n");
		return caen_api_return_value;
	}

	CAENVME_API parse_and_call_CAENVME_WriteCycle( char* arguments ){
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		uint32_t address;
		uint16_t value;

		// parse register address and input value
		char * pch;
		pch = strtok(arguments, " "); // blank space is the only delimeter in out case
		sscanf (pch, "%x", &address);
		sscanf (strtok(NULL, " "), "%x", &value);

		printf("Writing %x to address %x on VME\n(bridge handle ID = %d)\n", value, address, *bridge_handler);
		caen_api_return_value = CAENVME_WriteCycle( *bridge_handler, address, &value, cvA32_U_DATA, cvD16);
		printf("Done\n");
		return caen_api_return_value;
	}


	CAENVME_API parse_and_call_CAENVME_BLTReadCycle( char* arguments ){
		// parse string, call CAENVMElib function
		CAENVME_API caen_api_return_value;
		uint32_t address;
		int size;
		// printf("Got arguments:\n%s\n", arguments);
		// sscanf (arguments, "%x", &address);
		// printf("Got address:\n%x\n", address);

		// parse address and the size of block
		char * pch;
		pch = strtok(arguments, " "); // blank space is the only delimeter in out case
		sscanf (pch, "%x", &address);
		sscanf (strtok(NULL, " "), "%d", &size);

		char * block_buffer;
		block_buffer = (char*)malloc(size); // size bytes in the buffer
		// memset(block_buffer, 0, sizeof(uint32_t));
		int block_size = size;
		int count = 0;

		printf("Reading block @ %x address on VME of the size %x bytes\n(bridge handle ID = %d)\n", address, size, *bridge_handler);
		caen_api_return_value = CAENVME_BLTReadCycle( *bridge_handler, address, block_buffer, size, cvA32_U_DATA, cvD32, &count );
		printf("Block read. %d bytes transfered\n", count);

		// for now, with -- cvD32 -- let's output to stdout four-byte lines
		for (int i = 0; i < count; ++i)
		{
			printf("%x%x%x%x\n", block_buffer[i++], block_buffer[i++], block_buffer[i++], block_buffer[i]);
		}

		return caen_api_return_value;
	}


	map<string, CAENlib_VME_Call>  create_text_to_CAENlib_map( void ) {
		map<string, CAENlib_VME_Call> m;

		m["read_cycle"] = (CAENlib_VME_Call) { parse_and_call_CAENVME_ReadCycle,
			(VMECall_help_record) { "read_cycle",
			                        "<VME address 0x>",
			                        "Performs a single VME read cycle.\nPrints the result.\n"}
		};

		m["read_bridge_fw"] = (CAENlib_VME_Call) { parse_and_call_CAENVME_BoardFWRelease,
			(VMECall_help_record) { "read_bridge_fw",
			                        "",
			                        "Permits to read the firmware release loaded into the device.\n"
			                        "Prints FW release.\n"}
		};

		m["write_bridge_register"] = (CAENlib_VME_Call) { parse_and_call_CAENVME_WriteRegister,
			(VMECall_help_record) { "write_bridge_register",
			                        "<Bridge Register Address 0x> <New Value 0x>",
			                        "Writes the new value to the register at the given address on the Bridge device.\n"}
		};

		m["write_cycle"] = (CAENlib_VME_Call) { parse_and_call_CAENVME_WriteCycle,
			(VMECall_help_record) { "write_cycle",
			                        "<VME Address 0x> <New Value 0x>",
			                        "Writes the new value to the register at the given address on VME.\n"}
		};

		m["read_block_cycle"] = (CAENlib_VME_Call) {parse_and_call_CAENVME_BLTReadCycle,
			(VMECall_help_record) { "read_block_cycle",
			                        "<VME Address 0x> <Number of Bytes to read 0d>",
			                        "The function performs a VME block transfer read cycle."
			                        "It can be used to perform MBLT transfers using 64 bit data width.\n"
			                        "(works only with 32 bit width buffers)\n(output goes to stdout)\n"}
		};

	return m;
	}

	//text_to_CAENlib_map = create_text_to_CAENlib_map();

}

