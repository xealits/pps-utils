from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
import Pyro4
import sys
# from threading import Thread, Event

# TODO: how to serialize ctypes objects?
# Pyro4.config.SERIALIZER = 'pickle'

c_uint32_p = POINTER(c_uint32)
c_int32_p = POINTER(c_int32)
#import Pyro4

from CAENVMEdefinitions import *


# for now the lib should be in the same directory (symlinks are welcome)
#cdll.LoadLibrary( "./libCAENVME.so" )
#lib = CDLL( "./libCAENVME.so" )

class Broadcaster(object):
    """docstring for Broadcaster"""
    def __init__(self, listeners_uris=None):
        self.listeners = list(Pyro4.Proxy(uri) for uri in listeners_uris) if listeners_uris else []

    def add_listener(self, uri):
        self.listeners.append(Pyro4.Proxy(uri))

    def pyro_connection_echo(self, *args):
        print(args)
        print(type(args))
        return args


class PreVMEOperator(Broadcaster):
    """docstring for PreVMEOperator"""

    def __init__(self, libpath):
        '''PreVMEOperator(self, libpath)
        '''
        Broadcaster.__init__(self)
        # load the lib
        cdll.LoadLibrary( libpath ) # TODO: if error -- break
        # initialize the CDLL object
        self.lib = CDLL( libpath )
        # super(PreVMEOperator, self).__init__(libpath)
        # TODO: move the lib initialization further to init?
        #       to make library calls unavailable here?
        # TODO: the .so has no names -- the functions are not seen before a call to them
        self.set_ctype_restrictions() # set input restrictions for CAEN calls?
        # store the path
        self.libpath = libpath
        self.device_handler = None # ctypes long
        self.buffers =  None # ctypes string buffer for reading VME output and the io pipes
        # at the end we have: the lib-connection is ready,
        # the operations are not initialized yet

    # TODO: check link and bdnum -- where is the definition, what's the type, what are the values?
    def init(self, board_type=cvV2718.value, link=0, bdnum=0):
        '''init(self, board_type=cvV2718.value, link=0, bdnum=0)

        init operation parameters and CAENVMElib
        the parameters are native Python data
        -- serializable and sendable over Pyro
        '''

        if self.device_handler:
            print("device_handler is already set -- something is terribly wrong")
            return None

        #dev = c_long() # In Reference it is long, but in headers it's int32_t
        dev = c_int32()
        # TODO: for some odd reason ctypes returns Python's int
        # even when the function has restype == c_int
        # thus err is Python' int here
        # be aware!
        err = self.lib.CAENVME_Init(CVBoardTypes_t(board_type), link, bdnum, byref(dev))

        # err is Python's int, so is cvSuccess.value
        if err != cvSuccess.value:
            print("CAENVME_Init error %s" % err)
            return err

        self.device_handler = dev

        # TODO: initialize IO buffers self.buffers

        # when everything is ready switch the state to the initialized operator
        self.__class__ = VMEOperator


    # exposing the lib methods to Pyro connection
    def CAENVME_SWRelease(self, output_len):
        s = create_string_buffer(b'0'*output_len)
        # TODO: should one use bytes or strings? in Python2/3?
        err = self.lib.CAENVME_SWRelease(s)
        # TODO: err always is Python's int? Or output type can be set to ctypes?
        return (err, s.value)

    def set_ctype_restrictions(self):
        # TODO: self.lib should be the initialized object/class
        #       with the ctype representation of the lib calls
        #       and setting the argument check now should fix it for VMEOperator as well
        # first argument is the device handler everywhere

        try:
            self.lib.CAENVME_SWRelease.argtypes = [c_char_p]
            self.lib.CAENVME_End.argtypes       = [c_int32]
            self.lib.CAENVME_BoardFWRelease.argtypes = [c_int32, c_char_p]
            # common pattern: the second argument is the address
            #                 the third -- data to be passed
            #                 then address modifier and datawidth
            self.lib.CAENVME_DriverRelease.argtypes = [c_int32, c_char_p]
            self.lib.CAENVME_DeviceReset.argtypes   = [c_int32]
            self.lib.CAENVME_ReadCycle.argtypes  = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
            self.lib.CAENVME_RMWCycle.argtypes   = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
            self.lib.CAENVME_WriteCycle.argtypes = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]

            self.lib.CAENVME_MultiRead.argtypes  = [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)]
            self.lib.CAENVME_MultiWrite.argtypes = [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)]

            self.lib.CAENVME_BLTReadCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
            self.lib.CAENVME_FIFOBLTReadCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]

            self.lib.CAENVME_MBLTReadCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
            self.lib.CAENVME_FIFOMBLTReadCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]

            self.lib.CAENVME_BLTWriteCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
            self.lib.CAENVME_FIFOBLTWriteCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]

            self.lib.CAENVME_MBLTWriteCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
            self.lib.CAENVME_FIFOMBLTWriteCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]

            self.lib.CAENVME_ADOCycle.argtypes  = [c_int32, c_uint32, CVAddressModifier_t]
            self.lib.CAENVME_ADOHCycle.argtypes = [c_int32, c_uint32, CVAddressModifier_t]

        except Exception as e:
            print( e )
        else:
            pass
        finally:
            pass

        '''
        self.lib.CAENVME_IACKCycle.argtypes = [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_IRQCheck.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_IRQEnable.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_IRQDisable.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_IRQWait.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetPulserConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetScalerConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetOutputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetInputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetPulserConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetScalerConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetOutputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetInputConf.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_ReadRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_WriteRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetOutputRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_ClearOutputRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_PulseOutputRegister.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_ReadDisplay.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetArbiterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetRequesterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetReleaseType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetBusReqLevel.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetTimeout.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetLocationMonitor.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SetFIFOMode.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetArbiterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetRequesterType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetReleaseType.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetBusReqLevel.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetTimeout.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_GetFIFOMode.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_SystemReset.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_ResetScalerCount.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_EnableScalerGate.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_DisableScalerGate.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_StartPulser.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_StopPulser.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_WriteFlashPage.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_ReadFlashPage.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_EraseFlashPage.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_BLTReadAsync.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        self.lib.CAENVME_BLTReadWait.argtypes = [ c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        '''

 

