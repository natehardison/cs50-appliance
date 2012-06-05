#!/usr/bin/python

import os
import pexpect
import sys

USERNAME = "jharvard"
PASSWORD = "crimson"
IP_ADDR = "172.16.79.129"

def scp(src, dst, debug=False):
    src = os.path.expanduser(src)
    # Don't expand dst because '~' means something different on the appliance
    child = pexpect.spawn("scp -r %s %s@%s:%s" % (src, USERNAME, IP_ADDR, dst))
    if debug:
        child.logfile = sys.stdout
    child.expect_exact("%s@%s's password:" % (USERNAME, IP_ADDR))
    child.sendline(PASSWORD)
    child.expect(pexpect.EOF)

def main():
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

    debug = (len(sys.argv) == 2 and sys.argv[1] == "-d")

    sys.stdout.write("Copying over .ssh directory...")
    sys.stdout.flush()
    scp("~/.ssh", "~", debug)
    sys.stdout.write("done.\n")

    sys.stdout.write("Copying setup script to appliance...")
    sys.stdout.flush()
    scp("_setup.sh", "~/setup.sh", debug)
    sys.stdout.write("done.\n")

    sys.stdout.write("Executing setup script on appliance...")
    sys.stdout.flush()
    ssh = pexpect.spawn("ssh %s@%s" % (USERNAME, IP_ADDR))
    if debug:
        ssh.logfile = sys.stdout
    ssh.expect_exact("%s@%s's password:" % (USERNAME, IP_ADDR))
    ssh.sendline(PASSWORD)
    ssh.expect_exact("jharvard@appliance (~): ")
    ssh.sendline("chmod +x setup.sh ; ./setup.sh ; rm -f ./setup.sh ; exit")
    ssh.expect(pexpect.EOF)
    sys.stdout.write("done.\n")

    os.chdir(original_dir)


if __name__ == "__main__":
    main()