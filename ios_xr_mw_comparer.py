__author__     = "Sam Milstead"
__copyright__  = "Copyright 2020 (C) Cisco TAC"
__credits__    = "Sam Milstead"
__version__    = "1.0.0"
__maintainer__ = "Sam Milstead"
__email__      = "smilstea@cisco.com"
__status__     = "alpha"
import os
import sys
import re

def task():
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform all the parsing and then pass values to other functions
	#for making sense of the data and comparison tests
	#Finally output the data to the user and write to the output file
    is_error = False
    pre = ''
    post = ''
    compare = ''
    for index, arg in enumerate(sys.argv):
        if arg in ['--pre'] and len(sys.argv) > index + 1:
            pre = str(sys.argv[index + 1])
            del sys.argv[index]
            del sys.argv[index]
            break
    for index, arg in enumerate(sys.argv):
		if arg in ['--post'] and len(sys.argv) > index + 1:
			post = str(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
    for index, arg in enumerate(sys.argv):
		if arg in ['--compare', '-c'] and len(sys.argv) > index + 1:
			compare = str(sys.argv[index + 1])
			del sys.argv[index]
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
		print("Usage: python {sys.argv[0]} [--pre <filename>|--post <filename>][--compare <filename>]")
		return
    else:
		if pre:
			print("Pre filename: " + pre)
		if post:
			print("Post filename: " + post)
		if len(pre) == 0 or len(post) == 0:
			print("Please use --pre and --post and select a filename for each")
			return
		if not compare:
			print("Please use --compare and select a filename for the output")
			return
		if not os.path.isfile(pre):
			print("Pre filename does not exist, please choose an existing filename")
			return
		if not os.path.isfile(post):
			print("Pre filename does not exist, please choose an existing filename")
			return
		if os.path.isfile(compare):
			print("Compare filename exists, please choose a non-existing filename")
			return
		outfile = open(compare, "a+")
		pre_file = open(pre, "r")
		post_file = open(post, "r")
		commands = ['show install active summary', 'show interface description', 'show ipv6 interface brief', 'show memory summary loc all', 'show filesystem loc all',
					'show route summary', 'show route vrf all summary', 'show redundancy', 'show bgp all all summary', 'show l2vpn xconnect',
					'show l2vpn bridge detail', 'show nv satellite status', 'show ospf neighbor', 'show ospf vrf all neighbor', 'show isis neighbor',
					'show mpls ldp neighbor brief', 'show mpls traffic-eng tunnels', 'show bfd session']
		crs_commands = ['admin show controller fabric plane all detail']
		asr9k_commands = ['show pfm loc all']
		ncs5500_commands = ['show controllers npu resources all location all', 'show controllers fia diagshell 0 "diag alloc all" location all']
		####################
		#get platform      #
		####################
		platform = "None"
		pre_commands = {}
		post_commands = {}
		show_platform_found = False
		end_of_command = False
		command2 = str(commands[0])
		for line in pre_file:
			if 'show platform' in line:
				print("found show platform in " + str(pre))
				show_platform_found = True
				if 'show platform' not in pre_commands.keys():
						pre_commands['show platform' ] = ['show platform']
			if end_of_command == True:
				break
			elif show_platform_found == True:
				if command2 in line:
					end_of_command = True
				else:
					pre_commands['show platform'].append(line)
					if 'A9K' in line or 'A99' in line:
						platform = 'asr9k'
					elif 'MSC' in line or 'LSP' in line or 'FP' in line:
						platform = 'crs'
					elif 'NC55' in line:
						platform = 'ncs5500'
		else:
			pre_file.close()
		try:
			pre_file.close()
		except Exception as e:
			pass
		show_platform_found = False
		end_of_command = False
		for line in post_file:
			if 'show platform' in line:
				print("found show platform in " + str(post))
				show_platform_found = True
				if 'show platform' not in post_commands.keys():
						post_commands['show platform' ] = ['show platform']
			if end_of_command == True:
				pass
			elif show_platform_found == True:
				if command2 in line:
					end_of_command = True
				else:
					post_commands['show platform'].append(line)
		else:
			post_file.close()	
		if platform == 'asr9k':
			commands.extend(asr9k_commands)
		elif platform == 'crs':
			commands.extend(crs_commands)
		elif platform == 'ncs5500':
			commands.extend(ncs5500_commands)
		##################################################
		#put commands a dictionary and outputs in a list #
		##################################################
		pre_file = open(pre, "r")
		post_file = open(post, "r")
		command_length = len(commands)
		i = 0
		for line in pre_file:					
			try:
				if str(commands[i]) in line:
					print("found " + str(commands[i]) + " in " + str(pre))
					command = str(commands[i])
					if command not in pre_commands.keys():
						pre_commands[command] = [command]
					i += 1
				else:
					pre_commands[command].append(line)
			except IndexError:
				pre_commands[command].append(line)
			except Exception as e:
				pass
		else:
			pre_file.close()
			if i == len(commands):
				print("found all commands in " + str(pre))
			else:
				i += 1
				print("found " + str(i) + " commands of " + str(len(commands)+1) + " in " + str(pre))
		i = 0
		for line in post_file:					
			try:
				if str(commands[i]) in line:
					print("found " + str(commands[i]) + " in " + str(post))
					command = str(commands[i])
					if command not in post_commands.keys():
						post_commands[command] = [command]
					i += 1
				else:
					post_commands[command].append(line)
			except IndexError:
				post_commands[command].append(line)
			except Exception as e:
				pass
		else:
			post_file.close()
			if i == len(commands):
				print("found all commands in " + str(post))
			else:
				i += 1
				print("found " + str(i) + " commands of " + str(len(commands)+1) + " in " + str(post))
		##############################
		#Start performing comparisons#
		##############################
		##############################
		#show platform comparison    #
		##############################
		show_platform_pre_counters  = {}
		show_platform_post_counters = {}
		pre_totals = {}
		post_totals = {}
		platform_pre_list = []
		platform_post_list = []
		for value in pre_commands['show platform']:
			platform_pre_list.append(value)
		for value in post_commands['show platform']:
			platform_post_list.append(value)		
		try:
			show_platform_pre_counters = show_platform_compare(platform_pre_list, platform)
			show_platform_post_counters = show_platform_compare(platform_post_list, platform)
			pre_totals = show_platform_totals(show_platform_pre_counters)
			post_totals = show_platform_totals(show_platform_post_counters)
			show_platform_pre_counters.update(pre_totals)
			show_platform_post_counters.update(post_totals)
		except Exception as e:
			print("error " + str(e))
		ext_text = 'Card States:'
		show_platform_result = create_result('show platform', ext_text, show_platform_pre_counters, pre_totals, show_platform_post_counters)
		response = print_results(show_platform_result, show_platform_pre_counters, show_platform_post_counters, outfile)
		###########################################################################
		#Parse command by command and call on magic and change detection logic    #
		###########################################################################
		for command in commands:
			pre_list = []
			post_list = []
			pre_counters = {}
			post_counters = {}
			result = ''
			response = ''
			try:
				for value in pre_commands[command]:
					pre_list.append(value)
			except Exception as e:
				continue
			try:
				for value in post_commands[command]:
					post_list.append(value)
			except Exception as e:
				continue
			try:
				verbose = True
				if command == 'show install active summary':
					pre_counters = show_install_compare(pre_list)
					post_counters = show_install_compare(post_list)
					pre_totals = show_install_totals(pre_counters)
					post_totals = show_install_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nActive Packages:'
					result = create_result('show install active summary', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show interface description':
					pre_counters = show_interface_compare(pre_list)
					post_counters = show_interface_compare(post_list)
					pre_totals = show_interface_totals(pre_counters)
					post_totals = show_interface_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nInterface Summary:'
					result = create_result('show interface description', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show ipv6 interface brief':
					pre_counters = show_ipv6_interface_compare(pre_list)
					post_counters = show_ipv6_interface_compare(post_list)
					pre_totals = show_ipv6_interface_totals(pre_counters)
					post_totals = show_ipv6_interface_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nIPv6 Interface Summary:'
					result = create_result('show ipv6 interface brief', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show memory summary loc all':
					pre_counters = show_memory_summary_compare(pre_list)
					post_counters = show_memory_summary_compare(post_list)
					pre_totals = show_memory_summary_totals(pre_counters)
					post_totals = show_memory_summary_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nMemory Summary:'
					result = create_result('show memory summary loc all', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show filesystem loc all':
					pre_counters = show_filesystem_compare(pre_list)
					post_counters = show_filesystem_compare(post_list)
					pre_totals = show_filesystem_totals(pre_counters)
					post_totals = show_filesystem_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nFilesystem Summary:'
					result = create_result('show filesystem loc all', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show route summary':
					pre_counters = show_route_summary_compare(pre_list)
					post_counters = show_route_summary_compare(post_list)
					pre_totals = show_route_summary_totals(pre_counters)
					post_totals = show_route_summary_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nDefault VRF Summary:'
					result = create_result('show route summary', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show route vrf all summary':
					pre_counters = show_route_summary_compare(pre_list)
					post_counters = show_route_summary_compare(post_list)
					pre_totals = show_route_summary_totals(pre_counters)
					post_totals = show_route_summary_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nVRF Routing Summary:'
					result = create_result('show route vrf all summary', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show redundancy':
					pre_counters = show_redundancy_compare(pre_list)
					post_counters = show_redundancy_compare(post_list)
					pre_totals = show_redundancy_totals(pre_counters)
					post_totals = show_redundancy_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nRedundancy Summary:'
					result = create_result('show redundancy', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show bgp all all summary':
					pre_counters = show_bgp_all_all_summary_compare(pre_list)
					post_counters = show_bgp_all_all_summary_compare(post_list)
					pre_totals = show_bgp_all_all_summary_totals(pre_counters)
					post_totals = show_bgp_all_all_summary_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nBGP Summary:'
					result = create_result('show bgp all all summary', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show l2vpn xconnect':
					pre_counters = show_l2vpn_xconnect_compare(pre_list)
					post_counters = show_l2vpn_xconnect_compare(post_list)
					pre_totals = show_l2vpn_xconnect_totals(pre_counters)
					post_totals = show_l2vpn_xconnect_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nL2VPN Xconnect Summary:'
					result = create_result('show l2vpn xconnect', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show l2vpn bridge detail':
					pre_counters = show_l2vpn_bridge_compare(pre_list)
					post_counters = show_l2vpn_bridge_compare(post_list)
					pre_totals = show_l2vpn_bridge_totals(pre_counters)
					post_totals = show_l2vpn_bridge_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nL2VPN bridge Summary:'
					result = create_result('show l2vpn bridge detail', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show nv satellite status':
					pre_counters = show_nv_satellite_compare(pre_list)
					post_counters = show_nv_satellite_compare(post_list)
					pre_totals = show_nv_satellite_totals(pre_counters)
					post_totals = show_nv_satellite_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nNv Satellite Summary:'
					result = create_result('show nv satellite status', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show ospf neighbor':
					pre_counters = show_ospf_neighbor_compare(pre_list)
					post_counters = show_ospf_neighbor_compare(post_list)
					pre_totals = show_ospf_neighbor_totals(pre_counters)
					post_totals = show_ospf_neighbor_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nOSPF Neighbor Summary:'
					result = create_result('show ospf neighbor', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show ospf vrf all neighbor':
					pre_counters = show_ospf_neighbor_compare(pre_list)
					post_counters = show_ospf_neighbor_compare(post_list)
					pre_totals = show_ospf_neighbor_totals(pre_counters)
					post_totals = show_ospf_neighbor_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nOSPF VRF All Neighbor Summary:'
					result = create_result('show ospf vrf all neighbor', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show isis neighbor':
					pre_counters = show_isis_neighbor_compare(pre_list)
					post_counters = show_isis_neighbor_compare(post_list)
					pre_totals = show_isis_neighbor_totals(pre_counters)
					post_totals = show_isis_neighbor_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nISIS Neighbor Summary:'
					result = create_result('show isis neighbor', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show mpls ldp neighbor brief':
					pre_counters = show_mpls_ldp_neighbor_brief_compare(pre_list)
					post_counters = show_mpls_ldp_neighbor_brief_compare(post_list)
					pre_totals = show_mpls_ldp_neighbor_brief_totals(pre_counters)
					post_totals = show_mpls_ldp_neighbor_brief_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nMPLS LDP Neighbor Summary:'
					result = create_result('show mpls ldp neighbor brief', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show mpls traffic-eng tunnels':
					pre_counters = show_mpls_traffic_eng_tunnels_compare(pre_list, platform)
					post_counters = show_mpls_traffic_eng_tunnels_compare(post_list, platform)
					pre_totals = show_mpls_traffic_eng_tunnels_totals(pre_counters)
					post_totals = show_mpls_traffic_eng_tunnels_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nMPLS Traffic Engineering Summary:'
					result = create_result('show mpls traffic-eng tunnels', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show bfd session':
					pre_counters = show_bfd_session_compare(pre_list)
					post_counters = show_bfd_session_compare(post_list)
					pre_totals = show_bfd_session_totals(pre_counters)
					post_totals = show_bfd_session_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nBFD Summary:'
					result = create_result('show bfd session', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'admin show controller fabric plane all detail':
					pre_counters = admin_show_controller_fabric_plane_all_detail_compare(pre_list)
					post_counters = admin_show_controller_fabric_plane_all_detail_compare(post_list)
					pre_totals = admin_show_controller_fabric_plane_all_detail_totals(pre_counters)
					post_totals = admin_show_controller_fabric_plane_all_detail_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nCRS Fabric Summary:'
					result = create_result('admin show controller fabric plane all detail', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show pfm loc all':
					pre_counters = show_pfm_loc_all_compare(pre_list)
					post_counters = show_pfm_loc_all_compare(post_list)
					pre_totals = show_pfm_loc_all_totals(pre_counters)
					post_totals = show_pfm_loc_all_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nPFM Alarm Summary:'
					result = create_result('show pfm loc all', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show controllers npu resources all location all':
					pre_counters = show_controllers_npu_resources_all_compare(pre_list)
					post_counters = show_controllers_npu_resources_all_compare(post_list)
					pre_totals = show_controllers_npu_resources_all_totals(pre_counters)
					post_totals = show_controllers_npu_resources_all_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nNPU Resource Summary:'
					result = create_result('show controllers npu resources all location all', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)
				elif command == 'show controllers fia diagshell 0 "diag alloc all" location all':
					pre_counters = show_controllers_fia_diag_alloc_all_compare(pre_list)
					post_counters = show_controllers_fia_diag_alloc_all_compare(post_list)
					pre_totals = show_controllers_fia_diag_alloc_all_totals(pre_counters)
					post_totals = show_controllers_fia_diag_alloc_all_totals(post_counters)
					pre_counters.update(pre_totals)
					post_counters.update(post_totals)
					ext_text = '\nNPU Allocation Resource Summary:'
					result = create_result('show controllers fia diagshell 0 "diag alloc all" location all', ext_text, pre_counters, pre_totals, post_counters)
					response = print_results(result, pre_counters, post_counters, outfile)	
			except Exception as e:
				print("Error during processing of " + str(command) + " " + str(e))
				pass
		outfile.close		
		print("End of script, results in: " + str(compare))
		return
####################
#Dictionary Magic  #
####################
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
		self.current_dict, self.past_dict = current_dict, past_dict
		self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
		self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
		return self.set_current - self.intersect 
    def removed(self):
		return self.set_past - self.intersect 
    def changed(self):
		return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
		return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
def create_result(command, ext_text, pre_dict, pre_totals, post_dict = None):
    """
    Create the result object for each command.
    input:
        command (string) the command
        pre_dict (dict) the dictionary dirived from the command taken pre-MW
        ext_ext (string) the external text for the result
        post_dict (dict) (optional) the dictionary dirived from the command taken post-MW
    """
    title = "'" + command + "' results:"
    if not post_dict:
        severity = 'Severity INFO\n'
    else:
		if pre_dict == post_dict:
			severity = 'Severity INFO\n'
			ext_text = "\nThe Pre and Post outputs match.\n" + ext_text +"\n"
			for key, value in pre_totals.items():
				ext_text += str(key) + "\n"
				ext_text += str(pre_totals[key]) + "\n"
		else:
			the_diffs = DictDiffer(post_dict, pre_dict)
			ext_text += '\nThe following items were added:\n'
			ext_text += get_changes(the_diffs.added(), post_dict)
			ext_text += '\nThe following items were deleted:\n'
			ext_text += get_changes(the_diffs.removed(), pre_dict)
			ext_text += "\nThe changed items were:\n"
			ext_text += get_changes(the_diffs.changed(), pre_dict, post_dict)
			# ext_text += get_changes("   after : ", the_diffs.changed(), post_dict)
			severity = 'Severity WARNING\n'
    my_result = [severity, title, ext_text]
    return my_result
def get_changes(the_diffs, my_set, my_set2 = None):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Here we need to see if we have a dictionary inside of a dictionary
	#or a flat dictionary and then check for diffs
    diff_info = ""
    if not the_diffs:
		diff_info += 'None\n'
    elif not my_set2:
		for entry in the_diffs:
			diff_info += "{}: ".format(entry)
			try:
				for key, value in my_set[entry].items():
					try:
						diff_info += "'{}: {}' ".format(key, value)
					except Exception as e:
						pass
			except Exception as e:
				diff_info += str(my_set[entry]) + " "
    else:
		for entry in the_diffs:
			diff_info += "\nBefore:\n {}: ".format(entry)
			try:
				for key, value in my_set[entry].items():
					value3 = my_set[entry][key]
					try:
						value2 = my_set2[entry][key]
						if value2 != value3:
							diff_info += "'{}: {}' ".format(key, value)
					except Exception as e:
						diff_info += "'{}: {}' ".format(key, value)
			except Exception as e:
				diff_info += str(my_set[entry]) + " "
			diff_info += "\nAfter:\n {}: ".format(entry)
			try:
				for key, value in my_set2[entry].items():
					value3 = my_set2[entry][key]
					try:
						value2=my_set[entry][key]
						if value2 != value3:
							diff_info += "'{}: {}' ".format(key, value)
					except Exception as e:
						diff_info += "'{}: {}' ".format(key, value)
			except Exception as e:
				diff_info += str(my_set2[entry]) + " "	
    return diff_info
def print_results(result, pre_counters, post_counters, outfile):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#print results to terminal and outfile
    print("\n**********")
    outfile.write("\n**********")
    for value in result:
		print(value)
		outfile.write(value)
    try:
		outfile.write("\nInitial Values for Pre Counters\n")
		for key, value in pre_counters.items():
			outfile.write(str(key) + "\n")
			outfile.write(str(pre_counters[key]) + "\n")
    except Exception as e:
		outfile.write(str(key) + "\n")
		outfile.write(str(pre_counters[key])+ "\n")	
    try:
		outfile.write("\nValues for Post Counters\n")
		for key, value in post_counters.items():
			outfile.write(str(key) + "\n")
			outfile.write(str(post_counters[key]) + "\n")
    except Exception as e:
		outfile.write(str(key) + "\n")
		outfile.write(str(post_counters[key])+ "\n")		
    return
####################
#PI Commands	   #
####################
def show_platform_compare(file, platform):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show platform
	#Each line being an item in a list
	#Determine Card state and return the pre and post results
    sh_plat = {}
    found_start = False
    for line in file:
		if '---------------' in line:
			found_start = True
			continue
		try:
			if found_start == True:
				line_list = re.split(r'\s{2,}', line)
				if len(line_list) >= 4:
					if platform == 'crs':
						sh_plat[line_list[0]] = {}
						sh_plat[line_list[0]]['type'] = line_list[1] + ' ' + line_list[2]
						sh_plat[line_list[0]]['State'] = line_list[3]
						sh_plat[line_list[0]]['config state'] = line_list[4]
					if platform == 'asr9k':
						sh_plat[line_list[0]] = {}
						sh_plat[line_list[0]]['type'] = line_list[1]
						sh_plat[line_list[0]]['State'] = line_list[2]
						sh_plat[line_list[0]]['config state'] = line_list[3]
					if platform == 'ncs5500':
						sh_plat[line_list[0]] = {}
						sh_plat[line_list[0]]['type'] = line_list[1]
						sh_plat[line_list[0]]['State'] = line_list[2]
						sh_plat[line_list[0]]['config state'] = line_list[3]
				elif len(line_list) == 3:
					if platform == 'ncs5500':
						sh_plat[line_list[0]] = {}
						sh_plat[line_list[0]]['type'] = line_list[1]
						sh_plat[line_list[0]]['State'] = line_list[2]
					elif platform == 'asr9k':
						sh_plat[line_list[0]] = {}
						sh_plat[line_list[0]]['type'] = line_list[1]
						sh_plat[line_list[0]]['State'] = line_list[2]
		except Exception as e:
			print("error " + str(e))
    return sh_plat
def show_platform_totals(sh_plat):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.0.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show platform
    #Each line being an item in a list
    #Determine totals
    counters = {'Total Cards': 0, 'XR RUN/OK/UP/OPERATIONAL': 0, 'UNPOWERED/POWERED_OFF': 0, 'IN-RESET': 0, 'SW_INACTIVE': 0, 'Other': 0}
    for key in sh_plat:
		counters['Total Cards'] += 1
		if sh_plat[key]['State'] == 'IOS XR RUN' or sh_plat[key]['State'] == 'OK' or sh_plat[key]['State'] == 'UP' or sh_plat[key]['State'] == 'OPERATIONAL':
			counters['XR RUN/OK/UP/OPERATIONAL'] += 1
		elif sh_plat[key]['State'] == 'UNPOWERED' or sh_plat[key]['State'] == 'POWERED_OFF':
			counters['UNPOWERED/POWERED_OFF'] += 1
		elif sh_plat[key]['State'] == 'IN-RESET':
			counters['IN-RESET'] += 1
		elif sh_plat[key]['State'] == 'SW_INACTIVE':
			counters['SW_INACTIVE'] += 1
		else:
			counters['Other'] += 1
    return counters
def show_install_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show install active summary
	#Each line being an item in a list
	#Determine if all the same packages are loaded
    pkg_num = 0
    found_start = False
    sh_cmd = {}
    for line in file:
		#logger.debug("show int line is: " + line)
		if 'Active Packages' in line:
			found_start = True
			continue
		if found_start:
			if len(line) < 3:
				break
			else:
				try:
					line_list = re.split(r'-', line)
					pkg_type = line_list[1]
					pkg_num += 1
					if line_list[1] == "px" or line_list[1] == "p":
						pkg_type = line_list[2]
					elif line_list[1] == "services":
						if line_list[2] != "px" or line_list[2] != "p":
							pkg_type = line_list[1] + "-" + line_list[2]
					elif pkg_type == "services" or pkg_type == "9000v":
						pkg_type = line_list[1] + "-" + line_list[2]
					sh_cmd[pkg_type] = {}
					sh_cmd[pkg_type]['name'] = line
				except Exception as e:
					print("error " + str(e))
    return sh_cmd
def show_install_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show install active summary
	#Each line being an item in a list
	#Determine total packages
    counters = {'Total Packages': 0}
    for key in sh_cmd_dict:
        counters['Total Packages'] += 1
    return counters
def show_interface_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show interface description
	#Each line being an item in a list
	#Determine if status for an interface has changed
    found_start = False
    sh_int = {}
    for line in file:
		try:
			if '---------------' in line:
				found_start = True
				continue
			if found_start:
				line_list = line.split()
				if len(line_list) >= 3:
					sh_int[line_list[0]] = {}
					sh_int[line_list[0]]['status'] = line_list[1]
					sh_int[line_list[0]]['protocol'] = line_list[2]
					try:
						sh_int[line_list[0]]['desc'] = ' '.join(line_list[3:])
					except Exception as e:
						sh_int[line_list[0]]['desc'] = ' '
		except Exception as e:
			pass
	#We get an error message for null keys so we need to handle those
	#"dictionary changed size during iteration"
    for key in list(sh_int):
		if not sh_int[key]: 
			sh_int.pop(key)
    return sh_int	
def show_interface_totals(sh_int):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show interface description
	#Each line being an item in a list
	#Determine totals
    int_status_cnt = {'Up/Up': 0, 'Up/Down': 0, 'Down/Down': 0, 'Admin Down': 0, 'Other': 0}
    for key in sh_int:
        if sh_int[key]['status'] == 'up' and sh_int[key]['protocol'] == 'up':
            int_status_cnt['Up/Up'] += 1
        elif sh_int[key]['status'] == 'up' and sh_int[key]['protocol'] == 'down':
            int_status_cnt['Up/Down'] += 1
        elif sh_int[key]['protocol'] == 'down':
            int_status_cnt['Down/Down'] += 1
        elif sh_int[key]['status'] == 'admin-down':
            int_status_cnt['Admin Down'] += 1
        else:
            int_status_cnt['Other'] += 1
    return int_status_cnt
def show_ipv6_interface_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show ipv6 interface brief
	#Each line being an item in a list
	#Determine if interface status has changed
    found_start = True
    sh_int = {}
    regex_match = re.compile('^(\S+)\s+\[(\S+)/(\S+)\]')
    for line in file:
		try:
			if found_start:
				line_list = line.split()
				if len(line_list) >= 2:
					match = regex_match.search(line)
					sh_int[match.group(1)] = {}
					sh_int[match.group(1)]['status'] = match.group(2)
					sh_int[match.group(1)]['protocol'] = match.group(3)
		except Exception as e:
			pass
    return sh_int
def show_ipv6_interface_totals(sh_int):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show ipv6 interface brief
	#Each line being an item in a list
	#Determine totals
    int_status_cnt = {'Up/Up': 0, 'Up/Down': 0, 'Down/Down': 0, 'Shutdown': 0, 'Other': 0}
    for key in sh_int:
        if sh_int[key]['status'] == 'Up' and sh_int[key]['protocol'] == 'Up':
            int_status_cnt['Up/Up'] += 1
        elif sh_int[key]['status'] == 'Up' and sh_int[key]['protocol'] == 'Down':
            int_status_cnt['Up/Down'] += 1
        elif sh_int[key]['protocol'] == 'Down':
            int_status_cnt['Down/Down'] += 1
        elif sh_int[key]['status'] == 'Shutdown':
            int_status_cnt['Shutdown'] += 1
        else:
            int_status_cnt['Other'] += 1
    return int_status_cnt
def show_memory_summary_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show memory summary
	#Each line being an item in a list
	#Determine if memory has changed
    sh_cmd = {}
    found_node = False
    for line in file:
		try:
			if len(line) != 0:
				line_list = re.split(r'\s{1,}', line)
			else:
				continue
			if 'node:' in line:
				found_node = True
				node = line_list[1]
				sh_cmd[node] = {}
				continue
			elif '-------------' in line:
				continue
			elif found_node and "Physical Memory" in line:
				sh_cmd[node]["Phy Memory"] = line_list[2]
			elif found_node and "Application Memory" in line:
				sh_cmd[node]["Appl Memory"] = line_list[4] + " " + line_list[5] + " " + line_list[6]
			elif found_node and "Image" in line:
				sh_cmd[node]["Image"] = line_list[2]
			elif found_node and "Reserved" in line:
				sh_cmd[node]["Reserved"] = line_list[2]
				sh_cmd[node]["IOMem"] = line_list[4]
				sh_cmd[node]["flashfsys"] = line_list[6]
			elif found_node and "Total shared window" in line:
				sh_cmd[node]["Total shared"] = line_list[4]
				found_node = False
		except Exception as e:
			print("error " + str(e))
    return sh_cmd
def show_memory_summary_totals(sh_cmd_dict):	
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show memory summary
	#Each line being an item in a list
	#Nothing of importance yet
    counters = {'Total Nodes': 0}
    for key in sh_cmd_dict:
        counters['Total Nodes'] += 1
    return counters
def show_filesystem_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show filesystem
	#Each line being an item in a list
	#Determine if disk space has changed
    sh_cmd = {}
    found_node = False
    for line in file:
		try:
			if len(line) != 0:
				line_list = re.split(r'\s{1,}', line)
			else:
				continue
			if 'node:' in line:
				found_node = True
				node = line_list[2]
				sh_cmd[node] = {}
				continue
			elif '-------------' in line:
				continue
			elif found_node and "lcdisk0:" in line:
				continue
			elif found_node and "qsm/disk0:" in line:
				continue
			elif found_node and "qsm/harddisk:" in line:
				continue
			elif found_node and "qsm/disk1:" in line:
				continue
			elif found_node and "qsm_/dumper_disk0:" in line:
				continue
			elif found_node and "qsm_/dumper_disk1:" in line:
				continue
			elif found_node and "qsm_/dumper_harddisk:" in line:
				continue
			elif found_node and "disk0:" in line:
				try:
					megabytes = int(line_list[2])*0.000001
					megabytes = int(megabytes)
					sh_cmd[node]["disk0: Free Space in MB"] = megabytes
				except Exception as e:
					if line_list[2] == 0:
						sh_cmd[node]["disk0: Free Space in MB"] = line_list[2]
					else:
						sh_cmd[node]["disk0: Free Space in Bytes"] = line_list[2]
			elif found_node and "disk1:" in line:
				try:
					megabytes = int(line_list[2])*0.000001
					megabytes = int(megabytes)
					sh_cmd[node]["disk1: Free Space in MB"] = megabytes
				except Exception as e:
					if line_list[2] == 0:
						sh_cmd[node]["disk1: Free Space in MB"] = line_list[2]
					else:
						sh_cmd[node]["disk1: Free Space in Bytes"] = line_list[2]
			elif found_node and " harddisk:" in line:
				try:
					megabytes = int(line_list[2])*0.000001
					megabytes = int(megabytes)
					sh_cmd[node]["harddisk: Free Space in MB"] = megabytes
				except Exception as e:
					if line_list[2] == 0:
						sh_cmd[node]["harddisk: Free Space in MB"] = line_list[2]
					else:
						sh_cmd[node]["harddisk: Free Space in Bytes"] = line_list[2]
			elif found_node and "bootflash:" in line:
				found_node = False
			elif found_node and "nvram:" in line:
				found_node = False
		except Exception as E:
			print("error " + str(e))
    return sh_cmd
def show_filesystem_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show filesystem
	#Each line being an item in a list
	#Determine total free space on all disks, need to improve this
    counters = {'Total Nodes': 0, 'Total Free Space in MB': 0}
    for key in sh_cmd_dict:
		counters['Total Nodes'] += 1
		for value in sh_cmd_dict[key]:
			if 'disk0: Free Space in MB' in value:
				counters['Total Free Space in MB'] +=  sh_cmd_dict[key][value]
			elif 'disk1: Free Space in MB' in value:
				counters['Total Free Space in MB'] +=  sh_cmd_dict[key][value]
			elif 'harddisk: Free Space in MB' in value:
				counters['Total Free Space in MB'] +=  sh_cmd_dict[key][value]
    return counters
def show_route_summary_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show route summary
	#Each line being an item in a list
	#Determine if number of routes has changed
    sh_cmd = {}
    found_vrf = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if found_vrf == False:
			if 'Route Source' in line:
				found_vrf = True
				vrf = line_list[1]
				sh_cmd[vrf] = {}
				continue
		elif 'VRF:' in line:
			found_vrf = True
			vrf = line_list[1]
			sh_cmd[vrf] = {}
			continue
		elif found_vrf and "connected" in line:
			sh_cmd[vrf]["Connected Routes"] = line_list[1]
		elif found_vrf and "local VRRP" in line:
			sh_cmd[vrf]["Local VRRP Routes"] = line_list[2]
		elif found_vrf and "local HSRP" in line:
			sh_cmd[vrf]["Local HSRP Routes"] = line_list[2]                                                  
		elif found_vrf and "local LSPV" in line:
			sh_cmd[vrf]["Local LSPV Routes"] = line_list[2] 
		elif found_vrf and "local SMIAP" in line:
			sh_cmd[vrf]["Local SMIAP Routes"] = line_list[2] 
		elif found_vrf and "local" in line:
			sh_cmd[vrf]["Local Routes"] = line_list[1]
		elif found_vrf and "static" in line:
			sh_cmd[vrf]["Static Routes"] = line_list[1]
		elif found_vrf and "application" in line:
			sh_cmd[vrf]["Application Routes"] = line_list[1]
		elif found_vrf and "subscriber" in line:
			sh_cmd[vrf]["Subscriber Routes"] = line_list[1]
		elif found_vrf and "isis" in line:
			sh_cmd[vrf]["isis " + line_list[1] + " Routes"] = line_list[2]
		elif found_vrf and "dagr" in line:
			sh_cmd[vrf]["Dagr Routes"] = line_list[1]
		elif found_vrf and "bgp" in line:
			sh_cmd[vrf]["BGP " + line_list[1] + " Routes"] = line_list[2]
		elif found_vrf and "eigrp" in line:
			sh_cmd[vrf]["EIGRP " + line_list[1] + " Routes"] = line_list[2]  
		elif found_vrf and "ospf" in line:
			sh_cmd[vrf]["OSPF " + line_list[1] + " Routes"] = line_list[2] 
		elif found_vrf and "Total" in line:
			sh_cmd[vrf]["Total Routes"] = line_list[1]
    return sh_cmd
def show_route_summary_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show route summary
	#Each line being an item in a list
	#Determine if number of routes has changed
    counters = {'Total VRFs': 0, 'Total Routes': 0}
    for key in sh_cmd_dict:
		counters['Total VRFs'] += 1
		mytotal = sh_cmd_dict[key]['Total Routes']
		counters['Total Routes'] += int(mytotal)
    return counters
def show_redundancy_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show redundancy
	#Each line being an item in a list
	#Determine if redundancy state has changed
    sh_cmd = {}
    found_group = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if "---------        ---------" in line:
			found_group = True
			continue
		elif "Process Group Details" in line:
			found_group = False
		elif found_group and "Not NSR-Ready" in line:
			sh_cmd[line_list[0]] = {}
			sh_cmd[line_list[0]]['status'] = "Not NSR-Ready"
		elif found_group and "Not Ready" in line:
			sh_cmd[line_list[0]] = {}
			sh_cmd[line_list[0]]['status'] = "Not Ready"
		elif found_group and "Ready" in line:
			sh_cmd[line_list[0]] = {}
			sh_cmd[line_list[0]]['status'] = "Ready"
    return sh_cmd
def show_redundancy_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show redundancy
	#Each line being an item in a list
	#Determine total process groups and states	
    counters = {'Total Groups': 0, 'Process Groups in Not Ready State': 0, 'Process Groups in Not NSR-Ready State': 0, 'Process Groups in Ready State': 0}
    for key in sh_cmd_dict:
		counters['Total Groups'] += 1
		if sh_cmd_dict[key]['status'] == 'Not NSR-Ready':
			counters['Process Groups in Not NSR-Ready State'] += 1
		elif sh_cmd_dict[key]['status'] == 'Not Ready':
			counters['Process Groups in Not Ready State'] += 1
		elif sh_cmd_dict[key]['status'] == 'Ready':
			counters['Process Groups in Ready State'] += 1
    return counters
def show_bgp_all_all_summary_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show bgp all all summary
	#Each line being an item in a list
	#Determine if neighbor state or prefixes have changed
    sh_cmd = {}
    found_AF = False
    regex_string = re.compile('\d+\.\d+\.\d+\.\d+')
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if 'Address Family:' in line:
			found_AF = True
			AF = line_list[0] + ' ' + line_list[1]
			if line_list[2]:
				AF += (' ' + line_list[2])
			if line_list[3]:
				AF += (' ' + line_list[3])
			sh_cmd[AF] = {}
			continue
		elif '-------------' in line:
			continue
		elif found_AF:
			found = regex_string.search(line_list[0])
			if found:
				sh_cmd[AF][line_list[0]] = 'Prefix Received: ' + line_list[9]
    return sh_cmd
def show_bgp_all_all_summary_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show bgp all all summary
	#Each line being an item in a list
	#Determine total AFs and routes
    counters = {'Total AFs': 0, 'Total Routes': 0}
    regex = re.compile('(\d+)')
    for key in sh_cmd_dict:
		counters['Total AFs'] += 1
		for value in sh_cmd_dict[key]:
			mytotal = sh_cmd_dict[key][value]
			match = regex.search(mytotal)
			if match:
				mynewtotal = match.group(0)
				counters['Total Routes'] += int(mynewtotal)
    return counters
def show_l2vpn_xconnect_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show l2vpn xconnect
	#Each line being an item in a list
	#Determine if state has changed for xconnect
    sh_cmd = {}
    found_start = False
    list_test = ['UP', 'DN', 'AD', 'UR', 'SB', 'SR' 'PP']
    for line in file:
		if '------------------------' in line:
			found_start = True
			continue
		if found_start:
			line_list = line.split()
			if len(line_list) < 5:
				continue
			#there is some weird logging message being captured as well
			#going to add another check so that it won't be caught
			for item in list_test:
				if item in line_list[2]:
					sh_cmd[line_list[0] + ' ' + line_list[1]] = {}
					sh_cmd[line_list[0] + ' ' + line_list[1]]['Xconnect Status (Overall)'] = line_list[2] 
				if item in line_list[1]:
					sh_cmd['Unknown Xconnect Name, With Name: ' + line_list[0]] = {}
					sh_cmd['Unknown Xconnect Name, With Name: ' + line_list[0]]['Xconnect Status (Overall)'] = line_list[1]    
				if item in line_list[0]:
					#sh_cmd_post['Unknown Circuit Name, Line: ' + line] = {}
					#sh_cmd_post['Unknown Circuit Name, Line: ' + line]['Xconnect Status (Overall)'] = line_list[0]
					#This causes a duplicate to be made
					continue
    return sh_cmd
def show_l2vpn_xconnect_totals(sh_cmd):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show l2vpn xconnect
	#Each line being an item in a list
	#Determine xconnect totals	
    counters = {'Total Xconnects': 0, 'Total Xconnects in UP State': 0, 'Total Xconnects in DN State': 0, 'Total Xconnects in any other state': 0}
    for key in sh_cmd:
		counters['Total Xconnects'] += 1
    for key in sh_cmd:
		for value in sh_cmd[key]:
			mytotal = sh_cmd[key][value]
			if 'DN' in mytotal:
				counters['Total Xconnects in DN State'] += 1
				continue
			elif 'UP' in mytotal:
				counters['Total Xconnects in UP State'] += 1
				continue
			else:
				counters['Total Xconnects in any other state'] +=1
				continue
    return counters
def show_l2vpn_bridge_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show l2vpn xconnect
	#Each line being an item in a list
	#Determine if state has changed for bridge domain
    sh_cmd = {}
    found_BG = False
    regex_string = re.compile('ACs: (\d+) \((\d+) up\), VFIs: (\d+), PWs: (\d+) \((\d+) up\), PBBs: (\d+) \((\d+) up\), VNIs: (\d+) \((\d+) up\)')
    #There is an issue where *'s will sometimes appear at the beginning of the string, unknown why, this fixes it
    regex_string2 = re.compile('^\*\*\*\*\*\*\*\*\*\*')
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if 'Bridge group:' in line:
			found_BG = True
			BG = line_list[0] + " " + line_list[1]
			found = regex_string2.search(BG)
			if found:
				BG = BG[10:]
			if line_list[2]:
				BG += (' ' + line_list[2])
				BG = BG[:-1:]
			if line_list[3]:
				BG += (' ' + line_list[3])
			if line_list[4]:
				BG += (' ' + line_list[4])
				BG = BG[:-1:]
			sh_cmd[BG] = {}
			continue
		elif '-------------' in line:
			continue
		elif found_BG:
			try:
				found = regex_string.search(line)
				if found:
					sh_cmd[BG]['Total ACs'] = str(found.group(1))
					sh_cmd[BG]['ACs Up'] =  str(found.group(2))
					sh_cmd[BG]['Total VFIs'] =  str(found.group(3))
					sh_cmd[BG]['Total PWs'] =  str(found.group(4))
					sh_cmd[BG]['PWs Up'] =  str(found.group(5))
					sh_cmd[BG]['Total PBBs'] =  str(found.group(6))
					sh_cmd[BG]['PBBs Up'] =  str(found.group(7))
					sh_cmd[BG]['Total VNIs'] =  str(found.group(8))
					sh_cmd[BG]['VNIs Up'] =  str(found.group(9))
			except Exception as e:
				continue
    return sh_cmd
def show_l2vpn_bridge_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show l2vpn xconnect
	#Each line being an item in a list
	#Determine total circuits and states
    counters = {'Total Circuits': 0, 'ACs in Up State': 0, 'PWs in Up State': 0, 'VNIs in Up State': 0, 'P2MP PWs in Up State': 0}
    for key in sh_cmd_dict:
		for value in sh_cmd_dict[key]:
			if value == 'Total':
				counters['Total Circuits'] += int(sh_cmd_dict[key][value])
		if key == 'ACs':        
			for value in sh_cmd_dict[key]:
				if value == 'Up':
					counters['ACs in Up State'] +=  int(sh_cmd_dict[key][value])
		elif key == 'PWs':
			for value in sh_cmd_dict[key]:
				if value == 'Up':
					counters['PWs in Up State'] +=  int(sh_cmd_dict[key][value])
		elif key == 'P2MP':
			for value in sh_cmd_dict[key]:
				if value == 'Up':
					counters['P2MP PWs in Up State'] +=  int(sh_cmd_dict[key][value])       
		elif key == 'VNIs':
			for value in sh_cmd_dict[key]:
				if value == 'Up':
					counters['VNIs in Up State'] +=  int(sh_cmd_dict[key][value])
    return counters
def show_nv_satellite_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show nv satellite status
	#Each line being an item in a list
	#Determine if satellite status, icl, etc has changed
    sh_cmd = {}
    regex_string = re.compile('Satellite \d+')
    icl_string = re.compile('\S+')
    found_satellite = False
    found_icl = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		match = regex_string.search(line)
		if match:
			found_satellite = True
			found_icl = False
			satellite = line_list[1]
			sh_cmd[satellite] = {}
			continue
		elif '-------------' in line:
			continue
		elif found_satellite and 'Ethernet' in line:
			found_icl = True
			match = icl_string.search(line)
			icl = str(match.group(0))
		elif found_satellite and 'Gig' in line:
			found_icl = True
			match = icl_string.search(line)
			icl = str(match.group(0))
		elif found_satellite and 'Bundle' in line:
			found_icl = True
			match = icl_string.search(line)
			icl = str(match.group(0))
		elif found_satellite and 'Status:' in line:
			if found_icl == False:
				sh_cmd[satellite]['status'] = line
			else:
				icl_status = "icl " + icl
				found_icl == False
				sh_cmd[satellite][icl_status] = line
				found_satellite = False
    return sh_cmd
def show_nv_satellite_totals(sh_cmd):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show nv satellite status
	#Each line being an item in a list
	#Determine totals
    counters = {'Total Satellites': 0, 'Total Status Connected Satellites': 0, 'Total Status Not Connected Satellites': 0, 'Total Status Satellite Ready ICL': 0, 'Total ICL': 0, 'Total Status Not Ready ICL': 0}
    regex = re.compile('Satellite Ready')
    regex2 = re.compile('Connected')
    for key in sh_cmd:
		counters['Total Satellites'] += 1
    for key in sh_cmd:
		for value in sh_cmd[key]:
			if 'icl' in value:
				icl_status = sh_cmd[key][value]
				match = regex.search(icl_status)
				counters['Total ICL'] += 1
				if match:
					counters['Total Status Satellite Ready ICL'] += 1
				else:
					counters['Total Status Not Ready ICL'] += 1
			elif 'status' in value:
				status = sh_cmd[key][value]
				if 'Connected' in status:
					counters['Total Status Connected Satellites'] += 1
				else:
					counters['Total Status Not Connected Satellites'] += 1
    return(counters)
def show_ospf_neighbor_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show ospf neighbor
	#Each line being an item in a list
	#Determine if OSPF neighborship has changed
    sh_cmd = {}
    regex_string = re.compile('\d+\.\d+\.\d+\.\d+')
    found_ospf = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if 'Neighbors' in line:
			found_ospf = True
			if len(line_list) == 6:
				ospf = line_list[3] + ' '
				temp = line_list[4]
				temp = temp[:-1:]
				ospf = ospf + temp + ' ' + line_list[5]
			else:
				ospf = line_list[3]
			sh_cmd['OSPF ' + ospf] = {}
			continue
		elif found_ospf:
			found = regex_string.search(line_list[0])
			if found:
				if len(line_list) == 6:
					sh_cmd['OSPF ' + ospf]['Neighbor ' + line_list[0] + ' ' + line_list[5] + " In State: "] = line_list[2]
				elif len(line_list) == 7:
					sh_cmd['OSPF ' + ospf]['Neighbor ' + line_list[0] + ' ' + line_list[6] + " In State: "] = line_list[2]
    return sh_cmd
def show_ospf_neighbor_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show ospf neighbor
	#Each line being an item in a list
	#Determine totals for OSPF
    counters = {'Total OSPF Instances': 0, 'Total OSPF Neighbors': 0, 'Total Neighbors in FULL State': 0, 'Total Neighbors in Any Other State': 0}
    regex = re.compile('FULL')
    for key in sh_cmd_dict:
		counters['Total OSPF Instances'] += 1
		for value in sh_cmd_dict[key]:
			counters['Total OSPF Neighbors'] += 1
			dict_value = sh_cmd_dict[key][value]
			match = regex.search(dict_value)
			if match:
				counters['Total Neighbors in FULL State'] += 1
			else:
				counters['Total Neighbors in Any Other State'] += 1
    return counters
def show_isis_neighbor_compare(file):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show isis neighbor
	#Each line being an item in a list
	#Determine isis neighbor details
    sh_cmd = {}
    regex_string = re.compile('IS-IS \S+ neighbors:')
    regex_string2 = re.compile('\S+\s+\S+\S+\d+\s+\S+\s+\S+\s+\d+\s+\S+\s+\S+')
    found_isis = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		match = regex_string.search(line)
		if match:
			found_isis = True
			isis = line_list[1]
			sh_cmd['ISIS ' + isis] = {}
			continue
		elif 'System Id' in line:
			continue
		elif found_isis:
			found = regex_string2.search(line)
			if found:
				sh_cmd['ISIS ' + isis]['Neighbor ' + line_list[0] + ' ' + line_list[1] + " in State: "] = line_list[3]
    return sh_cmd
def show_isis_neighbor_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show isis neighbor
	#Each line being an item in a list
	#Determine isis neighbor totals
    counters = {'Total ISIS Instances': 0, 'Total ISIS Neighbors': 0, 'Total Neighbors in Up State': 0, 'Total Neighbors in Any Other State': 0}
    regex = re.compile('Up')
    for key in sh_cmd_dict:
		counters['Total ISIS Instances'] += 1
		for value in sh_cmd_dict[key]:
			counters['Total ISIS Neighbors'] += 1
			dict_value = sh_cmd_dict[key][value]
			match = regex.search(dict_value)
			if match:
				counters['Total Neighbors in Up State'] += 1
			else:
				counters['Total Neighbors in Any Other State'] += 1
    return counters
def show_mpls_ldp_neighbor_brief_compare(file):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show mpls ldp neighbor brief
	#Each line being an item in a list
	#Determine neighborships, labels, etc
    sh_cmd = {}
    found_group = False
    regex = re.compile('\d+\.\d+\.\d+\.\d+\:\d+')
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if "-----------------" in line:
			found_group = True
			continue
		elif found_group:
			match = regex.search(line_list[0])
			if match:
				#Len has to be 1 more than the actual number of fields, ASR9K has 10, CRS has 7
				if len(line_list) == 11:
					sh_cmd[line_list[0]] = {}
					sh_cmd[line_list[0]]['GR'] = line_list[1]
					sh_cmd[line_list[0]]['NSR'] = line_list[2]
					sh_cmd[line_list[0]]['Discovery IPv4'] = line_list[4]
					sh_cmd[line_list[0]]['Discovery IPv6'] = line_list[5]
					sh_cmd[line_list[0]]['Addresses IPv4'] = line_list[6]
					sh_cmd[line_list[0]]['Addresses IPv6'] = line_list[7]
					sh_cmd[line_list[0]]['Labels IPv4'] = line_list[8]
					sh_cmd[line_list[0]]['Labels IPv6'] = line_list[9]
				elif len(line_list) == 8:
					sh_cmd[line_list[0]] = {}
					sh_cmd[line_list[0]]['GR'] = line_list[1]
					sh_cmd[line_list[0]]['NSR'] = line_list[2]
					sh_cmd[line_list[0]]['Discovery'] = line_list[4]
					sh_cmd[line_list[0]]['Addresses'] = line_list[5]
					sh_cmd[line_list[0]]['Labels IPv4'] = line_list[6]
    return sh_cmd
def show_mpls_ldp_neighbor_brief_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show mpls ldp neighbor brief
	#Each line being an item in a list
	#Determine neighborship totals
    counters = {'Total Peers': 0, 'Total Discovery': 0, 'Total GR Neighbors': 0, 'Total NSR Neighbors': 0}
    for key in sh_cmd_dict:
		counters['Total Peers'] += 1
		if sh_cmd_dict[key]['GR'] == 'Y':
			counters['Total GR Neighbors'] += 1
		if sh_cmd_dict[key]['NSR'] == 'Y':
			counters['Total NSR Neighbors'] += 1
		#The code doesn't like if statements if the value doesn't exist
		try:
			if sh_cmd_dict[key]['Discovery IPv4']:
				dict_value = sh_cmd_dict[key]['Discovery IPv4']
				counters['Total Discovery'] += int(dict_value)
		except Exception as e:
			pass
		try:
			if sh_cmd_dict[key]['Discovery IPv6']:
				dict_value = sh_cmd_dict[key]['Discovery IPv6']
				counters['Total Discovery'] += int(dict_value)
		except Exception as e:
			pass
		try:
			if sh_cmd_dict[key]['Discovery']:
				dict_value = sh_cmd_dict[key]['Discovery']
				counters['Total Discovery'] += int(dict_value)
		except Exception as e:
			pass
    return counters
def show_mpls_traffic_eng_tunnels_compare(file, platform):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show mpls traffic-eng tunnels
	#Each line being an item in a list
	#Determine tunnel state
    sh_cmd = {}
    regex_string = re.compile('Signalled-Name:\s(\S+)')
    regex_string2 = re.compile('Admin:\s(\S+)\s+Oper:\s(\S+)')
    regex_string3 = re.compile('Destination:\s(\S+)')
    regex_string4 = re.compile('State:\s(\S+)')
    found_tunnel = False
    if platform == 'asr9k':
		for line in file:
			if len(line) != 0:
				line_list = re.split(r'\s{1,}', line)
			else:
				continue
			match = regex_string.search(line)
			if match:
				found_tunnel = True
				tunnel = str(match.group(1))
				sh_cmd['Tunnel ' + tunnel] = {}
				continue
			elif found_tunnel:
				found = regex_string2.search(line)
				if found:
					sh_cmd['Tunnel ' + tunnel]['Admin State'] = str(found.group(1))
					sh_cmd['Tunnel ' + tunnel]['Oper State'] = str(found.group(2))
				destination = regex_string3.search(line)
				if destination:
					destination_stripped = str(destination.group(1))
					sh_cmd['Tunnel ' + tunnel]['Destination ' + destination_stripped] = ''
				state = regex_string4.search(line)
				if state:
					sh_cmd['Tunnel ' + tunnel][destination_stripped] = str(state.group(1))
    elif platform == 'crs':
		for line in file:
			if len(line) != 0:
				line_list = re.split(r'\s{1,}', line)
			else:
				continue
			match = regex_string.search(line)
			if match:
				found_tunnel = True
				tunnel = str(match.group(1))
				sh_cmd['Tunnel ' + tunnel] = {}
				continue
			elif found_tunnel:
				found = regex_string2.search(line)
				if found:
					sh_cmd['Tunnel ' + tunnel]['Admin State'] = str(found.group(1))
					sh_cmd['Tunnel ' + tunnel]['Oper State'] = str(found.group(2))
				if destination_stripped not in sh_cmd['Tunnel ' + tunnel].keys():
					sh_cmd['Tunnel ' + tunnel]['Destination ' + destination_stripped] = ''
				state = regex_string4.search(line)
				if state:
					sh_cmd['Tunnel ' + tunnel][destination_stripped] = str(state.group(1))
			destination = regex_string3.search(line)
			if destination:
				destination_stripped = str(destination.group(1))
    return sh_cmd
def show_mpls_traffic_eng_tunnels_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show mpls traffic-eng tunnels
	#Each line being an item in a list
	#Determine how many tunnels there are
    counters = {'Total Tunnels': 0, 'Total Admin Up Tunnels': 0, 'Total Oper Up Tunnels': 0, 'Total Destinations': 0,'Total Up Destinations': 0, 'Total Any Other State Destinations':0}
    regex_string = re.compile('Destination\s\S+')
    for key in sh_cmd_dict:
		counters['Total Tunnels'] += 1
		for entry in sh_cmd_dict[key].items():
			if entry == 'Admin State':
				if sh_cmd_dict[key][entry] == 'up':
					counters['Total Admin Up Tunnels'] += 1
				continue
			if entry == 'Oper State':
				if sh_cmd_dict[key][entry] == 'up':
					counters['Total Oper Up Tunnels'] += 1
				continue
			match = regex_string.search(str(entry))
			if match:
				counters['Total Destinations'] += 1
				try:
					if sh_cmd_dict[key][entry] == 'Up':
						counters['Total Up Destinations'] += 1
					else:
						counters['Total Any Other State Destinations'] += 1
				except Exception as e:
					pass
    return counters
def show_bfd_session_compare(file):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show bfd session
	#Each line being an item in a list
	#Determine BFD state
    sh_cmd = {}
    regex_string = re.compile('^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
    found_line = False
    for line in file:
		if '-------------------' in line:
			found_line = True
		elif found_line == True:
			match = regex_string.search(line)
			if match:
				interface = str(match.group(1))
				destination = str(match.group(2))
				sh_cmd[interface + ' ' + destination] = str(match.group(3)) + ' ' + str(match.group(4)) + ' ' + str(match.group(5))
    return sh_cmd
def show_bfd_session_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show bfd session
	#Each line being an item in a list
	#Determine how many bfd session are UP or DOWN
    counters = {'Total BFD Sessions': 0, 'Total UP BFD Sessions': 0, 'Total DOWN BFD Sessions': 0}
    for key in sh_cmd_dict:
		counters['Total BFD Sessions'] += 1
		value = sh_cmd_dict[key]
		if 'UP' in value:
			counters['Total UP BFD Sessions'] += 1
		elif 'DOWN' in value:
			counters['Total DOWN BFD Sessions'] += 1
    return counters
####################
#CRS PD            #
####################
def admin_show_controller_fabric_plane_all_detail_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for admin show controller fabric plane all detail
	#Each line being an item in a list
	#Determine plane state
    sh_cmd = {}
    regex = re.compile('(\d)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+')
    regex2 = re.compile('(\d)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+')
    found_group = False
    for line in file:
        #logger.debug("show int line is: " + line)
        if len(line) != 0:
            line_list = re.split(r'\s{1,}', line)
        else:
            continue
        if "-----------------" in line:
            found_group = True
            continue
        elif found_group:
            match = regex.search(line)
            if match:
				sh_cmd[match.group(1)] = {}
				sh_cmd[match.group(1)]['Admin/Oper State'] = match.group(2) + ' ' + match.group(3)
				sh_cmd[match.group(1)]['Total Bundles'] = match.group(8)
				sh_cmd[match.group(1)]['Down Bundles'] = match.group(9)
            match = regex2.search(line)
            if match:
				sh_cmd[match.group(1)] = {}
				sh_cmd[match.group(1)]['Admin/Oper State'] = match.group(2)  + ' ' + match.group(3)
				sh_cmd[match.group(1)]['Total Bundles'] = match.group(7)
				sh_cmd[match.group(1)]['Down Bundles'] = match.group(8)
    return sh_cmd
def admin_show_controller_fabric_plane_all_detail_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for admin show controller fabric plane all detail
	#Each line being an item in a list
	#Determine Oper State and Bundle States
    counters = {'Total Planes': 0, 'Total Planes in UP UP State': 0, 'Total Planes in Any Other State': 0, 'Total Bundles': 0, 'Total Bundles Down': 0}
    for key in sh_cmd_dict:
        counters['Total Planes'] += 1
        if sh_cmd_dict[key]['Admin/Oper State'] == 'UP UP':
            counters['Total Planes in UP UP State'] += 1
        else:
            counters['Total Planes in Any Other State'] += 1
        if sh_cmd_dict[key]['Total Bundles']:
            value = sh_cmd_dict[key]['Total Bundles']
            counters['Total Bundles'] += int(value)
        if sh_cmd_dict[key]['Down Bundles']:
            value = sh_cmd_dict[key]['Down Bundles']
            counters['Total Bundles Down'] += int(value)
    return counters
####################
#ASR9K PD          #
####################
def show_pfm_loc_all_compare(file):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show pfm loc all
	#Each line being an item in a list
	#Determine alarm state
    sh_cmd = {}
    found_node = False
    regex_string = re.compile('(\w+\s)?(\w+\s+\d+\s+\d+\:\d+\:\d+)(\s\d+)?(\|--\||\|\d+\s?\|)(\S+)(\|)?.*\|(\S+).*\|\S+.*\|\S+.*\|(0x\S+)')
    regex2 = re.compile('(\w+\s)?(\w+\s+\d+\s+\d+\:\d+\:\d+)(\s\d+)?(\|--\||\|\d+\s?\|)(\S+)')
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if 'node:' in line:
			found_node = True
			node = line_list[1]
			sh_cmd[node] = {}
			continue
		elif '-------------' in line:
			continue
		elif found_node:
			match = regex_string.search(line)
			if match:
				sh_cmd[node]['Alarm and Severity ' +  str(match.group(5)) + ' With Handle ' + str(match.group(8))] = match.group(2) + ' ' + str(match.group(7)) 
    return sh_cmd
def show_pfm_loc_all_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show pfm loc all
	#Each line being an item in a list
	#Determine alarm state
    counters = {'Total Nodes': 0, 'Total Alarms': 0, 'Total Emergency/Alert alarms': 0, 'Total Critical Alarms': 0, 'Total Error Alarms': 0}
    regex_string = re.compile('NO\'\)$')
    regex_string2 = re.compile('E/A\'\)$')
    regex_string3 = re.compile('CR\'\)$')
    regex_string4 = re.compile('ER\'\)$')
    for key in sh_cmd_dict:
		counters['Total Nodes'] += 1
		for entry in sh_cmd_dict[key].items():
			match = regex_string.search(str(entry))
			if not match:
				counters['Total Alarms'] += 1
				match2 = regex_string2.search(str(entry))
				if match2:
					counters['Total Emergency/Alert alarms'] += 1
				match3 = regex_string3.search(str(entry))
				if match3:
					counters['Total Critical Alarms'] += 1
				match4 = regex_string4.search(str(entry))
				if match4:
					counters['Total Error Alarms'] += 1 
    return counters
####################
#NCS5500 PD        #
####################
def show_controllers_npu_resources_all_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show controllers npu resources all loc all
	#Each line being an item in a list
	#Determine NPU resources
    sh_cmd = {}
    found_location = False
    current_usage = False
    OOR_found = False
    total_found = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if 'Location' in line:
			found_location = True
			location = line_list[6]
			sh_cmd[location] = {}
		elif 'Name' in line:
			if total_found == True:
				sh_cmd[location][found_memory + ' ' + npu + ' Total In-Use'] = total
			found_memory = line_list[3]
			current_usage = False
			OOR_found = False
			OOR_state = line_list[4]
			total_found = False
		elif 'NPU' in line and current_usage == False:
			if OOR_found == True:
				sh_cmd[location][found_memory + ' ' + npu + ' OOR State'] = OOR_state
			npu = line_list[1]
		elif 'OOR State' in line:
			OOR_found = True
			OOR_state = line_list[4]
		elif 'Current Usage' in line:
			current_usage = True
			sh_cmd[location][found_memory + ' ' + npu + ' OOR State'] = OOR_state
		elif 'NPU' in line and current_usage == True:
			if total_found == True:
				sh_cmd[location][found_memory + ' ' + npu + ' Total In-Use'] = total
			npu = line_list[1]
		elif 'Total In-Use' in line:
			total_found = True
			total = line_list[4]
    return sh_cmd
def show_controllers_npu_resources_all_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show controllers npu resources all loc all
	#Each line being an item in a list
	#Determine NPU OOR Status
    counters = {'lem Green State': 0, 'lem Other State': 0, 'lpm Green State': 0, 'lpm Other State': 0, 'encap Green State': 0, 'encap Other State': 0,
				'fec Green State': 0, 'fec Other State': 0, 'ecmp_fec Green State': 0, 'ecmp_fec Other State': 0}
    regex_string = re.compile('lem')
    regex_string2 = re.compile('lpm')
    regex_string3 = re.compile('encap')
    regex_string4 = re.compile('ecmp_fec')
    regex_string5 = re.compile('fec')
    for key in sh_cmd_dict:
		for entry in sh_cmd_dict[key].items():
			print(str(entry))
			match = regex_string.search(str(entry))
			if match:
				if 'Green' in str(entry):
					counters['lem Green State'] += 1
				elif 'Total' in str(entry):
					pass
				else:
					counters['lem Other State'] += 1
				continue
			match = regex_string2.search(str(entry))
			if match:
				if 'Green' in str(entry):
					counters['lpm Green State'] += 1
				elif 'Total' in str(entry):
					pass
				else:
					counters['lpm Other State'] += 1
				continue
			match = regex_string3.search(str(entry))
			if match:
				if 'Green' in str(entry):
					counters['encap Green State'] += 1
				elif 'Total' in str(entry):
					pass
				else:
					counters['encap Other State'] += 1
				continue
			match = regex_string4.search(str(entry))
			if match:
				if 'Green' in str(entry):
					counters['ecmp_fec Green State'] += 1
				elif 'Total' in str(entry):
					pass
				else:
					counters['ecmp_fec Other State'] += 1
				continue
			match = regex_string5.search(str(entry))
			if match:
				if 'Green' in str(entry):
					counters['fec Green State'] += 1
				elif 'Total' in str(entry):
					pass
				else:
					counters['fec Other State'] += 1
    return counters
def show_controllers_fia_diag_alloc_all_compare(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show controllers fia diagshell 0 "diag alloc all" location all
	#Each line being an item in a list
	#Determine resource allocation
    sh_cmd = {}
    found_location = False
    regex_string = re.compile('^(\^M)?\s(.*\S+)\s+Total number of entries: (\d+)\s+Used entries (\d+).*$')
    current_usage = False
    OOR_found = False
    total_found = False
    for line in file:
		if len(line) != 0:
			line_list = re.split(r'\s{1,}', line)
		else:
			continue
		if 'Node' in line:
			found_location = True
			location = line_list[2]
			sh_cmd[location] = {}
		elif found_location == True:
			match = regex_string.search(line)
			if match:
				sh_cmd[location][str(match.group(2)) + ' Total Entries '] = str(match.group(3))
				sh_cmd[location][str(match.group(2)) + ' Used Entries '] = str(match.group(4))
    return sh_cmd
def show_controllers_fia_diag_alloc_all_totals(sh_cmd_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#Perform some magic on the pre and post lines of output for show controllers npu resources all loc all
	#Each line being an item in a list
	#Determine NPU OOR Status
    counters = {}
    return counters	
####################
#call main task    #
####################
if __name__ == '__main__':
    task()