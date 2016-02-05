#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
from builtins import input

import datetime

DEVICE_LIST = []

def load_db():
    global DEVICE_LIST

    DEVICE_LIST = []

    import appdirs, os
    app_dir = appdirs.user_data_dir('transmission-manager')
    db_file = os.path.join(app_dir,"device_list")
    if os.path.exists( db_file ):
        with open(db_file, 'r') as df:
            db_lines = df.readlines()

        from device import Device
        for db_line in db_lines:
            d = Device()
            d.from_string(db_line)
            DEVICE_LIST.append(d)

    #return DEVICE_LIST

def save_db():
    global DEVICE_LIST

    import appdirs, os
    app_dir = appdirs.user_data_dir('transmission-manager')
    db_file = os.path.join(app_dir,"device_list")

    if not os.path.exists( app_dir ):
        os.makedirs(app_dir)

    with open(db_file, 'w') as df:
        for d in DEVICE_LIST:
            df.write(d.to_string()+'\n')

def active_device(mac, ip='0.0.0.0', name='', time_stamp = datetime.datetime.now()):
    global DEVICE_LIST

    load_db()

    #time_stamp = datetime.datetime.now()

    mac_list = []
    for d in DEVICE_LIST:
        mac_list.append(d._mac)

    if not mac in mac_list:
        #have not found this device previously
        if len(name) < 1:
            name = input('What is the name of this machine? ('+ip+', '+mac+') ')

        from device import Device

        unkn_d = Device(name, mac)

        unkn_d.add_ip(ip)
        unkn_d.add_ts(time_stamp)

        print("Adding new DEVICE to DB")
        DEVICE_LIST.append(unkn_d)

    else:
        # already part of the db - only add time stamp
        print("Updating existing DEVICE in DB")

        index = mac_list.index(mac)
        DEVICE_LIST[index].add_ip(ip)
        DEVICE_LIST[index].add_ts(time_stamp)

    save_db()

def record_peers(ip_peers):
    import communication
    mac_peers = communication.find_macs(ip_peers)

    from device import Device

    for ip_peer,mac_peer in zip(ip_peers,mac_peers):
        active_device(mac_peer,ip_peer)

def main():
    global DEVICE_LIST
    print("Initializing network knowledge to make life easier.")

    import communication
    local_ip = communication.find_local_ip()
    local_mac = communication.find_mac(local_ip)
    local_name = communication.host_name()

    active_device(local_mac,local_ip,local_name)

    #fixed_ips = input('Do you have fixed IPs assigned to certain machines? (Y/N) ')

    local_ip_peers = communication.find_peers(local_ip)

    record_peers(local_ip_peers)

if __name__ == '__main__':
    main()
