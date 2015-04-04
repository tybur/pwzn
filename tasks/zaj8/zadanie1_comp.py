import datetime
import random

def test_algo(func, N):
    startt = datetime.datetime.now()
    for i in range(N):
        func(gendata(100), 0, 99)
    return datetime.datetime.now()-startt


def gendata(N):
    return [int(random.random()*100) for x in range(N)]


def test2(func, N):
    func(gendata(N), 0, N-1)
