# -*- coding: utf-8 -*-
import requests
import hashlib

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool


def compare(url, ffile):
    full = requests.get(url)
    full = full.content
    #TODO

def parallel_get(url, N):
    response = requests.head(url)
    resp_len = int(response.headers['Content-Length'])
    # calculate request range:
    reqranges = get_request_ranges(resp_len, N)
    reqdata = [(url, x) for x in reqranges]
    p = ThreadPool(N)
    data = p.map(get_file_part, reqdata)
    data.sort(key=lambda x: x[0])
    return b''.join([b[1].content for b in data])


def get_request_ranges(length, N):
    reqrange = list(range(0,resp_len,resp_len//N))
    reqrange[-1] = resp_len
    tmp = [x+1 for x in reqrange[1:-1]]
    return [(0, reqrange[1])] + [(x,y) for x,y in zip(tmp, reqrange[2:])]


def get_file_part(args):
    url = args[0]
    request_range = args[1]
    return request_range, requests.get(url, headers = {"Range": "bytes={}-{}".format(*request_range)})
