from optparse import OptionParser
import atexit
import getopt
import json
import os
import pexpect
import sys
import subprocess
import tempfile
import time

# Escape codes for cursor movements.
# XXX: I'm not sure this is the best way to deal with this.
cursor_up = '\x1b[A'
cursor_down = '\x1b[B'
cursor_right = '\x1b[C'
cursor_left = '\x1b[D'

test_config = None
test_config_file = None
sentinel_file = None

def usage(argv):
    print "Usage:"
    print "    %s -f [JSON config file]" % argv[0]


# The following test:
#   (1) Boots the disk image

def main(argv):

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:")
    except getopt.GetoptError as err:
        sys.exit(2)

    global test_config
    global test_config_file

    for o, a in opts:
        if o == "-f":
            test_config_file = a
        else:
            assert False, "unhandled option"

    if test_config_file is None:
        usage(argv)
        sys.exit(1)

    config_file = open(test_config_file, "r")
    test_config = json.load(config_file)
    config_file.close()
    checkpreReqBhyve()

    while True:
        try:
            runVm()
        except:
            pass

def runVm():
    global test_config
    global test_config_file
    global sentinel_file

    cmd = "bhyvectl --destroy --vm=%s" % test_config['vm_name']
    print cmd
    ret = os.system(cmd)

    cmd = "bhyveload -m %s -d %s %s" % (test_config['ram'], test_config['disk_img'], test_config['vm_name'])
    print cmd
    child5 = pexpect.spawn(cmd)
    child5.logfile = sys.stdout
    #child5.expect (['Booting...'], 250000)
    child5.expect(pexpect.EOF)
    extra_disks = ""
    i = 1
    for d in test_config['disks']:
        if os.path.exists(d):
            extra_disks += " -s 31:%d,virtio-blk,%s" % (i, d)
            i=i+1

    macaddress = ""
    if test_config.has_key('mac'):
        macaddress = ",mac=%s" % test_config['mac']

    cmd = "bhyve -c 2 -m %s -AI -H -P -g 0 -s 0:0,hostbridge -s 1:0,lpc -s 2:0,virtio-net,%s%s -s 31:0,virtio-blk,%s %s -l com1,stdio %s" % (test_config['ram'], test_config['tap'], macaddress, test_config['disk_img'], extra_disks, test_config['vm_name'])
    print cmd
    child6 = pexpect.spawn(cmd)
    child6.logfile = sys.stdout
    c = child6.expect("bound to", 25000000)
    c = child6.expect("-- renewal in")
    test_config['ip'] = child6.before.strip()
    test_config['url'] = "http://%s" % test_config['ip']

    with open(test_config_file, 'w') as outfile:
        json.dump(test_config, outfile, indent=4)
        outfile.close()

    child6.expect("Starting nginx", 25000000)
    child6.expect("Starting cron")
    child6.expect(" PST ", 25000000)
    (handle, sentinel_file) = tempfile.mkstemp("test")

    test_config['sentinel_file'] = sentinel_file
    with open(test_config_file, 'w') as outfile:
        json.dump(test_config, outfile, indent=4)
        outfile.close()

    child6.interact()

def checkpreReqBhyve():
    # Check if Bhyve module is loaded, and if we ran the script as superuser.
    # If not, silently kill the application.
    # XXX: Maybe this should not be so silent?
    euid = os.geteuid()
    if euid != 0:
        raise EnvironmentError, "this script need to be run as root"
        sys.exit()
    ret = os.system("kldload -n vmm")
    if ret != 0:
        raise EnvironmentError, "missing vmm.ko"
        sys.exit()
    ret = os.system("kldload -n if_tap")
    if ret != 0:
        raise EnvironmentError, "missing if_tap.ko"
        sys.exit()

def cleanup():
    os.system("rm -f %s" % (sentinel_file))

if __name__ == "__main__":
    atexit.register(cleanup)
    main(sys.argv)
