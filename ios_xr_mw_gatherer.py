__author__     = "Sam Milstead"
__copyright__  = "Copyright 2021 (C) Cisco TAC"
__credits__    = "Sam Milstead"
__version__    = "2.0.0"
__maintainer__ = "Sam Milstead"
__email__      = "smilstea@cisco.com"
__status__     = "alpha"

global pexpect, pxssh
import pexpect
from pexpect import pxssh
global os
import os
import sys
import getpass
import re

def task():
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    key = 1
    is_error = False
    ssh = False
    file = ''
    ipv4_addr = ''
    username = ''
    for index, arg in enumerate(sys.argv):
        if arg in ['--file'] and len(sys.argv) > index + 1:
            file = str(sys.argv[index + 1])
            del sys.argv[index]
            del sys.argv[index]
            break
    for index, arg in enumerate(sys.argv):
        if arg in ['--ipv4addr', '-i'] and len(sys.argv) > index + 1:
            ipv4_addr = str(sys.argv[index + 1])
            del sys.argv[index]
            del sys.argv[index]
            break
    for index, arg in enumerate(sys.argv):
        if arg in ['--username', '-u'] and len(sys.argv) > index + 1:
            username = str(sys.argv[index + 1])
            del sys.argv[index]
            del sys.argv[index]
            break
    for index, arg in enumerate(sys.argv):
        if arg in ['--ssh', '-s']:
            ssh = True
            del sys.argv[index]
            break
    for index, arg in enumerate(sys.argv):
        if arg in ['--help', '-h']:
            break
    if len(sys.argv) > 1:
        is_error = True
    else:
        for arg in sys.argv:
            if arg.startswith('-'):
                is_error = True

    if is_error:
        print(str(sys.argv))
        print("Usage: python {" + sys.argv[0] + "} [--file <filename>][--ipv4addr <ipv4 address>][--username <username>](--ssh)")
        return
    else:
        if file:
            filename = file
            print("Filename: " + filename)
        elif not file:
            print("Please use --file and select a filename")
            return
        if not username:
            print("Please use --username and enter a username")
            return
        if not ipv4_addr:
            print("Please use --ipv4addr and enter the routers ipv4 address")
            return
    if ipv4_addr and username:
        if os.path.isfile(filename):
            print("Filename exists, please choose a non-existing filename")
            return
        outfile = open(filename, "a+")
        commands = ['show platform', 'show install active summary', 'show interface description', 'show ipv6 interface brief', 'show memory summary loc all', 'show filesystem loc all',
                    'show route summary', 'show route vrf all summary', 'show redundancy', 'show bgp all all summary', 'show bgp vrf all ipv4 unicast summary',
                    'show bgp vrf all ipv4 flowspec summary', 'show bgp vrf all ipv4 labeled-unicast summary', 'show bgp vrf all ipv4 multicast summary', 'show bgp vrf all ipv4 mvpn summary',
                    'show bgp vrf all ipv6 unicast summary', 'show bgp vrf all ipv6 flowspec summary', 'show bgp vrf all ipv6 multicast summary', 'show bgp vrf all ipv6 mvpn summary',
                    'show l2vpn xconnect', 'show l2vpn bridge detail', 'show nv satellite status', 'show ospf neighbor', 'show ospf vrf all neighbor', 'show ospfv3 neighbor', 'show ospfv3 vrf all neighbor',
                    'show isis neighbor', 'show mpls ldp neighbor brief', 'show mpls traffic-eng tunnels p2p', 'show mpls traffic-eng tunnels p2mp', 'show bfd session', 'show dhcp ipv4 proxy binding summary',
                    'show dhcp ipv4 server binding summary', 'show dhcp ipv6 proxy binding summary', 'show dhcp ipv6 server binding summary', 'show ipsla statistics']
        crs_commands = ['admin show controller fabric plane all detail', 'admin show controller fabric link health']
        asr9k_commands = ['show subscriber session all summary', 'show pfm loc all']
        ncs5500_commands = ['show controllers npu resources all location all', 'show controllers fia diagshell 0 "diag alloc all" location all']
        ncs6000_commands = ['admin show controller fabric plane all detail', 'admin show controller fabric link port s1 tx state down', 'admin show controller fabric link port s1 tx state mismatch',
                            'admin show controller fabric link port s1 rx state down', 'admin show controller fabric link port s1 rx state mismatch', 'admin show controller fabric link port fia tx state down',
                            'admin show controller fabric link port fia tx state mismatch', 'admin show controller fabric link port fia rx state down', 'admin show controller fabric link port fia rx state mismatch',
                            'admin show controller fabric link port s2 tx state down', 'admin show controller fabric link port s2 tx state mismatch', 'admin show controller fabric link port s2 rx state down',
                            'admin show controller fabric link port s2 rx state mismatch', 'admin show controller fabric link port s3 tx state down', 'admin show controller fabric link port s3 tx state mismatch',
                            'admin show controller fabric link port s3 rx state down', 'admin show controller fabric link port s3 rx state mismatch']
        print("Proceeding with login to router")
        password = getpass.getpass(prompt="Please enter your password:")
        #######
        # SSH #
        #######
        if ssh:
            try:
                sshconnect(ipv4_addr, username, password, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands, ncs6000_commands)
            except Exception as e:
                print("SSH error " + str(e))
                return()
        ##########
        # Telnet #
        ##########
        else:
            try:
                print("Trying telnet")
                telnetconnect(ipv4_addr, username, password, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands, ncs6000_commands)
            except Exception as e:
                print("Telnet error " + str(e))
                return
    else:
        print("Field(s) are missing for logging into the router")
        return
