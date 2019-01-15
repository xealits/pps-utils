import logging
import argparse
from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p
import CAENVMEdefinitions
from CAENVMEdefinitions import cvSuccess, CVBoardTypes_t, CVAddressModifier_t, CVDataWidth_t, CVErrorCodes_t, CAENVME_API
import sys
from os.path import isfile

c_uint32_p = POINTER(c_uint32)
c_int32_p = POINTER(c_int32)

# convenient C variables
def charp(init_val='________'):
    return c_char_p(bytes(init_val, 'utf'))


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

vme_bus_c_calls = {
'CAENVME_SWRelease'      : {'func_def': (CAENVME_API, [(c_char_p, ['SwRel' , 'out'])])},
'CAENVME_End'            : {'func_def': (CAENVME_API, [(c_int32,  ['Handle', ])])},
'CAENVME_DeviceReset'    : {'func_def': (CAENVME_API, [(c_int32,  ['Handle', ])])},
'CAENVME_BoardFWRelease' : {'func_def': (CAENVME_API, [(c_int32,  ['Handle', ]), (c_char_p, ['FWRel',   'out'])])},
'CAENVME_DriverRelease'  : {'func_def': (CAENVME_API, [(c_int32,  ['Handle', ]), (c_char_p, ['Rel'  ,   'out'])])},
'CAENVME_ReadCycle'      : {'func_def': (CAENVME_API, [(c_int32,  ['Handle', ]), (c_uint32, ['Address', ]), (c_char_p, ['Data', 'out']),
                            (CVAddressModifier_t, ['AM']), (CVDataWidth_t, ['DW'])])},
'CAENVME_WriteCycle'     : {'func_def': (CAENVME_API, [(c_int32,  ['Handle', ]), (c_uint32, ['Address', ]), (c_char_p, ['Data']),
                            (CVAddressModifier_t, ['AM']), (CVDataWidth_t, ['DW'])])},
}

def typecheck_c_call(func_name, args):
    # skip the ret type
    logging.debug('typecheck: %s , %s' % (func_name, repr(args)))
    # get the parameter types
    func_def  = vme_bus_c_calls[func_name]['func_def']
    par_types = [par_def[0] for par_def in func_def[1]]
    logging.debug(par_types)
    logging.debug(args)

    # try to convert inputs with typical python objects to ctypes:
    converted_args = []
    for n, (arg, data_t) in enumerate(zip(args, par_types)):
        #if   isinstance(arg, str):
        #    args[n] = charp(arg)
        #elif isinstance(arg, int):
        #    args[n] = data_t(arg)
        # no! convert based on the function definition
        if isinstance(arg, data_t):
            converted_args.append(arg)
        elif data_t == c_char_p:
            converted_args.append(charp(arg))
        else:
            # damn handling all the ints
            # assume hex
            converted_args.append(data_t(int(arg, 16)))

    # check all worked
    if len(par_types) == len(converted_args) and all(isinstance(arg, data_t) for arg, data_t in zip(converted_args, par_types)):
        return converted_args
    else:
        return None

# из-за консольности всё передаются текстом и не видно смысла в хардкодинге питоном, с полным объектом
# что если просто функция вызова с 1 лишь дефаултом -- dev?
# нужна одна система для обоих случаев
# пока сделаем текстовый метод "call", из которого потом сгенерируем отдельные методы

