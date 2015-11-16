from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, c_uint32, c_int32, c_int, c_char, c_char_p
from threading import Thread, Event

c_uint32_p = POINTER(c_uint32)
c_int32_p = POINTER(c_int32)
#import Pyro4

from CAENVMEdefinitions import *


# for now the lib should be in the same directory (symlinks are welcome)
#cdll.LoadLibrary( "./libCAENVME.so" )
#lib = CDLL( "./libCAENVME.so" )


class PreVMEOperator(CDLL):
    """docstring for PreVMEOperator"""

    def __init__(self, libpath):
        '''PreVMEOperator(self, libpath)
        '''
        # load the lib
        cdll.LoadLibrary( libpath ) # TODO: if error -- break
        # initialize the CDLL object
        super(PreVMEOperator, self).__init__(libpath)
        # TODO: move the lib initialization further to init?
        #       to make library calls unavailable here?
        set_ctype_restrictions(super(PreVMEOperator, self)) # set input restrictions for CAEN calls?
        # store the path
        self.libpath = libpath
        self.device_handler = None # ctypes long
        self.buffers =  None # ctypes string buffer for reading VME output and the io pipes
        # at the end we have: the lib-connection is ready,
        # the operations are not initialized yet
        
    def init(self, board_type=cvV2718, link=0, bdnum=0):
        '''init(self, board_type=cvV2718, link=0, bdnum=0)

        init operation parameters and CAENVMElib
        '''

        if self.device_handler:
            print("device_handler is already set -- something is terribly wrong")
            return None

        #dev = c_long() # In Reference it is long, but in headers it's int32_t
        dev = c_int32()
        err = self.CAENVME_Init(board_type, link, bdnum, byref(dev))

        if err != cvSuccess:
            print("CAENVME_Init error %s" % err)
            return err

        self.device_handler = dev
        # TODO: how to shove the devhandler into the CAENVME calls automaticaly?

        # TODO: initialize IO buffers self.buffers

        # when everything is ready switch the state to the initialized operator
        self.__class__ = VMEOperator
        # TODO: maybe one can redefine the methods for VME-bus calls to have device_handler in default?


    # TODO: how to pack all this identical calls into one loop?
    # TODO: and how to add the ctypes input type restrictions?
    #       the ctypes restrictions should be done before -- directly on the CDLL methods
    #       these are regular Python methods
    def CAENVME_BoardFWRelease(self, *args):
        return super(VMEOperator, self).CAENVME_BoardFWRelease(self.device_handler, *args)

    def CAENVME_DriverRelease(self, *args):
        return super(VMEOperator, self).CAENVME_DriverRelease(self.device_handler, *args)

    def CAENVME_DeviceReset(self, *args):
        return super(VMEOperator, self).CAENVME_DeviceReset(self.device_handler, *args)

    def CAENVME_End(self, *args):
        return super(VMEOperator, self).CAENVME_End(self.device_handler, *args)

    def CAENVME_ReadCycle(self, *args):
        return super(VMEOperator, self).CAENVME_ReadCycle(self.device_handler, *args)

    def CAENVME_RMWCycle(self, *args):
        return super(VMEOperator, self).CAENVME_RMWCycle(self.device_handler, *args)

    def CAENVME_WriteCycle(self, *args):
        return super(VMEOperator, self).CAENVME_WriteCycle(self.device_handler, *args)

 
    def CAENVME_MultiRead(self, *args):
        return super(VMEOperator, self).CAENVME_MultiRead(self.device_handler, *args)

    def CAENVME_MultiWrite(self, *args):
        return super(VMEOperator, self).CAENVME_MultiWrite(self.device_handler, *args)

    def CAENVME_BLTReadCycle(self, *args):
        return super(VMEOperator, self).CAENVME_BLTReadCycle(self.device_handler, *args)

    def CAENVME_FIFOBLTReadCycle(self, *args):
        return super(VMEOperator, self).CAENVME_FIFOBLTReadCycle(self.device_handler, *args)

    def CAENVME_MBLTReadCycle(self, *args):
        return super(VMEOperator, self).CAENVME_MBLTReadCycle(self.device_handler, *args)

    def CAENVME_FIFOMBLTReadCycle(self, *args):
        return super(VMEOperator, self).CAENVME_FIFOMBLTReadCycle(self.device_handler, *args)

    def CAENVME_BLTWriteCycle(self, *args):
        return super(VMEOperator, self).CAENVME_BLTWriteCycle(self.device_handler, *args)

    def CAENVME_FIFOBLTWriteCycle(self, *args):
        return super(VMEOperator, self).CAENVME_FIFOBLTWriteCycle(self.device_handler, *args)

    def CAENVME_MBLTWriteCycle(self, *args):
        return super(VMEOperator, self).CAENVME_MBLTWriteCycle(self.device_handler, *args)

    def CAENVME_FIFOMBLTWriteCycle(self, *args):
        return super(VMEOperator, self).CAENVME_FIFOMBLTWriteCycle(self.device_handler, *args)

    def CAENVME_ADOCycle(self, *args):
        return super(VMEOperator, self).CAENVME_ADOCycle(self.device_handler, *args)

    def CAENVME_ADOHCycle(self, *args):
        return super(VMEOperator, self).CAENVME_ADOHCycle(self.device_handler, *args)

    def CAENVME_IACKCycle(self, *args):
        return super(VMEOperator, self).CAENVME_IACKCycle(self.device_handler, *args)

    def CAENVME_IRQCheck(self, *args):
        return super(VMEOperator, self).CAENVME_IRQCheck(self.device_handler, *args)

    def CAENVME_IRQEnable(self, *args):
        return super(VMEOperator, self).CAENVME_IRQEnable(self.device_handler, *args)

    def CAENVME_IRQDisable(self, *args):
        return super(VMEOperator, self).CAENVME_IRQDisable(self.device_handler, *args)

    def CAENVME_IRQWait(self, *args):
        return super(VMEOperator, self).CAENVME_IRQWait(self.device_handler, *args)

    def CAENVME_SetPulserConf(self, *args):
        return super(VMEOperator, self).CAENVME_SetPulserConf(self.device_handler, *args)

    def CAENVME_SetScalerConf(self, *args):
        return super(VMEOperator, self).CAENVME_SetScalerConf(self.device_handler, *args)

    def CAENVME_SetOutputConf(self, *args):
        return super(VMEOperator, self).CAENVME_SetOutputConf(self.device_handler, *args)

    def CAENVME_SetInputConf(self, *args):
        return super(VMEOperator, self).CAENVME_SetInputConf(self.device_handler, *args)

    def CAENVME_GetPulserConf(self, *args):
        return super(VMEOperator, self).CAENVME_GetPulserConf(self.device_handler, *args)

    def CAENVME_GetScalerConf(self, *args):
        return super(VMEOperator, self).CAENVME_GetScalerConf(self.device_handler, *args)

    def CAENVME_GetOutputConf(self, *args):
        return super(VMEOperator, self).CAENVME_GetOutputConf(self.device_handler, *args)

    def CAENVME_GetInputConf(self, *args):
        return super(VMEOperator, self).CAENVME_GetInputConf(self.device_handler, *args)

    def CAENVME_ReadRegister(self, *args):
        return super(VMEOperator, self).CAENVME_ReadRegister(self.device_handler, *args)

    def CAENVME_WriteRegister(self, *args):
        return super(VMEOperator, self).CAENVME_WriteRegister(self.device_handler, *args)

    def CAENVME_SetOutputRegister(self, *args):
        return super(VMEOperator, self).CAENVME_SetOutputRegister(self.device_handler, *args)

    def CAENVME_ClearOutputRegister(self, *args):
        return super(VMEOperator, self).CAENVME_ClearOutputRegister(self.device_handler, *args)

    def CAENVME_PulseOutputRegister(self, *args):
        return super(VMEOperator, self).CAENVME_PulseOutputRegister(self.device_handler, *args)

    def CAENVME_ReadDisplay(self, *args):
        return super(VMEOperator, self).CAENVME_ReadDisplay(self.device_handler, *args)

    def CAENVME_SetArbiterType(self, *args):
        return super(VMEOperator, self).CAENVME_SetArbiterType(self.device_handler, *args)

    def CAENVME_SetRequesterType(self, *args):
        return super(VMEOperator, self).CAENVME_SetRequesterType(self.device_handler, *args)

    def CAENVME_SetReleaseType(self, *args):
        return super(VMEOperator, self).CAENVME_SetReleaseType(self.device_handler, *args)

    def CAENVME_SetBusReqLevel(self, *args):
        return super(VMEOperator, self).CAENVME_SetBusReqLevel(self.device_handler, *args)

    def CAENVME_SetTimeout(self, *args):
        return super(VMEOperator, self).CAENVME_SetTimeout(self.device_handler, *args)

    def CAENVME_SetLocationMonitor(self, *args):
        return super(VMEOperator, self).CAENVME_SetLocationMonitor(self.device_handler, *args)

    def CAENVME_SetFIFOMode(self, *args):
        return super(VMEOperator, self).CAENVME_SetFIFOMode(self.device_handler, *args)

    def CAENVME_GetArbiterType(self, *args):
        return super(VMEOperator, self).CAENVME_GetArbiterType(self.device_handler, *args)

    def CAENVME_GetRequesterType(self, *args):
        return super(VMEOperator, self).CAENVME_GetRequesterType(self.device_handler, *args)

    def CAENVME_GetReleaseType(self, *args):
        return super(VMEOperator, self).CAENVME_GetReleaseType(self.device_handler, *args)

    def CAENVME_GetBusReqLevel(self, *args):
        return super(VMEOperator, self).CAENVME_GetBusReqLevel(self.device_handler, *args)

    def CAENVME_GetTimeout(self, *args):
        return super(VMEOperator, self).CAENVME_GetTimeout(self.device_handler, *args)

    def CAENVME_GetFIFOMode(self, *args):
        return super(VMEOperator, self).CAENVME_GetFIFOMode(self.device_handler, *args)

    def CAENVME_SystemReset(self, *args):
        return super(VMEOperator, self).CAENVME_SystemReset(self.device_handler, *args)

    def CAENVME_ResetScalerCount(self, *args):
        return super(VMEOperator, self).CAENVME_ResetScalerCount(self.device_handler, *args)

    def CAENVME_EnableScalerGate(self, *args):
        return super(VMEOperator, self).CAENVME_EnableScalerGate(self.device_handler, *args)

    def CAENVME_DisableScalerGate(self, *args):
        return super(VMEOperator, self).CAENVME_DisableScalerGate(self.device_handler, *args)

    def CAENVME_StartPulser(self, *args):
        return super(VMEOperator, self).CAENVME_StartPulser(self.device_handler, *args)

    def CAENVME_StopPulser(self, *args):
        return super(VMEOperator, self).CAENVME_StopPulser(self.device_handler, *args)

    def CAENVME_WriteFlashPage(self, *args):
        return super(VMEOperator, self).CAENVME_WriteFlashPage(self.device_handler, *args)

    def CAENVME_ReadFlashPage(self, *args):
        return super(VMEOperator, self).CAENVME_ReadFlashPage(self.device_handler, *args)

    def CAENVME_EraseFlashPage(self, *args):
        return super(VMEOperator, self).CAENVME_EraseFlashPage(self.device_handler, *args)

    def CAENVME_BLTReadAsync(self, *args):
        return super(VMEOperator, self).CAENVME_BLTReadAsync(self.device_handler, *args)

    def CAENVME_BLTReadWait(self, *args):
        return super(VMEOperator, self).CAENVME_BLTReadWait(self.device_handler, *args)

    def set_ctype_restrictions(self, lo):
        # TODO: lo should be the initialized object/class
        #       with the ctype representation of the lib calls
        #       and setting the argument check now should fix it for VMEOperator as well
        # first argument is the device handler everywhere
        lo.CAENVME_BoardFWRelease.argtypes = [c_int32, c_char_p]
        # common pattern: the second argument is the address
        #                 the third -- data to be passed
        #                 then address modifier and datawidth
        lo.CAENVME_DriverRelease.argtypes = [c_int32, c_uint32]
        lo.CAENVME_DeviceReset.argtypes = [c_int32]
        lo.CAENVME_End.argtypes = [c_int32]
        lo.CAENVME_ReadCycle.argtypes = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_RMWCycle.argtypes = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_WriteCycle.argtypes = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]

        lo.CAENVME_MultiRead.argtypes = [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)]
        lo.CAENVME_MultiWrite.argtypes = [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)]

        lo.CAENVME_BLTReadCycle.argtypes =      [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
        lo.CAENVME_FIFOBLTReadCycle.argtypes =  [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]

        lo.CAENVME_MBLTReadCycle.argtypes =     [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
        lo.CAENVME_FIFOMBLTReadCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]

        lo.CAENVME_BLTWriteCycle.argtypes =      [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
        lo.CAENVME_FIFOBLTWriteCycle.argtypes =  [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]

        lo.CAENVME_MBLTWriteCycle.argtypes =     [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
        lo.CAENVME_FIFOMBLTWriteCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]

        lo.CAENVME_ADOCycle.argtypes =  [c_int32, c_uint32, CVAddressModifier_t]
        lo.CAENVME_ADOHCycle.argtypes = [c_int32, c_uint32, CVAddressModifier_t]

        '''
        lo.CAENVME_IACKCycle.argtypes = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_IRQCheck.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_IRQEnable.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_IRQDisable.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_IRQWait.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetPulserConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetScalerConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetOutputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetInputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetPulserConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetScalerConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetOutputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetInputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_ReadRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_WriteRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetOutputRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_ClearOutputRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_PulseOutputRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_ReadDisplay.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetArbiterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetRequesterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetReleaseType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetBusReqLevel.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetTimeout.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetLocationMonitor.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SetFIFOMode.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetArbiterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetRequesterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetReleaseType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetBusReqLevel.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetTimeout.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_GetFIFOMode.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_SystemReset.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_ResetScalerCount.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_EnableScalerGate.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_DisableScalerGate.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_StartPulser.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_StopPulser.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_WriteFlashPage.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_ReadFlashPage.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_EraseFlashPage.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_BLTReadAsync.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        lo.CAENVME_BLTReadWait.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        '''

 

class VMEOperator(CDLL):
    """docstring for VMEOperator"""

    def __init__(self, device_handler, buffers):
        '''(self, device_handler, buffers)

        if creating the VMEOperator directly,
        the lib should be initialized and ready,
        device_handler and the buffers required.
        '''
        # the library should be already loaded
        # and CDLL initialized,
        # only couple of methods are missing
        #super(VMEOperator, self).__init__(libpath)
        self.device_handler = device_handler # ctypes long/int32?
        self.buffers = buffers # ctypes string buffer for reading VME output and the io pipes


    def end(self):
        '''end(self)

        end CAENVMElib operation -- call CAENVME_End(self.device_handler)
        '''

        err = self.CAENVME_End()
        if err != cvSuccess:
            print("CAENVME_Init error %s" % err)
            return err

        self.buffers = None

        # when everything is closed -- go back to not-init state
        self.__class__ = PreVMEOperator

    '''
    # TODO: default for device_handler in the initialized VMEOperator?
    def CAENVME_BoardFWRelease(self, *args):
        return super(VMEOperator, self).CAENVME_BoardFWRelease(self.device_handler, *args)
    # the same for all VME-bus calls
    '''
