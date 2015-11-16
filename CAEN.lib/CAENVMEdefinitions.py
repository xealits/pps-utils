'''
Just structs/enums and other definitions.
'''

# TODO: one should parse it from the actual header
# TODO: maybe it's better to keep them in some special type?

# CVBoardTypes
cvV1718 = 0
cvV2718 = 1
cvA2818 = 2
cvA2719 = 3
cvA3818 = 4

# CVDataWidth
cvD8 = 0x01
cvD16 = 0x02
cvD32 = 0x04
cvD64 = 0x08
cvD16_swapped = 0x12
cvD32_swapped = 0x14
cvD64_swapped = 0x18

# CVAddressModifier
cvA16_S = 0x2D
cvA16_U = 0x29
cvA16_LCK = 0x2C
cvA24_S_BLT = 0x3F
cvA24_S_PGM = 0x3E
cvA24_S_DATA = 0x3D
cvA24_S_MBLT = 0x3C
cvA24_U_BLT = 0x3B
cvA24_U_PGM = 0x3A
cvA24_U_DATA = 0x39
cvA24_U_MBLT = 0x38
cvA24_LCK = 0x32
cvA32_S_BLT = 0x0F
cvA32_S_PGM = 0x0E
cvA32_S_DATA = 0x0D
cvA32_S_MBLT = 0x0C
cvA32_U_BLT = 0x0B
cvA32_U_PGM = 0x0A
cvA32_U_DATA = 0x09
cvA32_U_MBLT = 0x08
cvA32_LCK = 0x05
cvCR_CSR = 0x2F
cvA40_BLT = 0x37
cvA40_LCK = 0x35
cvA40 = 0x34
cvA64 = 0x01
cvA64_BLT = 0x03
cvA64_MBLT = 0x00
cvA64_LCK = 0x04
cvA3U_2eVME = 0x21
cvA6U_2eVME = 0x20

# CVErrorCodes
cvSuccess = 0
cvBusError = -1
cvCommError = -2
cvGenericError = -3
cvInvalidParam = -4
cvTimeoutError = -5



