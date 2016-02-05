#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

def main():
    #print("Running Transmission Manager.")

    import communication
    t_ip_port,local_peers = communication.find_transmission()

    if len(local_peers) < 1:
        local_ip = communication.find_local_ip()
        local_peers = communication.find_peers(local_ip)

    # record what we have found - this part should actually be executed every 10 min or something like that
    # over time it will become interesting to see which IPs are frequently offline or online
    # TODO: this does not log the local host (ip,mac,..) right now !
    import knowledge
    knowledge.record_peers(local_peers)

    import decider
    decider.is_network_busy()


if __name__ == '__main__':
    main()