class VMEOperator(Broadcaster):
    """docstring for VMEOperator"""

    def __init__(self, device_handler, buffers, lib):
        '''(self, device_handler, buffers)

        if creating the VMEOperator directly,
        the lib should be initialized and ready,
        device_handler and the buffers required.
        '''
        # the library should be already loaded
        # CDLL initialized at self.lib
        # only couple of methods are missing
        #super(VMEOperator, self).__init__(libpath)
        self.device_handler = device_handler # ctypes long/int32?
        self.buffers = buffers # ctypes string buffer for reading VME output and the io pipes
        self.lib = lib


    def end(self):
        '''end(self)

        end CAENVMElib operation -- call CAENVME_End(self.device_handler)
        '''

        err = self.CAENVME_End()
        # err is Python's int, so is cvSuccess.value
        if err != cvSuccess.value:
            print("CAENVME_End error %s" % err)
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

    # exposing the lib methods to Pyro connection
    # SWRelease is duplicated in both classe to not create a common class (yet)
    def CAENVME_SWRelease(self, output_len):
        s = create_string_buffer(b'0'*output_len)
        # TODO: should one use bytes or strings? in Python2/3?
        err = self.lib.CAENVME_SWRelease(s)
        return (err, s.value)







    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    #[c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    #[c_int32, c_uint32, CVAddressModifier_t]
    #[c_int32, c_uint32, CVAddressModifier_t]


    # TODO: how to pack all this identical calls into one loop?
    # TODO: and how to add the ctypes input type restrictions?
    #       the ctypes restrictions should be done before -- directly on the CDLL methods
    #       these are regular Python methods
    def CAENVME_BoardFWRelease(self, output_len):
        '''CAENVME_BoardFWRelease(self, output_len)

        [c_int32, c_char_p]
        '''
        s = create_string_buffer(b'0'*output_len)
        # TODO: should one use bytes or strings? in Python2/3?
        err = self.lib.CAENVME_BoardFWRelease(self.device_handler, s)

        return (err, s.value)

    def CAENVME_DriverRelease(self, output_len):
        '''CAENVME_DriverRelease(self)

        [c_int32, c_char_p]
        '''
        s = create_string_buffer(b'0'*output_len)
        err = self.lib.CAENVME_DriverRelease(self.device_handler, s)
        return (err, s.value)

    def CAENVME_DeviceReset(self):
        '''CAENVME_DeviceReset(self)

        [c_int32]
        '''
        return (self.lib.CAENVME_DeviceReset(self.device_handler))

    def CAENVME_End(self):
        '''CAENVME_End(self)

        [c_int32]
        '''
        return (self.lib.CAENVME_End(self.device_handler))

    def CAENVME_ReadCycle(self, address, output_len, address_modifier, data_width):
        '''CAENVME_ReadCycle(self, address, output_len, address_modifier, data_width)

        [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        '''
        s = create_string_buffer(b'0'*output_len) # TODO: data_width probably sets the output len
        err = self.lib.CAENVME_ReadCycle(self.device_handler,
                                         c_uint32(address),
                                         s,
                                         CVAddressModifier_t(address_modifier),
                                         CVDataWidth_t(data_width))
        return (err, s.value)

    def CAENVME_RMWCycle(self, address, output_len, address_modifier, data_width):
        '''CAENVME_RMWCycle(self, address, output_len, address_modifier, data_width)

        [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        '''
        s = create_string_buffer(b'0'*output_len)
        err = self.lib.CAENVME_RMWCycle(self.device_handler,
                                        c_uint32(address),
                                        s,
                                        CVAddressModifier_t(address_modifier),
                                        CVDataWidth_t(data_width))
        return (err, s.value)

    def CAENVME_WriteCycle(self, address, data, address_modifier, data_width):
        '''CAENVME_WriteCycle(self, address, data, address_modifier, data_width)

        data is bytes, i.e. b'\x02', b'\x02\x04\xa3\x1f' etc (TODO: it is both Python2/3 compatible)

        [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t]
        '''
        # s = create_string_buffer(b'0'*output_len)
        # bytes should convert strings and bytes/bytearrays to ctypes-compatible format in both Python2/3
        s = create_string_buffer(bytes(data))
        err = self.lib.CAENVME_WriteCycle(self.device_handler,
                                          c_uint32(address),
                                          s,
                                          CVAddressModifier_t(address_modifier),
                                          CVDataWidth_t(data_width))
        return (err, s.value)


    # TODO: here the output is int32 (according to the header), why?
    def CAENVME_MultiRead(self, addresses, address_modifiers, data_widths):
        '''CAENVME_MultiRead(self, addresses, address_modifiers, data_widths)

        [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)]
        '''
        length = len(addresses)
        ads = (c_uint32 * length)(*addresses)
        ad_mods = (CVAddressModifier_t * length)(*address_modifiers)
        dt_wths = (CVDataWidth_t  * length)(*data_widths)
        e_codes = (CVErrorCodes_t * length)(*range(length))
        s = (c_uint32 * length)(*range(length))
        err = self.lib.CAENVME_MultiRead(self.device_handler,
                                         ads,
                                         s,
                                         c_int(length),
                                         ad_mods,
                                         dt_wths,
                                         e_codes)
        return (err, list(s), list(e_codes))
        # return self.lib.CAENVME_MultiRead(self.device_handler, *args)

    def CAENVME_MultiWrite(self, addresses, data, address_modifiers, data_widths):
        '''CAENVME_MultiWrite(self, addresses, data, address_modifiers, data_widths)

        TODO: for some reason multiwrite requires uint32 on input
        thus data has to be a list of integers
        TODO: make compatible with bytes input

        [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)]
        '''
        length = len(addresses)
        ads = (c_uint32 * length)(*addresses)
        ad_mods = (CVAddressModifier_t * length)(*address_modifiers)
        dt_wths = (CVDataWidth_t  * length)(*data_widths)
        e_codes = (CVErrorCodes_t * length)(*range(length))
        s = (c_uint32 * length)(*data)
        err = self.lib.CAENVME_MultiWrite(self.device_handler,
                                         ads,
                                         s,
                                         c_int(length),
                                         ad_mods,
                                         dt_wths,
                                         e_codes)
        return (err, list(e_codes))

    def CAENVME_BLTReadCycle(self, address, size, address_modifier, data_width):
        '''CAENVME_BLTReadCycle(self, address, size, address_modifier, data_width)

        size -- size of transfer in bytes
        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
        '''
        s = create_string_buffer(b'0'*size*data_width)
        count = c_int(-1)
        err = self.lib.CAENVME_BLTReadCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            CVDataWidth_t(data_width),
                                            pointer(count))
        return (err, s.value, count.value)
        # return self.lib.CAENVME_BLTReadCycle(self.device_handler, *args)

    def CAENVME_FIFOBLTReadCycle(self, address, size, address_modifier, data_width):
        '''CAENVME_FIFOBLTReadCycle(self, address, size, address_modifier, data_width)

        size -- size of transfer in bytes
        (int32_t Handle, uint32_t Address, void *Buffer,
         int Size, CVAddressModifier AM, CVDataWidth DW, int *count)
        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
        '''
        s = create_string_buffer(b'0'*size*data_width)
        count = c_int(-1)
        err = self.lib.CAENVME_FIFOBLTReadCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            CVDataWidth_t(data_width),
                                            pointer(count))
        return (err, s.value, count.value)

    '''
    # self.lib.CAENVME_MBLTReadCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    # self.lib.CAENVME_FIFOMBLTReadCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    # self.lib.CAENVME_BLTWriteCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
    # self.lib.CAENVME_FIFOBLTWriteCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
    # self.lib.CAENVME_MBLTWriteCycle.argtypes     = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    # self.lib.CAENVME_FIFOMBLTWriteCycle.argtypes = [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
    self.lib.CAENVME_ADOCycle.argtypes  = [c_int32, c_uint32, CVAddressModifier_t]
    self.lib.CAENVME_ADOHCycle.argtypes = [c_int32, c_uint32, CVAddressModifier_t]
    '''

    def CAENVME_MBLTReadCycle(self, address, size, address_modifier):
        '''CAENVME_MBLTReadCycle(self, address, size, address_modifier)

        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
        '''
        s = create_string_buffer(b'0'*size)
        count = c_int(-1)
        err = self.lib.CAENVME_MBLTReadCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            pointer(count))
        return (err, s.value, count.value)

    def CAENVME_FIFOMBLTReadCycle(self, address, size, address_modifier):
        '''CAENVME_FIFOMBLTReadCycle(self, address, size, address_modifier)

        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
        '''
        s = create_string_buffer(b'0'*size)
        count = c_int(-1)
        err = self.lib.CAENVME_FIFOMBLTReadCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            pointer(count))
        return (err, s.value, count.value)

    def CAENVME_BLTWriteCycle(self, address, data, size, address_modifier, data_width):
        '''CAENVME_BLTWriteCycle(self, address, data, address_modifier, data_width)

        data is bytes, i.e. b'\x02', b'\x02\x04\xa3\x1f' etc (TODO: it is both Python2/3 compatible)
        size is int, amount of bytes to write (thus data can have 0 character)

        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
        '''
        # s = create_string_buffer(b'0'*size*data_width)
        # bytes should convert strings and bytes/bytearrays to ctypes-compatible format in both Python2/3
        s = create_string_buffer(bytes(data[:size] + b'0'*(size-len(data))))
        count = c_int(-1)
        # print("calling")
        err = self.lib.CAENVME_BLTWriteCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            CVDataWidth_t(data_width),
                                            pointer(count))
        # print("done")
        return (err, count.value)

    def CAENVME_FIFOBLTWriteCycle(self, address, data, size, address_modifier, data_width):
        '''CAENVME_FIFOBLTWriteCycle(self, address, data, size, address_modifier, data_width)

        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)]
        '''
        s = create_string_buffer(bytes(data[:size] + b'0'*(size-len(data))))
        count = c_int(-1)
        err = self.lib.CAENVME_FIFOBLTWriteCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            CVDataWidth_t(data_width),
                                            pointer(count))
        return (err, count.value)

    def CAENVME_MBLTWriteCycle(self, address, data, size, address_modifier):
        '''CAENVME_MBLTWriteCycle(self, address, data, size, address_modifier)

        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
        '''
        s = create_string_buffer(bytes(data[:size] + b'0'*(size-len(data))))
        count = c_int(-1)
        err = self.lib.CAENVME_MBLTWriteCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            pointer(count))
        return (err, count.value)

    def CAENVME_FIFOMBLTWriteCycle(self, address, data, size, address_modifier):
        '''CAENVME_FIFOMBLTWriteCycle(self, address, data, size, address_modifier)

        [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)]
        '''
        s = create_string_buffer(bytes(data[:size] + b'0'*(size-len(data))))
        count = c_int(-1)
        err = self.lib.CAENVME_FIFOMBLTWriteCycle(self.device_handler,
                                            c_uint32(address),
                                            s,
                                            c_int(size),
                                            CVAddressModifier_t(address_modifier),
                                            pointer(count))
        return (err, count.value)


    def CAENVME_ADOCycle(self, address, address_modifier):
        '''CAENVME_ADOCycle(self, address, address_modifier)

        [c_int32, c_uint32, CVAddressModifier_t]
        '''
        return self.lib.CAENVME_ADOCycle(self.device_handler, c_uint32(address), CVAddressModifier_t(address_modifier))

    def CAENVME_ADOHCycle(self, address, address_modifier):
        '''CAENVME_ADOHCycle(self, address, address_modifier)

        [c_int32, c_uint32, CVAddressModifier_t]
        '''
        return self.lib.CAENVME_ADOHCycle(self.device_handler, c_uint32(address), CVAddressModifier_t(address_modifier))


