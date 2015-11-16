from ctypes import CDLL, cdll, byref, c_int32, c_char, create_string_buffer
from threading import Thread, Event
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

        err = self.CAENVME_End( )
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
