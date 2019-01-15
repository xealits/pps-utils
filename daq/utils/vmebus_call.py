"""
commandline utility for bus sessions
"""

import argparse, logging
import sys
from os.path import isfile
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
from CAENVMEdefinitions import cvSuccess, CVBoardTypes_t, CVAddressModifier_t, CVDataWidth_t, CVErrorCodes_t, CAENVME_API
import string

parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter,
    description = "run VME bus command",
    epilog = """Examples:
python3 vmebus_call.py CAENVME_SWRelease ________
python3 vmebus_call.py CAENVME_BoardFWRelease ________
python3 vmebus_call.py CAENVME_ReadCycle 0xa10 ______________ 2 3
""")


parser.add_argument("command", help='command name')
parser.add_argument("--debug", action='store_true', help='logging level DEBUG')
parser.add_argument("--lib-path", type=str, help='custom path to the VME lib')
parser.add_argument('inits', nargs='*', help='initialization of command arguments')


args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

import vmebus

if args.lib_path:
    bus = vmebus.VMEBus(args.lib_path)
else:
    bus = vmebus.VMEBus()

#def parse_bus_arguments(comline_args):

'''
объект-шина = сессия на шине, имеет свой интерфейс, не равный интерфейсу библиотеки

командная строка даёт вводные параметры именно этому интерфейсу

полный смысл ввода может зависеть от смысла параметров для шины (адрес не адрес?)
и от смысла ввода для карточек (парсить название карты и её регистры?)

-- в общем нужна полная инфа для интерфейса сессии (объекта-шины), a не только для библиотеки
'''

## parse the minilanguage for address inputs
## find the address inputs according to the vme bus datasheet
#vme_def = bus.command_full_args(args.command, )
#parsed_arguments = []
#for arg, arg_def in zimp(args.arguments, vme_def):
#    if arg_def

# the "datasheet" of cards
cards = {'tdc': {'status': '10a0', 'ctr': '10a1'}}

parsed_arguments = []
for arg in args.inits:
    if '@' in arg:
        cardname, addresses = arg.strip().split('@')

        if cardname not in cards:
            raise ValueError('the cardname "%s" is not available' % cardname)
        card = cards[cardname]

        global_addr, reg = addresses.split(':')
        # TODO: how to properly glue all these bits? global:register
        # for now just concat strings, hopefully it is always correct
        if reg in card:
            # then it's a name of the register
            addr = global_addr + card[reg]
        elif all(b in string.hexdigits for b in reg):
            # then it's explicit register address
            addr = global_addr + reg
        else:
            raise ValueError('wrong register definition, neither name nor hex: %s' % arg)

        parsed_arguments.append(addr)

    else:
        parsed_arguments.append(arg)

# relay on robust conversion from python objects to bus by the bus object
# pass strings or ints -- they are converted as in the datasheet
err, output_arguments = bus.call(args.command, parsed_arguments)

logging.debug('error: %s' % err)
for a in output_arguments:
    print(a.value)

sys.exit(err)


