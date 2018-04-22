import logging
import argparse
from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
import CAENVMEdefinitions
from CAENVMEdefinitions import cvSuccess, CVBoardTypes_t, CVAddressModifier_t, CVDataWidth_t, CVErrorCodes_t, CAENVME_API
import sys

c_uint32_p = POINTER(c_uint32)
c_int32_p = POINTER(c_int32)


'''
a prototype for just talking on the VME bus


# what it does and протокольность

it does VME EVAL:

1. parse the minilanguage of C input params
2. and make corresponding call on the library

-- simple split



## протокольность

модуль должен объявлять удобные функции для шины
и давать утилиту для тестов на __main__

удобная функция:

1. мини-язык для произвольных С вызовов
   C вызов = <return value> <func_name>(<input/output params>)
   & некоторые из <input/output params> это указатели для вывода

   т.е. здесь под-функции:

   * определение этих <input/output params> вообще
   * обработка самого вызова: что делать с <return>? что с <output>?

   для "протокольности" нужна функция, которую легко использовать в других программах
   <output> должен быть выводом функции, а <return> должен проверяться на ошибку

   <return> = ошибка это в VME lib-е,
   лучше сделать С-only систему и просто возвращать (<return>, [<outputs>])
   проверка ретурна -- для юзера

   как делать инпут такой системы? 1) строкой миниязыка?
   2) или уже конкретными С-параметрами, а строку парсит отедльная функция?
   стоит выделить 2), т.е.:

   * надо передавать параметры + какие из них <output> -- (par, isOut? = True/False)
   * возвращать (<ret>, [<outs>])

   сейчас это выглядит так:

       # VME EVAL
       arguments, output_arguments = parse_vme_arguments(args.arguments)
       err = eval('lib.%s(*arguments)' % args.command)
       logging.debug('error: %s' % err)
       for a in output_arguments:
           print(a.value)

   -- done! call_lib

   теперь за язык:
   
   * dev не должен быть встроен и не нужно его передавать с консоли
   * язык должен быть общим -- парсить строки в С типы
     а dev добавляем вручную,
     так как консольное приложение это не для С-вызовов
     а для вызовов шины
   * наконец удобнее язык будет с: `[out,]char[:8][=initval]`

   -- таки да, можно расширять язык на полный набор С параметров

2. соотв-нно какая-то проверка вызовов библиотеки,
   т.к. возникают странные ошибки с неверными вызовами,
   -- добавить тот питоновский список всех вызовов библиотеки

   это не только проверка, а конкретизация системы "С вызовов вообще" на вызовы данной библиотеки,
   т.е. заданы типы переменных и что вывод/что нет (как в datasheet!)
   и только сами значения передаются



# TODO:

input params language:

    char[8],out or char:8,out or char:8=out etc

the question is which arguments are for output?

'''

def parse_vme_arguments(comline_args):
    '''parse_vme_arguments(comline_args)

    minilang parsing comline arguments into C function calls

    [out,]<type>[:<N vect>][=<init val>]

    returns [(arg, isOut?)]
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


def call_lib(lib, func_name, args):
    '''call_lib(lib, func_name, args):

    запрашивает: 1) библиотеку для вызова, 2) имя функции
    3) параметры + какие из них <output>, args = [(par, isOut? = True/False)]
    возвращает (<ret>, [<outs>])
    '''

    logging.debug('arguments for lib call = %s' % repr(args))

    arguments = [a for a, _ in args]
    outs = [a for a, isOut in args if isOut]
    ret = eval('lib.%s(*arguments)' % func_name)

    return ret, outs


'''
type test and other lib info
(electronics datasheet or other programmable desciption of the interface, like `objdump` etc)

пока две простые вещи, те же что и в вызовах функций
1) проверка типа
2) + какие параметры выводные

записать их в ямл и парсить ямл
-- позже из ямла можно будет сделать спец. объекты и пр.
в целом это универсальный и читаемый формат, подходит для спецификации

