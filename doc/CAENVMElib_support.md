
# CAEN's VME lib

## Headers

    #include "CAENVMElib.h"
    #include "CAENVMEoslib.h"
    #include "CAENVMEtypes.h"



## Bridge handler type

    int32_t bridge_handler;



## Lib calls scheme

    char FWRel[64];
    // bridge_handler is int32_t ID of the device
    (CAENVME_API) CAENVME_BoardFWRelease(bridge_handler, FWRel);
    //
    uint32_t address;
    char bytes_to_read[2]; // 16 bits
    (CAENVME_API) CAENVME_ReadCycle( bridge_handler, address, bytes_to_read, cvA32_U_DATA, cvD16 );



## Address modifiers, like `cvA32_U_DATA`?

    ...


## Data transfer modifiers, like `cvD16`?

    ...


## Call result, `CAENVME_API`?

...


## More questions

### CVBoardTypes
### CVErrorCodes





# Laurent's bridge class

## header:

    #include "VME_BridgeVx718.h"


## object:

    VME::BridgeVx718 * bridge;
    bridge = new VME::BridgeVx718(bridge_device_filename, VME::CAEN_V2718);



## object initialization:

     BridgeVx718::BridgeVx718(const char *device, BridgeType type)
       {
         int dev = atoi(device);
         CVBoardTypes tp;
         CVErrorCodes ret;
         std::ostringstream o;
     
         char rel[20];
         CAENVME_SWRelease(rel);
         o.str("");
         o << "Initializing the VME bridge\n\t"
           << "CAEN library release: " << rel;
         PrintInfo(o.str());
     
         switch (type) {
           case CAEN_V1718: tp = cvV1718; break;
           case CAEN_V2718: tp = cvV2718; break;
           default:
             o.str("");
             o << "Invalid VME bridge type: " << type;
             throw Exception(__PRETTY_FUNCTION__, o.str(), Fatal);
         }
     
         ret = CAENVME_Init(tp, 0x0, dev, &fHandle);
         if (ret!=cvSuccess) {
           o.str("");
           o << "Error opening the VME bridge!\n\t"
             << "CAEN error: " << CAENVME_DecodeError(ret);
           throw Exception(__PRETTY_FUNCTION__, o.str(), Fatal);
         }
     
         ret = CAENVME_BoardFWRelease(fHandle, rel);
         if (ret!=cvSuccess) {
           o.str("");
           o << "Failed to retrieve the board FW release!\n\t"
             << "CAEN error: " << CAENVME_DecodeError(ret);
           throw Exception(__PRETTY_FUNCTION__, o.str(), Fatal);
         }
         o.str("");
         o << "Bridge firmware version: " << rel;
         PrintInfo(o.str());
     
         //Map output lines [0,4] to corresponding register.
         fPortMapping[cvOutput0] = cvOut0Bit;
         fPortMapping[cvOutput1] = cvOut1Bit;
         fPortMapping[cvOutput2] = cvOut2Bit;
         fPortMapping[cvOutput3] = cvOut3Bit;
         fPortMapping[cvOutput4] = cvOut4Bit;
     
         CheckConfiguration();
       }


where:

    std::map<CVOutputSelect,CVOutputRegisterBits> fPortMapping;

and both `CVOutputSelect`, `CVOutputRegisterBits` are


## another initialization procedure:

    BridgeVx718::BridgeVx718(const char* device, BridgeType type) :
        GenericBoard<CVRegisters,cvA32_U_DATA>(0, 0x0)
    {
        int dev = atoi(device);
        CVBoardTypes tp;
        CVErrorCodes ret; 
        std::ostringstream o;
     
        /*char rel[20];
        CAENVME_SWRelease(rel);
        o.str("");
        o << "Initializing the VME bridge\n\t"
          << "CAEN library release: " << rel;
        PrintInfo(o.str());*/
    
        switch (type) {
          case CAEN_V1718: tp = cvV1718; break;
          case CAEN_V2718:
            tp = cvV2718;
            try { CheckPCIInterface(device); } catch (Exception& e) {
              e.Dump();
              throw Exception(__PRETTY_FUNCTION__, "Failed to initialize the PCI/VME interface card!", Fatal);
            }
            break;
          default:
            o.str("");
            o << "Invalid VME bridge type: " << type;
            throw Exception(__PRETTY_FUNCTION__, o.str(), Fatal);
        }
    
        ret = CAENVME_Init(tp, 0x0, dev, &fHandle);
        if (ret!=cvSuccess) {
          o.str("");
          o << "Error opening the VME bridge!\n\t"
            << "CAEN error: " << CAENVME_DecodeError(ret);
          throw Exception(__PRETTY_FUNCTION__, o.str(), Fatal, CAEN_ERROR(ret));
        }
    
        char board_rel[100];
        ret = CAENVME_BoardFWRelease(fHandle, board_rel);
        if (ret!=cvSuccess) {
          o.str("");
          o << "Failed to retrieve the board FW release!\n\t"
            << "CAEN error: " << CAENVME_DecodeError(ret);
          throw Exception(__PRETTY_FUNCTION__, o.str(), Fatal, CAEN_ERROR(ret));
        }
        o.str("");
        o << "Bridge firmware version: " << board_rel;
        PrintInfo(o.str());
        CheckConfiguration();
    
        //SetIRQ(IRQ1|IRQ2|IRQ3|IRQ4|IRQ5|IRQ6|IRQ7, false);
    }

with:

    void BridgeVx718::CheckConfiguration() const
      {
        CVErrorCodes ret;
        CVDisplay config;
        std::ostringstream o;
        ret = CAENVME_ReadDisplay(fHandle, &config);
        if (ret!=cvSuccess) {
          std::ostringstream os;
          os << "Failed to retrieve configuration displayed on\n\t"
             << "module's front panel\n\t"
             << "CAEN error: " << CAENVME_DecodeError(ret);
          throw Exception(__PRETTY_FUNCTION__, os.str(), Fatal, CAEN_ERROR(ret));
        }
      }

and `CVRegisters` are not used anywhere else





### the library init call:


    int dev = atoi(device);
    CVBoardTypes tp;
    CVErrorCodes ret;
    char rel[20];
         CAENVME_SWRelease(rel);
    //...
    ret = CAENVME_Init(tp, 0x0, dev, &fHandle);



And then one can call to the bridge board:

    ret = CAENVME_BoardFWRelease(fHandle, rel);

