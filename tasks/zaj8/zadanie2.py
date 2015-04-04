import ctypes
import os
import threading
import time
import struct

_fields_ = [('wd', ctypes.c_int),
        ('mask', ctypes.c_uint32),
        ('cookie', ctypes.c_uint32),
        ('len', ctypes.c_uint32),
        ('name', ctypes.c_char_p)] 

def read_notification(fd):
    r = os.read(fd, 100)   
    return r

lib = ctypes.cdll.LoadLibrary('libc.so.6')
#lib.inotify_init.restype = ctypes.c_uint32
lib.inotify_init.argtypes = []
lib.inotify_init.restype = ctypes.c_int
lib.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p,
ctypes.c_uint32]
lib.inotify_add_watch.restype = ctypes.c_int
lib.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]
lib.inotify_rm_watch.restype = ctypes.c_int
#lib.read.restype = [ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_char_p]


fd = lib.inotify_init()
print('inotify init result = %d' % fd)
# uwaga: .encode('utf-8') - sedno!!!
wwd = lib.inotify_add_watch(fd, '/home/tybur/PWZN/pwzn/tasks/zaj8/testfile.txt'.encode('utf-8'), 0x400)
print('watch descriptor = %d' % wwd)
buff = ctypes.c_void_p()

buf = ctypes.create_string_buffer(500)
size = lib.read(fd, buf, 16)
print("size of data read: %d" %size)
wd, mask, cookie, ln = struct.unpack('iIII', buf[:16])
print("wd = %d, mask = %d, cookie = %d, len = %d" % (wd, mask, cookie, ln))
name = lib.read(fd, buf, ln)
print("name = " + name)
#print("result: %s" % buf)




