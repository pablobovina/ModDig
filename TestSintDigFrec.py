import ctypes
from Usb import Usb
from time import sleep

"""
vid_pid_norm = "vid_04d8&pid_000c"
out_pipe = "\\MCHP_EP1"
in_pipe = "\\MCHP_EP1"
mcpUsbApi = ctypes.CDLL("./Microchip/mpusbapi.dll")
selection = 0
cadena =  list(chr(0x00)*64)
cadena[0] = "g"
cadena[1] = chr(0x73)
cadena = "".join(cadena)

SendData = ctypes.create_string_buffer(cadena)
SentDataLength = (ctypes.c_ulong*1)()
ctypes.cast(SentDataLength, ctypes.POINTER(ctypes.c_ulong))
SendDelay = 10000
SendLength = len(cadena)

ReceiveData = ctypes.create_string_buffer(64)
ReceiveLength = (ctypes.c_ulong*1)()
ctypes.cast(ReceiveLength, ctypes.POINTER(ctypes.c_ulong))
ReceiveDelay = 15000
ExpectedReceiveLength = len(ReceiveData)

devcount = mcpUsbApi._MPUSBGetDeviceCount(vid_pid_norm)
myOutPipe = mcpUsbApi._MPUSBOpen(selection, vid_pid_norm, out_pipe, 0, 0)
myInPipe = mcpUsbApi._MPUSBOpen(selection, vid_pid_norm, in_pipe, 1, 0)
mcpUsbApi._MPUSBWrite(myOutPipe,SendData, SendLength, SentDataLength, SendDelay)
mcpUsbApi._MPUSBRead(myInPipe, ReceiveData, ExpectedReceiveLength, ReceiveLength, ReceiveDelay)
#print str(ReceiveData[0])+str(ReceiveData[1])+str(ReceiveData[2])+str(ReceiveData[3])
s = [str(ReceiveData[i]) for i in range(0,64)]
print "".join(s)
"""


def _freq_parts(freq, freq1=200000000):
    calculo = (freq * 281474976710656) / freq1
    w5 = calculo / 1099511627776  # divide por 2 ^ 40
    calculo = calculo - (w5 * 1099511627776)
    w4 = calculo / 4294967296  # divide por 2 ^ 32
    calculo = calculo - (w4 * 4294967296)
    w3 = calculo / 16777216  # divide por 2 ^ 24
    calculo = calculo - (w3 * 16777216)
    w2 = calculo / 65536  # divide por 2 ^ 16
    calculo = calculo - (w2 * 65536)
    w1 = calculo / 256  # divide por 2 ^ 8
    w0 = calculo - (w1 * 256)
    return [w0, w1, w2, w3, w4, w5]

import binascii

print _freq_parts(2**48)
print "{0:b}".format(2**38)
#binascii.unhexlify(str(hex (10000000)))
def _get_code():
    u = Usb()
    b = u.request(['b', chr(0x71), chr(0x00)], 4)
    s = [str(b[i]) for i in range(0,4)]
    print "".join(s)
    sleep(2)
    d = u.request(['g', chr(0x77), chr(0x00)], 4)
    s = [str(d[i]) for i in range(0,4)]
    print "".join(s)
