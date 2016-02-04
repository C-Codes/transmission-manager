#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

def main():
    print("Starting Transmission Manager.")

    import communication
    t_ip_port = communication.find_transmission()



if __name__ == '__main__':
    main()
