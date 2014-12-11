import requests
import hashlib
import bs4

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from multiprocessing import Queue, Process


def crawl(url, user, password, N):
    #result = requests.post({'uname':'foo', 'password': 'pass'})
    result = requests.post(url+'/login', data={'uname':'foo', 'password': 'bar'}, allow_redirects=False)
    resp2 = requests.get(url+'/220526', cookies=result.cookies)
    bs = bs4.BeautifulSoup(resp2.text)
    p = ThreadPool(N)


def process(q_in, q_out):
    
