#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import socket

def find_local_ip():
    # find our local area network address (may not work on some linux distros)
    local_ip = socket.gethostbyname(socket.gethostname())

    #print("HOST IP: " + str(local_ip))

    if local_ip.startswith('127.'):
        # may just return local host IP or may have multiple IPs (WiFi, ethernet, etc)
        # check how the machine connects to the internet to get proper IP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("google.com",80))
        local_ip = s.getsockname()[0]
        s.close()

    #print("LOCAL IP: " + str(local_ip))

    return local_ip

def check_local_peer_thread(ip, result, index):
    #TODO: might want to switch to subprocess.call
    import os
    result[index] = os.system("ping -q -o -c 1 -W 420 "+ip+" > /dev/null")

def check_local_peer(ip):
    #TODO: might want to switch to subprocess.call
    import os
    return os.system("ping -q -o -c 1 -W 420 "+ip+" > /dev/null")

def find_local_peers(ip, sub_ip_max=44):
    local_peers = []

    if ip.count('.') != 3:
        print("Invalid IP input:",ip)
        return local_peers

    main_ip = ip[:ip.rfind('.')]
    sub_ip = int(ip[ip.rfind('.')+1:])

    # Let's see which peers are actually active on the network (using PING)
    # maybe not the best solution, but until we find a better solution, this will work

    # NOTE: this will NOT find all assigned IPs from your DHCP
    # this will only find active devices on your network
    # for example, if your (i)Phone is on the network, but is currently not in use, it will not respond to PING
    # however, if you are using it, it should actually respond ... technically, this is exactly what we want
    # we only want to find actively used peers, not the inactive devices on the network

    sub_ip_range = [i+1 for i in range(sub_ip_max) if (i+1)!=sub_ip]
    check_lp_results = [None]*len(sub_ip_range)

    ## zero parallelism Version
    '''
    for sip in sub_ip_range:
        ret = check_local_peer(test_ip)
        if ret == 0:
            local_peers.append(main_ip+'.'+str(sip))
    '''

    ## THREADING version
    '''
    import threading

    check_lp_threads = []

    for i,sip in enumerate(sub_ip_range):
        test_ip = main_ip+'.'+str(sip)
        t = threading.Thread(target=check_local_peer_thread, args=(test_ip,check_lp_results,i))
        t.start()
        check_lp_threads.append(t)

    for i,t in enumerate(check_lp_threads):
        t.join()
        if check_lp_results[i] == 0:
            local_peers.append(main_ip+'.'+str(sub_ip_range[i]))
    '''

    ## MULTIPROCESSING Version -> fastest !

    import multiprocessing
    pool = multiprocessing.Pool(sub_ip_max) #technically you may want a lower pool size, but ping uses so little resources that all of these can be processed at the same time

    check_lp_results = pool.map(check_local_peer, [main_ip+'.'+str(sip) for sip in sub_ip_range])

    for i,r in enumerate(check_lp_results):
        if r == 0:
            local_peers.append(main_ip+'.'+str(sub_ip_range[i]))

    #print(local_peers)

    return local_peers

def open_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = s.connect_ex((ip,port))
    s.close()

    return (r == 0)

def find_transmission(port=9091):
    '''
    Looking for local IP's that have port 9091 open - likely serving transmission on there
    '''

    # inspired by:
    # http://stackoverflow.com/questions/19196105/python-how-to-check-if-a-network-port-is-open-on-linux

    if open_port('127.0.0.1',port):
       print("Port",str(port),"is open on localhost")
       return '127.0.0.1:'+str(port)

    local_ip = find_local_ip()

    local_peers = find_local_peers(local_ip)

    for local_peer in local_peers:
        if open_port(local_peer,port):
            print("Port",str(port),"is open on",local_peer)
            return local_peer+str(port)
        else:
            print("Port",str(port),"is closed on",local_peer)

    # assuming all other relevant machines are on this same network
    # one of those may be hosting transmission

    # couldn't find any active, valid connection to transmission

    return '0.0.0.0:'+str(port)
