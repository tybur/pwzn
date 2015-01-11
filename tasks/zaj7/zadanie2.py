# -*- coding: utf-8 -*-
import requests
import hashlib
import bs4

from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from multiprocessing import Queue, JoinableQueue, Process


def crawl(url, user, password, N, depth=5):
    #result = requests.post({'uname':'foo', 'password': 'pass'})
    result = requests.post(url+'/login', data={'uname':'foo', 'password': 'bar'}, allow_redirects=False)
#    resp2 = requests.get(url+'/220526', cookies=result.cookies)
#    bs = bs4.BeautifulSoup(resp2.text)
    # queue initialization:
    q_todo, q_done, q_quits = Queue(), Queue(), Queue()
    ntodos = [-1]*N
    base_url = url
    for ld in get_all_links(base_url, url+'/220526', result.cookies, 1):
        q_todo.put(ld)
    processes = []
    for i in range(N):
        p = Process(target=process, args=(q_todo, q_done, q_quits, depth, result.cookies, i, base_url))
        p.start()
        processes.append(p)
    w = Process(target=watch_proc, args=(q_quits,N))
    w.start()
    w.join()

    results = []
    while not q_done.empty():
        results.append(q_done.get())

    for p in processes:
        p.terminate()
    #w.terminate()
    return results
    

def process(q_todo, q_done, q_quits, max_depth, cookies, proc_num, base_url):
    while True:
        try:
            link_data = q_todo.get(True, 5)
        except Exception as e:
            q_quits.put('quit')
            break
        print('process %d got %s' % (proc_num, str(link_data)))
        depth = link_data[1]        
        '''
        if depth > max_depth:
            q_quits.put('quit')
            #print('process %d breaks, depth = %d' % (proc_num, depth))
            break
        q_done.put(link_data)
        '''
        print('process %d puts data to q_done' % proc_num)
        #for ld in get_all_links(link_data[0], cookies, depth+1):
        q_done.put(link_data)
        if depth >= max_depth:
            continue
        else:
            print('process %d puts data to q_todo' % proc_num)
            for ld in get_all_links(base_url, link_data[0], cookies, depth+1):
                q_todo.put(ld)
    

def get_all_links(base_url, url, cookies, curr_depth):
    data = requests.get(url, cookies=cookies)
    bs = bs4.BeautifulSoup(data.text)
    return [[base_url.rstrip("/") + x['href'], curr_depth] for x in bs.findAll('a')]
    

def watch_proc(q_quits, N):
    nproc = N
    while nproc > 0:
        '''
        try: 
            q = q_quits.get(False)
            nproc -= 1
        except Exception as e:
            pass
        '''
        q = q_quits.get(True)
        nproc -= 1
