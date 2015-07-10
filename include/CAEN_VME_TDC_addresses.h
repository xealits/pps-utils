
typedef enum {

    kOutputBuffer            = 0x0000, // D32 R
    kControl                 = 0x1000, // D16 R/W
    kStatus                  = 0x1002, // D16 R
    kInterruptLevel          = 0x100a, // D16 R/W
    kInterruptVector         = 0x100c, // D16 R/W
    kGeoAddress              = 0x100e, // D16 R/W
    kMCSTBase                = 0x1010, // D16 R/W
    kMCSTControl             = 0x1012, // D16 R/W
    kModuleReset             = 0x1014, // D16 W
    kSoftwareClear           = 0x1016, // D16 W
    kEventCounter            = 0x101c, // D32 R
    kEventStored             = 0x1020, // D16 R
    kBLTEventNumber          = 0x1024, // D16 R/W
    kFirmwareRev             = 0x1026, // D16 R
    kMicro                   = 0x102e, // D16 R/W
    kMicroHandshake          = 0x1030, // D16 R
    
    kEventFIFO               = 0x1038, // D32 R
    kEventFIFOStoredRegister = 0x103c, // D16 R
    kEventFIFOStatusRegister = 0x103e, // D16 R  
    
    kROMOui2                 = 0x4024,
    kROMOui1                 = 0x4028,
    kROMOui0                 = 0x402c,
    
    kROMBoard2               = 0x4034,
    kROMBoard1               = 0x4038,
    kROMBoard0               = 0x403c,
    kROMRevis3               = 0x4040,
    kROMRevis2               = 0x4044,
    kROMRevis1               = 0x4048,
    kROMRevis0               = 0x404c,
    kROMSerNum1              = 0x4080,
    kROMSerNum0              = 0x4084,
    
  } mod_reg;

