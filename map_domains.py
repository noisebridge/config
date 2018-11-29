#!/usr/bin/env python

from __future__ import print_function

import json
import os
import re
import requests
import socket
import sys

# TODO: Figure out how to label each location
BASE_URL = "https://www.google.com/maps/dir/?api=1&origin=2169+Mission+St+San+Francisco,+CA&waypoints="

def generate_map_url(domains):
    '''
    Prints the IP and Lat/Long of each valid domain given, then
    returns a Google Maps map of each domain's IP's server location
    '''
    ## Domains => IPs
    ip2domain = {}
    ips = []
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
        except socket.gaierror:
            print('Domain did not resolve:', domain)
            continue
        # print('Domain DID resolve:', domain)
        ip2domain[ip] = domain
        ips.append(ip)

    ## IPs => Lat/Longs
    ip_info = []
    for ip in ips:
        content = requests.get('https://ipinfo.io/' + ip).content
        info = json.loads(content)
        if 'loc' in info:
            info['domain'] = ip2domain[ip]
            ip_info.append(info)
        else:
            print('IP', ip, 'had no location:', info)

    domain_padding = max([len(info['domain']) for info in ip_info])
    for info in ip_info:
        print('{domain:{padding}} => IP: {ip:15}  Lat/Long: {loc}'.format(
            padding=domain_padding, **info)
        )

    ## Lat/Longs => Google Maps map of lat/longs
    # TODO: Figure out how to label each location
    return BASE_URL + '|'.join([info['loc'] for info in ip_info])


def usage():
    basename = os.path.basename(sys.argv[0])
    print('Usage:')
    print('  $ ', basename, 'domain1 [ domain2 ... ]')
    print('Example:')
    print('  $ ', basename, 'm3.noisebridge.net m4.noisebridge.net m5.noisebridge.net m6.noisebridge.net',
          'pegasus.noisebridge.net noisebridge.info')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
    else:
        domains = sys.argv[1:]
        print('\n' + generate_map_url(domains))
