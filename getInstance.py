#!/usr/bin/python3

import json, argparse, sys

def find_instance(number, clusterinfo, hostname=False, force=False):
    # Find the nth-numbered instance and print it
    instances = clusterinfo["instances"]
    thisinstance = clusterinfo["instanceInfo"]
    instances.append(thisinstance)
    instances = sorted(instances, key=lambda k: k['name'])
    try:
        requested = instances[number].get('name'), instances[number].get('adminAddr')
    except IndexError:
        print("No such instance: %s" % number)
    if force:
        print(requested[1]) if not hostname else print(requested[0])
        return
    else:
        if thisinstance.get('name') != requested[0]:
            print(requested[1]) if not hostname else print(requested[0])
            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help='false', description='Echo the Nth instance in the current cluster. If instances are 00, 02, 03; N = 1 will return the instance 02')
    parser.add_argument('-n', '--number', type=int, required=True, help='Get the nth instance')
    parser.add_argument('-f', '--force', action='store_true', help='Force to show the requested cluster\'s IP/hostname, even if I\'m such instance.')
    parser.add_argument('--hostname', action='store_true', help='Echo the hostname instead of the IP')
    args = parser.parse_args()
    try:
        with open("/etc/cluster.info") as f:
            clusterinfo = json.load(f)
    except FileNotFoundError:
        print("localhost")
        sys.exit(0)
    except:
        print("Error!")
        sys.exit(1)
    find_instance(args.number, clusterinfo, args.hostname, args.force)
    sys.exit(0)