class VMEBus:
    """
    defines type, name (nickname, description) and out/in/ret behaviour of parameter

    the bus objects represents a session on a bus,
    it exhibits only essential input parameters for the bus calls in the methods
    """

    def __init__(self, lib_path='./libCAENVME.so', board_type=CAENVMEdefinitions.cvV2718.value, link=0, bdnum=0):
        """VMEBus(lib)

	creates bus connection

        board_type - this is the VME bridge board
        link  
        bdnum 
        """

        assert isfile(lib_path)
        cdll.LoadLibrary(lib_path)
        self._lib = CDLL(lib_path)

        # this is the device number of out connection
        # usually it gets = 0
        self.dev = c_int32()

        err = self._lib.CAENVME_Init(CVBoardTypes_t(board_type), link, bdnum, byref(self.dev))
        logging.debug('VME init w. error: %s' % err)
        if err != cvSuccess.value:
            logging.error("VME_Init error %s" % err)
            sys.exit(1)

    def _full_args(self, command, arguments):

        # all commands in the lib take the dev number, except the SWRelease command
        if command != 'CAENVME_SWRelease':
            arguments = [self.dev] + arguments

        return arguments

    # TODO:
    # here _full_args or some _skip_args info
    # must be used for the mapping of bus session interface to the full lib interface (adapter?)
    # which is used in both getting the full list of arguments (with some logic for defining the missing params)
    # and in getting the args info from the datasheet
    # datasheet is about the C lib
    # this bus object defines a bus session -- it's simple but a different object, there is an adapter thing between them

    def command_args_info(self, command: str, arguments: list):
        """command_full_args(self, command: str, arguments: list)

        arguments -- list of essential command arguments in the bus session
                     some arguments for the lib might be missing

        return full list of arguments, with their info from datasheet [(arg_type, [infolist])]
        """

        logging.debug('VMEBus command_full_args: %s , %s' % (command, repr(arguments)))

        # attach info
        full_args = []
        for n, arg in enumerate(arguments):
            info = vme_bus_c_calls[command]['func_def'][1][n][1]
            full_args.append((arg, info))

        return full_args

    # now, it would be nice to have help messages for each call here...
    def call(self, command: str, arguments: list):
        """call(self, command: str, arguments: list)

        command 
        arguments = [<arg>]
        """

        logging.debug('VMEBus call: %s , %s' % (command, repr(arguments)))
        # check the command is in the datasheet
        assert command in vme_bus_c_calls

        # get the full arguments list
        arguments = self._full_args(command, arguments)

        # now the list must be full for the library
        # check agains the the call type definition
        converted_args = typecheck_c_call(command, arguments)
        if not converted_args:
            raise TypeError('the input arguments have wrong type: %s vs %s' % (repr(arguments), repr(vme_bus_c_calls[command]['func_def'][1])))

        # find the out arguments according to the datasheet
        # "out" arguments are mutable inputs, pointers, which the lib uses for output
        # return [(argument, out_or_not?)]
        converted_args = [(a, 'out' in arg_def[1]) for a, arg_def in zip(converted_args, vme_bus_c_calls[command]['func_def'][1])]
        logging.debug(repr(converted_args))

        # call the c lib via the protocol of C calls
        err, output_arguments = call_lib(self._lib, command, converted_args)
        # C call to a function in the library
        # returns the return value of the function and the list of input arguments which are marked as output

        #logging.debug('error: %s' % err)
        #for a in output_arguments:
        #    print(a.value)
        return err, output_arguments

    def __del__(self):

        # exit the lib
        err = self._lib.CAENVME_End(self.dev)
        logging.debug('VME end w. error: %s' % err)


# and generate methods from the datasheet
def set_vme_c_call(command_name: str):
    assert command_name in vme_bus_c_calls
    logging.debug('dynamic setting %s' % command_name)

    def command_call(*args):
        com_self, arguments = args[0], args[1:]
        return com_self.call(command_name, list(arguments))

    # TODO: these calls lack proper help, with doc string and function def, metaprograming is needed
    command_call.__name__ = command_name
    inp_string = ', '.join(str(i) for i in vme_bus_c_calls[command_name]['func_def'][1] if 'Handle' not in i[1])
    out_string = str(vme_bus_c_calls[command_name]['func_def'][0])
    doc_string = "expects = {inp}\nreturns = {out}".format(inp=inp_string, out=out_string)
    command_call.__doc__  = doc_string
    logging.debug('dynamic setting %s doc_string %s' % (command_name, doc_string))

    setattr(VMEBus, command_name, command_call)

# just syntactic convenience over the "call" method
for command_name, _ in vme_bus_c_calls.items():
    logging.debug('generating VMEBus attribute %s' % command_name)
    set_vme_c_call(command_name)

'''
isn't it entangled now? - no, it's fine
It's a datasheet, which among other stuff contains C lib description with all the calls.
This python module semi-generates a python representation of the bus, including the calls via the lib.
Basically python's representation is a pythonic object making the C calls of the lib + some more docs from the datasheet.
'''


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

logging.debug('vmebus is done')