def sshconnect(ipv4_addr, username, password, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands, ncs6000_commands):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2021 (C) Cisco TAC"
    ###__version__    = "2.0.0"
    ###__status__     = "alpha"
    #ssh login and actions
    s = pxssh.pxssh(options={
                    "StrictHostKeyChecking": "no",
                    "UserKnownHostsFile": "/dev/null"})
    print('Logging in, may take 30s before next output')
    hostname = ipv4_addr
    s.PROMPT='RP\S+#'
    s.login(hostname, username, password, login_timeout=20, auto_prompt_reset=False)
    s.prompt()
    s.sendline(b'show clock')
    s.prompt()
    s.sendline(b'term length 0')
    s.prompt()
    s.sendline(b'term width 0')
    s.prompt()
    s.sendline(b'show version')
    s.prompt()
    data = s.before
    data += s.after
    data = data.decode('ascii')
    outfile.write(data)
    if 'cisco ASR9K' in data:
        commands.extend(asr9k_commands)
    elif 'isco CRS' in data:
        commands.extend(crs_commands)
    elif 'cisco NCS-5500' in data:
        commands.extend(ncs5500_commands)
    elif 'cisco NCS-6000' in data:
        commands.extend(ncs6000_commands)
    commands_len = len(commands)
    i = 0
    for command in commands:
        i += 1
        s.sendline(command.encode('utf-8'))
        s.prompt()
        data = s.before
        data += s.after
        data = data.decode('ascii')
        outfile.write(data)
        print("Command " + str(i) + " of " + str(commands_len) + " complete")
    s.logout()
    outfile.close()
def telnetconnect(ipv4_addr, username, password, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands, ncs6000_commands):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2021 (C) Cisco TAC"
    ###__version__    = "2.0.0"
    ###__status__     = "alpha"
    #telnet login and actions
    connection = pexpect.spawn('telnet ' + ipv4_addr)
    connection.expect('Username:')
    connection.sendline(username)
    connection.expect('Password:')
    connection.sendline(password)
    connection.expect(r'RP\S+#')
    connection.sendline(b"term len 0")
    connection.expect(r'RP\S+#')
    connection.sendline(b"term width 0")
    connection.expect(r'RP\S+#')
    outfile.write("**********")
    connection.sendline(b"show version")
    connection.expect(r'RP\S+#')
    data = connection.before
    data += connection.after
    data = data.decode('ascii')
    if 'cisco ASR9K' in data:
        commands.extend(asr9k_commands)
    elif 'isco CRS' in data:
        commands.extend(crs_commands)
    elif 'cisco NCS-5500' in data:
        commands.extend(ncs5500_commands)
    elif 'cisco NCS-6000' in data:
        commands.extend(ncs6000_commands)
    outfile.write(data)
    commands_len = len(commands)
    i = 0
    for command in commands:
        i += 1
        connection.sendline(command.encode('utf-8'))
        connection.expect(r'RP\S+#')
        data = connection.before
        data += connection.after
        data = data.decode('ascii')
        outfile.write(data)
        print("Command " + str(i) + " of " + str(commands_len) + " complete")
    connection.close()
    outfile.close()
if __name__ == '__main__':
    task()