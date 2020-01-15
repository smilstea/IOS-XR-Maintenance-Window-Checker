__copyright__ = "Copyright (c) 2018 Cisco Systems. All rights reserved."
global paramiko, telnetlib
import paramiko, telnetlib
global os, time
import os, time
import sys
import getpass
import re


def task():
    key = 1
    is_error = False
    ssh = False
    pre = ''
    post = ''
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
    if len(sys.argv) > 1:
        is_error = True
    else:
        for arg in sys.argv:
            if arg.startswith('-'):
                is_error = True

    if is_error:
		print(str(sys.argv))
		print("Usage: python {sys.argv[0]} [--file <filename>][--ipv4addr <ipv4 address>][--username <username>]{--ssh}")
		return
    else:
		if file:
			filename = file
			print("Filename: " + filename)
		elif not filet:
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
		#######
        # SSH #
        #######
		commands = ['show install active summary', 'show interface description', 'show ipv6 interface brief', 'show memory summary loc all', 'show filesystem loc all',
					'show route summary', 'show route vrf all summary', 'show redundancy', 'show bgp all all summary', 'show l2vpn xconnect',
					'show l2vpn bridge detail', 'show nv satellite status', 'show ospf neighbor', 'show ospf vrf all neighbor', 'show isis neighbor',
					'show mpls ldp neighbor brief', 'show mpls traffic-eng tunnels', 'show bfd session']
		crs_commands = ['admin show controller fabric plane all detail']
		asr9k_commands = ['show pfm loc all']
		ncs5500_commands = ['show controllers npu resources all location all', 'show controllers fia diagshell 0 "diag alloc all" location all']
		print("Proceeding with login to router")
		password = getpass.getpass(prompt="Please enter your password:")
		if ssh:
			try:
				port = 22
				sshconnect(ipv4_addr, username, password, port, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands)
			except TypeError:
				return()
        ##########
        # Telnet #
        ##########
		else:
			try:
				port = 23
				print("Trying telnet")
				telnetconnect(ipv4_addr, username, password, port, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands)
			except Exception as e:
				print("Telnet error " + str(e))
				return
    else:
		print("Field(s) are missing for logging into the router")
		return
def sshconnect(ipv4_addr, username, password, port, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands):
    """
    SSH connection to router
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
		client.connect(ipv4_addr, port, username, password, banner_timeout=10)
		global remote_conn
		remote_conn = client.invoke_shell()
		regex_list = re.compile('RP\S+#')
		data = ""
		data = remote_conn.recv("#")
		data += remote_conn.recv(" ")
		if len(data) == 0:
			print("*** Connection terminated\r")
			sys.exit(3)
		match = regex_list.search(data)
		if match:
			prompt = match.group(0)
		else:
			print("Unable to get prompt")
			raise
		remote_conn.send("term len 0\n")
		remote_conn.recv(prompt)
		remote_conn.send("term width 0\n")
		remote_conn.recv(prompt)
        #########################################################
        # SSH: XR connection and config terminal error handling #
        #########################################################
		remote_conn.send("show platform\n")
		time.sleep(1)
		platform = ''
		try:
			data = remote_conn.recv(4096)
			platform += data
			if prompt in data:
				outfile.write(data)
				raise
			outfile.write(data)
			while data:
				data = remote_conn.recv(4096)
				platform += data
				outfile.write(data)
				if prompt in data:
					raise
		except:
			pass
		if 'A9K' in platform or 'A99' in platform:
			commands.extend(asr9k_commands)
		elif 'MSC' in platform or 'LSP' in platform or 'FP' in platform:
			commands.extend(crs_commands)
		elif 'NC55' in platform:
			commands.extend(ncs5500_commands)
		commands_len = len(commands)
		i = 0
		for command in commands:
			time.sleep(1)
			i += 1
			remote_conn.send(command + "\n")
			time.sleep(1)
			try:
				data = remote_conn.recv(4096)
				if prompt in data:
					outfile.write(data)
					raise
				outfile.write(data)
				while data:
					data = remote_conn.recv(4096)
					outfile.write(data)
					if prompt in data:
						raise
			except:
				pass
			print("Command " + str(i) + " of " + str(commands_len) + " complete")
		client.close()
		outfile.close()
    except paramiko.AuthenticationException:
		print("Authentication exception")
		raise
    except paramiko.ssh_exception.NoValidConnectionsError:
		print("Multiple connection attemps made and none succeeded")
		raise
    except paramiko.SSHException:
		print("SSH exception raised by failures in SSH2 protocol negotiation or logic errors")
		raise
def telnetconnect(ipv4_addr, username, password, port, outfile, commands, crs_commands, asr9k_commands, ncs5500_commands):
    """
    Connect to a router via telnet
    """
    try:
		global tn
		global prompt
		tn = telnetlib.Telnet(ipv4_addr, int(port))
		prompt = tn.read_until(b"Username:")
		if "Username:" in prompt:
			tn.write(username.encode('ascii') +b"\n")
		else:
			print("Unable to get username prompt")
			raise
		prompt = tn.read_until(b"Password:")
		if "Password:" in prompt:
			tn.write(password.encode('ascii')+b"\n")
		else:
			print("Unable to get password prompt")
			raise
		regex_list = ['RP\S+#']
		idx, obj, response = tn.expect(regex_list, 10)
		try:
			prompt = obj.group(0)
		except Exception as e:
			print("failure to get prompt")
			raise
		tn.write("term len 0\n")
		tn.read_until(prompt, 5)
		tn.write("term width 0\n")
		tn.read_until(prompt, 5)
		outfile.write("**********")
		tn.write("show platform" + "\n")
		platform = tn.read_until(prompt,10)
		if 'A9K' in platform or 'A99' in platform:
			commands.extend(asr9k_commands)
		elif 'MSC' in platform or 'LSP' in platform or 'FP' in platform:
			commands.extend(crs_commands)
		elif 'NC55' in platform:
			commands.extend(ncs5500_commands)
		outfile.write(platform)
		commands_len = len(commands)
		i = 0
		for command in commands:
			i += 1
			outfile.write("**********")
			tn.write(command + "\n")
			outfile.write(tn.read_until(prompt, 60))
			print("Command " + str(i) + " of " + str(commands_len) + " complete")
		tn.close()
		outfile.close()
    except IOError as e:
		print("Exception: " + str(e))
		raise
    except EOFError as e:
		print("Exception: " + str(e))
		raise
if __name__ == '__main__':
    task()