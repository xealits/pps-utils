import logging
import argparse
from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
import CAENVMEdefinitions
from CAENVMEdefinitions import cvSuccess, CVBoardTypes_t, CVAddressModifier_t, CVDataWidth_t
import sys

'''
a prototype for just talking on the VME bus
'''

parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter,
    description = "run VME bus command",
    epilog = """Examples:
python3 vmebus.py CAENVME_SWRelease char,8,out
python3 vmebus.py CAENVME_BoardFWRelease dev char,128,out
python3 vmebus.py CAENVME_ReadCycle dev uint32,0xa10 char,32,out AM,2 DW,3
"""
    )

parser.add_argument("command", help="command name")
parser.add_argument("--debug", action='store_true', help="logging level DEBUG")
parser.add_argument('arguments', nargs='*', help='command arguments')


args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

libpath = './libCAENVME.so'
cdll.LoadLibrary( libpath ) # TODO: if error -- break
lib = CDLL( libpath )

# parameters to init board
'''
      [in]  BdType    : The model of the bridge (V1718/V2718).
      [in]  Link      : The link number (don't care for V1718).                                                         
      [in]  BdNum     : The board number in the link.
      [out] Handle    : The handle that identifies the device.
'''

board_type = CAENVMEdefinitions.cvV2718.value # this is the VME bridge board
link  = 0
bdnum = 0 # board number in the link -- what does that mean?
# this is the device number of out connection
# usually it gets = 0
dev = c_int32()

err = lib.CAENVME_Init(CVBoardTypes_t(board_type), link, bdnum, byref(dev))
logging.debug('VME init w. error: %s' % err)
if err != cvSuccess.value:
    logging.error("VME_Init error %s" % err)
    sys.exit(1)

## release versions
#output_len = 16 # bytes
#s = create_string_buffer(b'0'*output_len)
#err = lib.CAENVME_SWRelease(s)

def parse_vme_arguments(comline_args):
    '''parse_vme_arguments(comline_args)

    minilang parsing comline arguments into C function calls
    '''

    all_arguments = []
    output_arguments = []
    for arg in comline_args:
        # most of commands require device handle
        # only very few don't
        # but for now for simplicity and generality
        # always explicitly all arguments are passed from comline
        # therefore parsing the device handle case:

        if arg == 'dev':
            all_arguments.append(dev)
            continue

        # char:20
        if arg[:4] == 'char':
            length = int(arg.split(',')[1])
            the_argument = create_string_buffer(b'0'*length)
        elif arg[:6] == 'uint32':
            # type:value -- value is integer in hex!
            address = int(arg.split(',')[1], 16)
            the_argument = c_uint32(address)
        elif arg[:2] == 'AM':
            # AM:value (integer value)
            value = int(arg.split(',')[1])
            the_argument = CVAddressModifier_t(address)
        elif arg[:2] == 'DW':
            # DW:value (integer value)
            value = int(arg.split(',')[1])
            the_argument = CVDataWidth_t(address)
        else:
            logging.error('unknown argument arg: %s' % arg)
            continue

        all_arguments.append(the_argument)
        if 'out' in arg:
            output_arguments.append(the_argument)

    return all_arguments, output_arguments

arguments, output_arguments = parse_vme_arguments(args.arguments)
err = eval('lib.%s(*arguments)' % args.command)
logging.debug('error: %s' % err)
for a in output_arguments:
    print(a.value)

# exit
err = lib.CAENVME_End(dev)
logging.debug('VME end w. error: %s' % err)

sys.exit(err)


