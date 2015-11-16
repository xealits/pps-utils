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
        cdll.LoadLibrary( libpath )
        # initialize the CDLL object
        super(PreVMEOperator, self).__init__(libpath)
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

        err = self.CAENVME_End( self.device_handler )
        if err != cvSuccess:
            print("CAENVME_Init error %s" % err)
            return err

        self.buffers = None

        # when everything is closed -- go back to not-init state
        self.__class__ = PreVMEOperator
