import logging
import argparse
from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
import CAENVMEdefinitions
from CAENVMEdefinitions import cvSuccess, CVBoardTypes_t, CVAddressModifier_t, CVDataWidth_t
import sys



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

        isOut = arg[:4] == 'out,'
        if isOut:
            arg = arg[4:]

        # <type>[:<N vect>][=<init val>]
        if '=' in arg:
            arg, init_val = arg.split('=')
        else:
            init_val = None

        # <type>[:<N vect>]
        if ':' in arg:
            arg, N_vect = arg.split(':')
            N_vect = int(N_vect)
        else:
            N_vect = None

        # char:20
        if arg == 'char' and N_vect:
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

        arguments.append((the_argument, isOut))
        #if 'out' in arg:
        #    output_arguments.append(the_argument)

    return arguments


def call_lib(lib, func_name, args):
    '''call_lib(lib, func_name, args):

    запрашивает: 1) библиотеку для вызова, 2) имя функции
    3) параметры + какие из них <output> -- (par, isOut? = True/False)
    возвращает (<ret>, [<outs>])
    '''

    logging.debug('arguments for lib call = %s' % repr(args))

    arguments = [a for a, _ in args]
    outs = [a for a, isOut in args if isOut]
    ret = eval('lib.%s(*arguments)' % func_name)

    return ret, outs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "run VME bus command",
        epilog = """Examples:
    python3 vmebus.py CAENVME_SWRelease out,char:8
    python3 vmebus.py CAENVME_BoardFWRelease out,char:128
    python3 vmebus.py CAENVME_ReadCycle uint32=0xa10 out,char:32 AM=2 DW=3
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

    # VME EVAL
    arguments = parse_vme_arguments(args.arguments)
    # only 1 VMElib call does not require dev
    if args.command != 'CAENVME_SWRelease':
        arguments = [(dev, False)] + arguments

    #err = eval('lib.%s(*arguments)' % args.command)
    err, output_arguments = call_lib(lib, args.command, arguments)
    logging.debug('error: %s' % err)
    for a in output_arguments:
        print(a.value)

    # exit
    err = lib.CAENVME_End(dev)
    logging.debug('VME end w. error: %s' % err)

    sys.exit(err)

