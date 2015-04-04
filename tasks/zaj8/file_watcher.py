import ctypes
import os
import threading
import time
import struct
import select
from multiprocessing import Queue


mask_dict = {0x00000001: ('IN_ACCESS',"File was accessed"),
0x00000002: ('IN_MODIFY',"File was modified"),
0x00000004: ('IN_ATTRIB',"Metadata changed"),
0x00000008: ('IN_CLOSE_WRITE',"Writtable file was closed"),
0x00000010: ('IN_CLOSE_NOWRITE',"Unwrittable file closed"),
0x00000020: ('IN_OPEN',	"File was opened"),
0x00000040: ('IN_MOVED_FROM',"File was moved from X"),
0x00000080: ('IN_MOVED_TO',	"File was moved to Y"),
0x00000100: ('IN_CREATE',"Subfile was created"),
0x00000200: ('IN_DELETE',"Subfile was deleted"),
0x00000400: ('IN_DELETE_SELF',"Self was deleted"),
0x00002000: ('IN_UNMOUNT', "Backing fs was unmounted"),
0x00004000: ('IN_Q_OVERFLOW', "Event queued overflowed"),
0x00008000: ('IN_IGNORED', "File was ignored"),
0x00000018: ('IN_CLOSE', "close"),
0x000000c0: ('IN_MOVE',	"moves"),
0x40000000: ('IN_ISDIR', "event occurred against dir"),
0x80000000: ('IN_ONESHOT', "only send event once")}
# API odpala pętlę zbierającą komunikaty w tle w osobnym wątku/procesie (do wyboru?) za pomocą epoll, komunikaty inotify wrzuca do kolejki, z której użytkownik może pobierać wyniki. 

inotify_fd = -1
libc = 0
inotify_wd_l = {}
process_loop = 0
process = -1
notif_count = 0
ep = select.epoll()

def init():
    global inotify_fd, libc, ep
    libc = ctypes.cdll.LoadLibrary('libc.so.6')
    libc.inotify_init.argtypes = []
    libc.inotify_init.restype = ctypes.c_int
    libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p,
    ctypes.c_uint32]
    libc.inotify_add_watch.restype = ctypes.c_int
    libc.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]
    libc.inotify_rm_watch.restype = ctypes.c_int

    inotify_fd = libc.inotify_init()
    ep.register(inotify_fd, select.EPOLLIN)
    


def add_files_to_watch(*files):
    for f in files:
        inotify_wd_l[libc.inotify_add_watch(inotify_fd, f.encode('utf-8'), 0xfff)] = (f, 0x400)


def get_watched_list():
    return inotify_wd_l


def remove_files_from_watched(*files):
    to_remove = [k for k in inotify_wd_l if inotify_wd_l[k][0] in files]
    for f in to_remove:
        libc.inotify_rm_watch(inotify_fd, f)


def start_watching(queue):
    global process_loop
    #resq = Queue()
    process_loop = threading.Thread(target=process_watching, args=[queue])
    process_loop.start()


def process_watching(q):
    global process, notif_count, ep
    buf = ctypes.create_string_buffer(20)
    process = 1
    while process == 1:
        event = ep.poll(1)
        if event:
            size = libc.read(inotify_fd, buf, 16)
            wd, mask, cookie, ln = struct.unpack('iIII', buf[:16])
            name = libc.read(inotify_fd, buf, ln)
            q.put({wd: ((mask, cookie, ln, name), inotify_wd_l[wd], mask_dict[mask])})
            notif_count += 1
            #time.sleep(1)

def stop_watching():
    global process
    process = 0
