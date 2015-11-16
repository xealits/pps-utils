'''
Just structs/enums and other definitions.
'''
from ctypes import c_int

# TODO: one should parse it from the actual header
# TODO: maybe it's better to keep them in some special type?

# CVBoardTypes
CVBoardTypes_t = c_int
cvV1718 = c_int(0)
cvV2718 = c_int(1)
cvA2818 = c_int(2)
cvA2719 = c_int(3)
cvA3818 = c_int(4)

# CVDataWidth
CVDataWidth_t = c_int
cvD8 = c_int(0x01)
cvD16 = c_int(0x02)
cvD32 = c_int(0x04)
cvD64 = c_int(0x08)
cvD16_swapped = c_int(0x12)
cvD32_swapped = c_int(0x14)
cvD64_swapped = c_int(0x18)

# CVAddressModifier
CVAddressModifier_t = c_int
cvA16_S = c_int(0x2D)
cvA16_U = c_int(0x29)
cvA16_LCK = c_int(0x2C)
cvA24_S_BLT = c_int(0x3F)
cvA24_S_PGM = c_int(0x3E)
cvA24_S_DATA = c_int(0x3D)
cvA24_S_MBLT = c_int(0x3C)
cvA24_U_BLT = c_int(0x3B)
cvA24_U_PGM = c_int(0x3A)
cvA24_U_DATA = c_int(0x39)
cvA24_U_MBLT = c_int(0x38)
cvA24_LCK = c_int(0x32)
cvA32_S_BLT = c_int(0x0F)
cvA32_S_PGM = c_int(0x0E)
cvA32_S_DATA = c_int(0x0D)
cvA32_S_MBLT = c_int(0x0C)
cvA32_U_BLT = c_int(0x0B)
cvA32_U_PGM = c_int(0x0A)
cvA32_U_DATA = c_int(0x09)
cvA32_U_MBLT = c_int(0x08)
cvA32_LCK = c_int(0x05)
cvCR_CSR = c_int(0x2F)
cvA40_BLT = c_int(0x37)
cvA40_LCK = c_int(0x35)
cvA40 = c_int(0x34)
cvA64 = c_int(0x01)
cvA64_BLT = c_int(0x03)
cvA64_MBLT = c_int(0x00)
cvA64_LCK = c_int(0x04)
cvA3U_2eVME = c_int(0x21)
cvA6U_2eVME = c_int(0x20)

# CVErrorCodes
CVErrorCodes_t = c_int
cvSuccess = c_int(0)
cvBusError =  c_int(-1)
cvCommError =  c_int(-2)
cvGenericError =  c_int(-3)
cvInvalidParam =  c_int(-4)
cvTimeoutError =  c_int(-5)



