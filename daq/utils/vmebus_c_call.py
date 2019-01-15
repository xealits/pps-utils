"""
commandline utility in main with expicit C calls
"""

import argparse, logging
import sys
from os.path import isfile
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
from CAENVMEdefinitions import cvSuccess, CVBoardTypes_t, CVAddressModifier_t, CVDataWidth_t, CVErrorCodes_t, CAENVME_API

parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter,
    description = "run VME bus command",
    epilog = """Examples:
python3 vmebus_c_call.py CAENVME_SWRelease charp=________
python3 vmebus_c_call.py CAENVME_BoardFWRelease charp=________
python3 vmebus_c_call.py CAENVME_ReadCycle uint32=0xa10 charp=______________ AM=2 DW=3
""")


parser.add_argument("command", help='command name')
parser.add_argument("--debug", action='store_true', help='logging level DEBUG')
parser.add_argument("--lib-path", type=str, help='custom path to the VME lib')
parser.add_argument('arguments', nargs='*', help='command arguments')


args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

import vmebus

# parameters to init board
'''
      [in]  BdType    : The model of the bridge (V1718/V2718).
      [in]  Link      : The link number (don't care for V1718).                                                         
      [in]  BdNum     : The board number in the link.
      [out] Handle    : The handle that identifies the device.
'''

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
'''

if args.lib_path:
    bus = vmebus.VMEBus(args.lib_path)
else:
    bus = vmebus.VMEBus()

## release versions
#output_len = 16 # bytes
#s = create_string_buffer(b'0'*output_len)
#err = lib.CAENVME_SWRelease(s)

'''
# VME EVAL
arguments = parse_vme_arguments(args.arguments)
# only 1 VMElib call does not require dev
if args.command != 'CAENVME_SWRelease':
    arguments = [dev] + arguments

#err = eval('lib.%s(*arguments)' % args.command)
assert typecheck_c_call(args.command, arguments)
#arguments = [(a, len(vme_bus_c_calls[args.command])>2 and vme_bus_c_calls[args.command][2] == 'out') for a in arguments]
arguments = [(a, len(arg_def)>2 and arg_def[2] == 'out') for a, arg_def in zip(arguments, vme_bus_c_calls[args.command][1:])]
logging.debug(repr(arguments))
err, output_arguments = call_lib(lib, args.command, arguments)
'''

def parse_vme_arguments(comline_args):
    '''parse_vme_arguments(comline_args)

    minilang parsing comline arguments into C function calls

    <type>[:<N vect>][=<init val>]

    returns [arg] with corresponding ctypes objects
    '''

    arguments = []
    for arg in comline_args:
        # most of commands require device handle
        # only very few don't
        # but for now for simplicity and generality
        # always explicitly all arguments are passed from comline
        # therefore parsing the device handle case:

        #if arg == 'dev':
        #    arguments.append((dev, False))
        #    continue

        logging.debug(arg)

        #isOut = arg[:4] == 'out,'
        #if isOut:
        #    arg = arg[4:]


        logging.debug(arg)
        # <type>[:<N vect>][=<init val>]
        if '=' in arg:
            arg, init_val = arg.split('=')
        else:
            init_val = None


        logging.debug(arg)
        # <type>[:<N vect>]
        if ':' in arg:
            arg, N_vect = arg.split(':')
            N_vect = int(N_vect)
        else:
            N_vect = None


        logging.debug(arg)
        # char:20
        if arg == 'charp':
            the_argument = c_char_p(bytes(init_val, 'utf'))
        elif arg == 'char' and N_vect:
            the_argument = create_string_buffer(b'0'*N_vect)
        elif arg == 'char':
            init_val = bytes(init_val, 'utf') if init_val else b'0'
            the_argument = c_char(init_val)
        elif arg == 'uint32':
            # type:value -- value is integer in hex!
            #address = int(arg.split(',')[1], 16)
            if init_val[:2] == '0x':
                init_val = int(init_val, 16) if init_val else 0
            else:
                init_val = int(init_val) if init_val else 0
            the_argument = c_uint32(init_val)
        elif arg == 'AM':
            # AM:value (integer value)
            #value = int(arg.split(',')[1])
            init_val = int(init_val) if init_val else 0
            the_argument = CVAddressModifier_t(init_val)
        elif arg == 'DW':
            # DW:value (integer value)
            #value = int(arg.split(',')[1])
            init_val = int(init_val) if init_val else 0
            the_argument = CVDataWidth_t(init_val)
        else:
            logging.error('unknown argument arg: %s' % arg)
            continue

        #arguments.append((the_argument, isOut))
        arguments.append(the_argument)
        #if 'out' in arg:
        #    output_arguments.append(the_argument)

    return arguments

'''
the cards are spaces of memory, this:

    datasheet_dict[card][register]

--- returns the address of this register on the chip

the minilanguage:

    tdc@00aa:control_register
    <card nickname>@<global address>:<register nickname>

is substituted with `<global><card[register]>` -- with some mask for the card space and global space
'''

# the input arguments are direct C types (ctypes literally)
err, output_arguments = bus.call(args.command, parse_vme_arguments(args.arguments))

"""анализ что за структура тут, насколько общая
1) работает объект VME шины
2) он делает общую операцию "call"
3) которая выполняется по названию команды и неким вводным параметрам
4) на вывод идут исходящие аргументы и ошибка
--- исходящие аргументы и ошибка это точно соотв. библиотеке,
    исходящие аргументы это часть из вводных на самом деле,
    единственное что смущает это общая операция вместо конкретных,
    но конкретные методы тяжело встроить в работу с командной строкой,
    со строчными вводами
эта общая операция может иметь смысл "in band communication"
т.е. что-то что шина делает на своей основной полосе,
но протокол же завиксирован, так что "read", "block read" должны быть захардкодены

looking into the call:
это "C call" -- вызов С-щной библиотеки
возможно С-шность вмешивается в представление шины здесь?
т.е. объект шины не достаточно инкапсулировал С-шную библиотеку,
какие-то детали остались, это недостаточно чистый "адаптер" в шину?
Единственное что инкапсулировано сейчас это передача dev номера при вызовах.

Добавил генерацию конкретных операций, позапускал.
Вроде ок, передаются только ключевые параметры, прямо по вызову, без доп. списков,
автоматически возвращается ошибка и выводные параметры.
Красота, только приходится возиться с объявлением C-шных переменных.
Нужно поделать удобных объектов типа "charp", вместе с языком для шелла.
"""

logging.debug('error: %s' % err)
for a in output_arguments:
    print(a.value)

sys.exit(err)