но пока запишем в питоновские структуры
'''

class param_def:
    "defines type, name (nickname, description) and out/in/ret behaviour of parameter"

    def __init__(self, c_type, name=None, behaviour='in'):
        #
        self.c_type = c_type


vme_bus_datasheet = {
'CAENVME_SWRelease'      : [[CAENVME_API, 'ret'], [c_char_p, 'SwRel' , 'out']],
'CAENVME_End'            : [[CAENVME_API, 'ret'], [c_int32,  'Handle', ]],
'CAENVME_DeviceReset'    : [[CAENVME_API, 'ret'], [c_int32,  'Handle', ]],
'CAENVME_BoardFWRelease' : [[CAENVME_API, 'ret'], [c_int32,  'Handle', ], [c_char_p, 'FWRel',   'out']],
'CAENVME_DriverRelease'  : [[CAENVME_API, 'ret'], [c_int32,  'Handle', ], [c_char_p, 'Rel'  ,   'out']],
'CAENVME_ReadCycle'      : [[CAENVME_API, 'ret'], [c_int32,  'Handle', ], [c_uint32, 'Address', ], [c_char_p, 'Data', 'out'],
                            [CVAddressModifier_t, 'AM'], [CVDataWidth_t, 'DW']],
'CAENVME_WriteCycle'     : [[CAENVME_API, 'ret'], [c_int32,  'Handle', ], [c_uint32, 'Address', ], [c_char_p, 'Data'],
                            [CVAddressModifier_t, 'AM'], [CVDataWidth_t, 'DW']],
}

def typecheck_call(func_name, args):
    # skip the ret type
    data_types = [par_def[0] for par_def in vme_bus_datasheet[func_name][1:]]
    logging.debug(data_types)
    logging.debug(args)
    return len(data_types) == len(args) and all(isinstance(arg, data_t) for data_t, arg in zip(data_types, args))

prelim_vme_bus_datasheet_full = {
'CAENVME_SWRelease':      [c_char_p],
'CAENVME_End':            [c_int32],
'CAENVME_BoardFWRelease': [c_int32, c_char_p],
'CAENVME_DriverRelease':  [c_int32, c_char_p],
'CAENVME_DeviceReset':    [c_int32],
'CAENVME_ReadCycle':      [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t],
'CAENVME_RMWCycle':       [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t],
'CAENVME_WriteCycle':     [c_int32, c_uint32, c_char_p, CVAddressModifier_t, CVDataWidth_t],

'CAENVME_MultiRead':      [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)],
'CAENVME_MultiWrite':     [c_int32, c_uint32_p, c_uint32_p, c_int32, POINTER(CVAddressModifier_t), POINTER(CVDataWidth_t), POINTER(CVErrorCodes_t)],

'CAENVME_BLTReadCycle':   [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)],
'CAENVME_FIFOBLTReadCycle': [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)],

'CAENVME_MBLTReadCycle':     [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)],
'CAENVME_FIFOMBLTReadCycle': [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)],

'CAENVME_BLTWriteCycle':     [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)],
'CAENVME_FIFOBLTWriteCycle': [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, CVDataWidth_t, POINTER(c_int)],

'CAENVME_MBLTWriteCycle':     [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)],
'CAENVME_FIFOMBLTWriteCycle': [c_int32, c_uint32, c_char_p, c_int, CVAddressModifier_t, POINTER(c_int)],

'CAENVME_ADOCycle':  [c_int32, c_uint32, CVAddressModifier_t],
'CAENVME_ADOHCycle': [c_int32, c_uint32, CVAddressModifier_t],
}



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "run VME bus command",
        epilog = """Examples:
    python3 vmebus.py CAENVME_SWRelease charp=________
    python3 vmebus.py CAENVME_BoardFWRelease charp=________
    python3 vmebus.py CAENVME_ReadCycle uint32=0xa10 charp=______________ AM=2 DW=3
    """)


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

    # VME EVAL
    arguments = parse_vme_arguments(args.arguments)
    # only 1 VMElib call does not require dev
    if args.command != 'CAENVME_SWRelease':
        arguments = [dev] + arguments

    #err = eval('lib.%s(*arguments)' % args.command)
    assert typecheck_call(args.command, arguments)
    #arguments = [(a, len(vme_bus_datasheet[args.command])>2 and vme_bus_datasheet[args.command][2] == 'out') for a in arguments]
    arguments = [(a, len(arg_def)>2 and arg_def[2] == 'out') for a, arg_def in zip(arguments, vme_bus_datasheet[args.command][1:])]
    logging.debug(repr(arguments))
    err, output_arguments = call_lib(lib, args.command, arguments)
    logging.debug('error: %s' % err)
    for a in output_arguments:
        print(a.value)

    # exit
    err = lib.CAENVME_End(dev)
    logging.debug('VME end w. error: %s' % err)

    sys.exit(err)

else:
    logging.basicConfig(level=logging.DEBUG)

