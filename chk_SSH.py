#!/usr/bin/env python

### Importing socket, argparse & sys modules
import socket
import sys
import argparse

parser = argparse.ArgumentParser()
arggroup = parser.add_mutually_exclusive_group(required=True)
arggroup.add_argument("-l", "--list", type=str, help="host list text file - hostlist.txt")
arggroup.add_argument("-s", "--server", type=str, help="hostname or IP address")
args = parser.parse_args()


def checkSSHOpen(host):
  try: 
    ### Check if host is in IP addr format
    chkIP = host[0].isdigit()
    if chkIP:
      #print('IP Address given')

      ### If IP addr is given, find & set hostname
      niceName = socket.gethostbyaddr(host)[0]
      serverIP = host
    else:
      #print('Hostname given')

      ### If hostname is given, find & set IP addr
      serverIP = socket.gethostbyname(host)
      niceName = host

    #print('IP Address = {}'.format(serverIP))
    #print('Host Name = {}'.format(niceName))

    ### Setup network socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ### Network socket connection timeout in seconds
    sock.settimeout(1.5)
    ### Test connection to port 22, using IP addr
    result = sock.connect_ex((serverIP, 22))
    if result == 0:
      ### If port is responding, print 'Open'
      print('{:30} : Open'.format(niceName))
    else:
      ### If port is not responsive, print 'Unresponsive'
      print('{:30} : Unresponsive'.format(niceName))
    ### Close sock connection
    sock.close()
    chkIP = None
  ### Capture Ctrl-C
  except KeyboardInterrupt:
    print('You pressed Ctrl-C')
    sys.exit()

  ### Print 'Unresolvable' & continue if hostname cannot be resolved
  except socket.gaierror:
    print('{:30} : Unresolvable'.format(host))

  ### Print 'IP unresponsive' & continue if IP is not responding
  except socket.error:
    print('{:30} : IP unresponsive'.format(host))

  return


print('\n{:30} : Status'.format('Servername'))
print('---------------------------------------')


### Get list of hostnames or IP addrs from text file
if args.list:
  hname = [line.strip('\n') for line in open(args.list)]
  for host in hname:
    checkSSHOpen(host)
else:
  checkSSHOpen(args.server)


print('\nCheck completed\n')
