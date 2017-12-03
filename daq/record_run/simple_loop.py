from ctypes import CDLL, cdll, byref, create_string_buffer
from ctypes import POINTER, pointer, c_uint32, c_int32, c_int, c_short, c_char, c_char_p

#libc = CDLL('libc.so.6')
#s = create_string_buffer(b'foo')
#libc.printf(s)


lib = CDLL("simple_loop.so")

addrs = (c_uint32*4)()
addrs[0] = 0
addrs[1] = 1
addrs[2] = 2
addrs[3] = 3

lib.record(0, 4, addrs)

