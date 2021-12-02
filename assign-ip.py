#!/usr/bin/python3

import os
import sys
import requests
import json
base_url = os.environ['zt_controllerURL']
network_id = os.environ['zt_networkID']
api_base = '{0}/controller/network/{1}/member'.format(base_url,network_id)


def usage():
    print('{0} [Floating IP] [Node ID]'.format(sys.argv[0]))
    print('\nYour Zerotier API token must be in the "zt_token"'
          ' environmental variable.')
    print('\nYour Zerotier API URL must be in the "zt_controllerURL"'
          ' environmental variable.')
    print('\nYour Zerotier Network ID must be in the "network_id"'
          ' environmental variable.')


def main(floating_ip, droplet_id):
    headers = {'X-ZT1-AUTH': '{0}'.format(os.environ['zt_token']),
               'Content-type': 'application/json'}
    url = api_base
    r = requests.get(url, headers=headers)
    resp = r.json()
    for x in resp:
     url = api_base + "/{0}".format(x)
     r = requests.get(url, headers=headers)
     respx = r.json()
#     print(json.dumps(respx))
     if(floating_ip in respx['ipAssignments']):
       iparray = respx['ipAssignments']
       iparray.remove(floating_ip)
       iparray =  {'ipAssignments':iparray}
       r = requests.post(url, headers=headers,  data=json.dumps(iparray))
       print('floating ip removed from {0}'.format(x))
       break



#step 1: get current ip
    url = api_base + "/{0}".format(droplet_id)
#    r = requests.post(url, headers=headers,  data=json.dumps(payload))
    r = requests.get(url, headers=headers)

    resp = r.json()
    if 'ipAssignments' in resp:
       iparray = resp['ipAssignments']
#       iparray.remove(floating_ip)
       iparray.append(floating_ip)
       iparray =  {'ipAssignments':iparray}
       r = requests.post(url, headers=headers,  data=json.dumps(iparray))
       resp = r.json()
       print('Moving IP address: {0} done'.format(json.dumps(resp['ipAssignments'])))

if __name__ == "__main__":
    if 'zt_token' not in os.environ or 'zt_controllerURL' not in os.environ or 'zt_networkID' not in os.environ or not len(sys.argv) > 2:
        usage()
        sys.exit()
        
    main(sys.argv[1], sys.argv[2])