'''
    def CAENVME_IACKCycle(self, *args):
        return self.lib.CAENVME_IACKCycle(self.device_handler, *args)

    def CAENVME_IRQCheck(self, *args):
        return self.lib.CAENVME_IRQCheck(self.device_handler, *args)

    def CAENVME_IRQEnable(self, *args):
        return self.lib.CAENVME_IRQEnable(self.device_handler, *args)

    def CAENVME_IRQDisable(self, *args):
        return self.lib.CAENVME_IRQDisable(self.device_handler, *args)

    def CAENVME_IRQWait(self, *args):
        return self.lib.CAENVME_IRQWait(self.device_handler, *args)

    def CAENVME_SetPulserConf(self, *args):
        return self.lib.CAENVME_SetPulserConf(self.device_handler, *args)

    def CAENVME_SetScalerConf(self, *args):
        return self.lib.CAENVME_SetScalerConf(self.device_handler, *args)

    def CAENVME_SetOutputConf(self, *args):
        return self.lib.CAENVME_SetOutputConf(self.device_handler, *args)

    def CAENVME_SetInputConf(self, *args):
        return self.lib.CAENVME_SetInputConf(self.device_handler, *args)

    def CAENVME_GetPulserConf(self, *args):
        return self.lib.CAENVME_GetPulserConf(self.device_handler, *args)

    def CAENVME_GetScalerConf(self, *args):
        return self.lib.CAENVME_GetScalerConf(self.device_handler, *args)

    def CAENVME_GetOutputConf(self, *args):
        return self.lib.CAENVME_GetOutputConf(self.device_handler, *args)

    def CAENVME_GetInputConf(self, *args):
        return self.lib.CAENVME_GetInputConf(self.device_handler, *args)

    def CAENVME_ReadRegister(self, *args):
        return self.lib.CAENVME_ReadRegister(self.device_handler, *args)

    def CAENVME_WriteRegister(self, *args):
        return self.lib.CAENVME_WriteRegister(self.device_handler, *args)

    def CAENVME_SetOutputRegister(self, *args):
        return self.lib.CAENVME_SetOutputRegister(self.device_handler, *args)

    def CAENVME_ClearOutputRegister(self, *args):
        return self.lib.CAENVME_ClearOutputRegister(self.device_handler, *args)

    def CAENVME_PulseOutputRegister(self, *args):
        return self.lib.CAENVME_PulseOutputRegister(self.device_handler, *args)

    def CAENVME_ReadDisplay(self, *args):
        return self.lib.CAENVME_ReadDisplay(self.device_handler, *args)

    def CAENVME_SetArbiterType(self, *args):
        return self.lib.CAENVME_SetArbiterType(self.device_handler, *args)

    def CAENVME_SetRequesterType(self, *args):
        return self.lib.CAENVME_SetRequesterType(self.device_handler, *args)

    def CAENVME_SetReleaseType(self, *args):
        return self.lib.CAENVME_SetReleaseType(self.device_handler, *args)

    def CAENVME_SetBusReqLevel(self, *args):
        return self.lib.CAENVME_SetBusReqLevel(self.device_handler, *args)

    def CAENVME_SetTimeout(self, *args):
        return self.lib.CAENVME_SetTimeout(self.device_handler, *args)

    def CAENVME_SetLocationMonitor(self, *args):
        return self.lib.CAENVME_SetLocationMonitor(self.device_handler, *args)

    def CAENVME_SetFIFOMode(self, *args):
        return self.lib.CAENVME_SetFIFOMode(self.device_handler, *args)

    def CAENVME_GetArbiterType(self, *args):
        return self.lib.CAENVME_GetArbiterType(self.device_handler, *args)

    def CAENVME_GetRequesterType(self, *args):
        return self.lib.CAENVME_GetRequesterType(self.device_handler, *args)

    def CAENVME_GetReleaseType(self, *args):
        return self.lib.CAENVME_GetReleaseType(self.device_handler, *args)

    def CAENVME_GetBusReqLevel(self, *args):
        return self.lib.CAENVME_GetBusReqLevel(self.device_handler, *args)

    def CAENVME_GetTimeout(self, *args):
        return self.lib.CAENVME_GetTimeout(self.device_handler, *args)

    def CAENVME_GetFIFOMode(self, *args):
        return self.lib.CAENVME_GetFIFOMode(self.device_handler, *args)

    def CAENVME_SystemReset(self, *args):
        return self.lib.CAENVME_SystemReset(self.device_handler, *args)

    def CAENVME_ResetScalerCount(self, *args):
        return self.lib.CAENVME_ResetScalerCount(self.device_handler, *args)

    def CAENVME_EnableScalerGate(self, *args):
        return self.lib.CAENVME_EnableScalerGate(self.device_handler, *args)

    def CAENVME_DisableScalerGate(self, *args):
        return self.lib.CAENVME_DisableScalerGate(self.device_handler, *args)

    def CAENVME_StartPulser(self, *args):
        return self.lib.CAENVME_StartPulser(self.device_handler, *args)

    def CAENVME_StopPulser(self, *args):
        return self.lib.CAENVME_StopPulser(self.device_handler, *args)

    def CAENVME_WriteFlashPage(self, *args):
        return self.lib.CAENVME_WriteFlashPage(self.device_handler, *args)

    def CAENVME_ReadFlashPage(self, *args):
        return self.lib.CAENVME_ReadFlashPage(self.device_handler, *args)

    def CAENVME_EraseFlashPage(self, *args):
        return self.lib.CAENVME_EraseFlashPage(self.device_handler, *args)

    def CAENVME_BLTReadAsync(self, *args):
        return self.lib.CAENVME_BLTReadAsync(self.device_handler, *args)

    def CAENVME_BLTReadWait(self, *args):
        return self.lib.CAENVME_BLTReadWait(self.device_handler, *args)
'''


if __name__ == '__main__':
    oper = PreVMEOperator(sys.argv[1])

    dem = Pyro4.Daemon()
    uri = dem.register(oper)
    print( uri )

    dem.requestLoop()

    # TODO: how to exit the demon correctly? calling end and so on
