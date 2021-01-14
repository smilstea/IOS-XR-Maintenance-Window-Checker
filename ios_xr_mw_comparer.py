__author__     = "Sam Milstead"
__copyright__  = "Copyright 2021 (C) Cisco TAC"
__credits__    = "Sam Milstead"
__version__    = "2.0.0"
__maintainer__ = "Sam Milstead"
__email__      = "smilstea@cisco.com"
__status__     = "alpha"

import os
import sys
import re

def task():
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
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
        print("Usage: python {" + sys.argv[0] + "} [--pre <filename>][|--post <filename>][--compare <filename>]")
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
        ####################
        #get platform      #
        ####################
        platform = "None"
        pre_commands = {}
        post_commands = {}
        show_version_found = False
        end_of_command = False
        command2 = str(commands[0])
        for line in pre_file:
            if 'show version' in line:
                print("found show version in " + str(pre))
                show_version_found = True
                if 'show version' not in pre_commands.keys():
                        pre_commands['show version' ] = ['show version']
            if end_of_command == True:
                break
            elif show_version_found == True:
                if command2 in line:
                    end_of_command = True
                else:
                    pre_commands['show version'].append(line)
                    if 'cisco ASR9K' in line:
                        platform = 'asr9k'
                    elif 'isco CRS' in line:
                        platform = 'crs'
                    elif 'cisco NCS-5500' in line:
                        platform = 'ncs5500'
                    elif 'cisco NCS-6000' in line:
                        platform = 'ncs6000'
        else:
            pre_file.close()
        try:
            pre_file.close()
        except Exception as e:
            pass
        show_version_found = False
        end_of_command = False
        for line in post_file:
            if 'show version' in line:
                print("found show version in " + str(post))
                show_version_found = True
                if 'show version' not in post_commands.keys():
                        post_commands['show version' ] = ['show version']
            if end_of_command == True:
                pass
            elif show_version_found == True:
                if command2 in line:
                    end_of_command = True
                else:
                    post_commands['show version'].append(line)
        else:
            post_file.close()   
        if platform == 'asr9k':
            commands.extend(asr9k_commands)
        elif platform == 'crs':
            commands.extend(crs_commands)
        elif platform == 'ncs5500':
            commands.extend(ncs5500_commands)
        elif platform == 'ncs6000':
            commands.extend(ncs6000_commands)
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
                if command == 'show platform':
                    pre_counters = show_platform_compare(pre_list, platform)
                    post_counters = show_platform_compare(post_list, platform)
                    pre_totals = show_platform_totals(pre_counters)
                    post_totals = show_platform_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = 'Card States:'
                    result = create_result('show platform', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show install active summary':
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
                    bgp_post_active = post_counters
                    ext_text = '\nBGP Summary:'
                    result = create_result('show bgp all all summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv4 unicast summary':
                    pre_counters = show_bgp_vrf_all_ipv4_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv4_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv4_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv4_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv4 Unicast Summary:'
                    result = create_result('show bgp vrf all ipv4 unicast summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv4 flowspec summary':
                    pre_counters = show_bgp_vrf_all_ipv4_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv4_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv4_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv4_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv4 Flowspec Summary:'
                    result = create_result('show bgp vrf all ipv4 flowspec summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv4 labeled-unicast summary':
                    pre_counters = show_bgp_vrf_all_ipv4_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv4_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv4_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv4_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv4 Labeled-unicast Summary:'
                    result = create_result('show bgp vrf all ipv4 labeled-unicast summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv4 multicast summary':
                    pre_counters = show_bgp_vrf_all_ipv4_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv4_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv4_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv4_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv4 Multicast Summary:'
                    result = create_result('show bgp vrf all ipv4 multicast summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv4 mvpn summary':
                    pre_counters = show_bgp_vrf_all_ipv4_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv4_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv4_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv4_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv4 MVPN Summary:'
                    result = create_result('show bgp vrf all ipv4 mvpn summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv6 unicast summary':
                    pre_counters = show_bgp_vrf_all_ipv6_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv6_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv6_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv6_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv6 Unicast Summary:'
                    result = create_result('show bgp vrf all ipv6 unicast summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv6 flowspec summary':
                    pre_counters = show_bgp_vrf_all_ipv6_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv6_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv6_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv6_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv6 Flowspec Summary:'
                    result = create_result('show bgp vrf all ipv6 flowspec summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv6 multicast summary':
                    pre_counters = show_bgp_vrf_all_ipv6_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv6_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv6_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv6_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv6 Multicast Summary:'
                    result = create_result('show bgp vrf all ipv6 multicast summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show bgp vrf all ipv6 mvpn summary':
                    pre_counters = show_bgp_vrf_all_ipv6_summary_compare(pre_list)
                    post_counters = show_bgp_vrf_all_ipv6_summary_compare(post_list)
                    pre_totals = show_bgp_vrf_all_ipv6_summary_totals(pre_counters)
                    post_totals = show_bgp_vrf_all_ipv6_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    bgp_post_active = post_counters
                    ext_text = '\nBGP VRF All IPv6 MVPN Summary:'
                    result = create_result('show bgp vrf all ipv6 mvpn summary', ext_text, pre_counters, pre_totals, post_counters)
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
                    ospf_post_active = post_counters
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
                    ospf_vrf_all_post_active = post_counters
                    ext_text = '\nOSPF VRF All Neighbor Summary:'
                    result = create_result('show ospf vrf all neighbor', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show ospfv3 neighbor':
                    pre_counters = show_ospf_neighbor_compare(pre_list)
                    post_counters = show_ospf_neighbor_compare(post_list)
                    pre_totals = show_ospf_neighbor_totals(pre_counters)
                    post_totals = show_ospf_neighbor_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ospf_post_active = post_counters
                    ext_text = '\nOSPFv3 Neighbor Summary:'
                    result = create_result('show ospfv3 neighbor', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show ospfv3 vrf all neighbor':
                    pre_counters = show_ospf_neighbor_compare(pre_list)
                    post_counters = show_ospf_neighbor_compare(post_list)
                    pre_totals = show_ospf_neighbor_totals(pre_counters)
                    post_totals = show_ospf_neighbor_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ospf_vrf_all_post_active = post_counters
                    ext_text = '\nOSPFv3 VRF All Neighbor Summary:'
                    result = create_result('show ospfv3 vrf all neighbor', ext_text, pre_counters, pre_totals, post_counters)
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
                elif command == 'show mpls traffic-eng tunnels p2p':
                    pre_counters = show_mpls_traffic_eng_tunnels_p2p_compare(pre_list)
                    post_counters = show_mpls_traffic_eng_tunnels_p2p_compare(post_list)
                    pre_totals = show_mpls_traffic_eng_tunnels_p2p_totals(pre_counters)
                    post_totals = show_mpls_traffic_eng_tunnels_p2p_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nMPLS Traffic Engineering P2P Summary:'
                    result = create_result('show mpls traffic-eng tunnels p2p', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show mpls traffic-eng tunnels p2mp':
                    pre_counters = show_mpls_traffic_eng_tunnels_p2mp_compare(pre_list)
                    post_counters = show_mpls_traffic_eng_tunnels_p2mp_compare(post_list)
                    pre_totals = show_mpls_traffic_eng_tunnels_p2mp_totals(pre_counters)
                    post_totals = show_mpls_traffic_eng_tunnels_p2mp_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nMPLS Traffic Engineering P2MP Summary:'
                    result = create_result('show mpls traffic-eng tunnels p2mp', ext_text, pre_counters, pre_totals, post_counters)
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
                elif command == 'show dhcp ipv4 proxy binding summary':
                    pre_counters = show_dhcp_ipv4_proxy_binding_summary_compare(pre_list)
                    post_counters = show_dhcp_ipv4_proxy_binding_summary_compare(post_list)
                    pre_totals = show_dhcp_ipv4_proxy_binding_summary_totals(pre_counters)
                    post_totals = show_dhcp_ipv4_proxy_binding_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nDHCPv4 Proxy Summary:'
                    result = create_result('show dhcp ipv4 proxy binding summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show dhcp ipv4 server binding summary':
                    pre_counters = show_dhcp_ipv4_server_binding_summary_compare(pre_list)
                    post_counters = show_dhcp_ipv4_server_binding_summary_compare(post_list)
                    pre_totals = show_dhcp_ipv4_server_binding_summary_totals(pre_counters)
                    post_totals = show_dhcp_ipv4_server_binding_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nDHCPv4 Server Summary:'
                    result = create_result('show dhcp ipv4 server binding summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show dhcp ipv6 proxy binding summary':
                    pre_counters = show_dhcp_ipv6_proxy_binding_summary_compare(pre_list)
                    post_counters = show_dhcp_ipv6_proxy_binding_summary_compare(post_list)
                    pre_totals = show_dhcp_ipv6_proxy_binding_summary_totals(pre_counters)
                    post_totals = show_dhcp_ipv6_proxy_binding_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nDHCPv6 Proxy Summary:'
                    result = create_result('show dhcp ipv6 proxy binding summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show dhcp ipv6 server binding summary':
                    pre_counters = show_dhcp_ipv6_server_binding_summary_compare(pre_list)
                    post_counters = show_dhcp_ipv6_server_binding_summary_compare(post_list)
                    pre_totals = show_dhcp_ipv6_server_binding_summary_totals(pre_counters)
                    post_totals = show_dhcp_ipv6_server_binding_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nDHCPv6 Server Summary:'
                    result = create_result('show dhcp ipv6 server binding summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show ipsla statistics':
                    pre_counters = show_ipsla_statistics_compare(pre_list)
                    post_counters = show_ipsla_statistics_compare(post_list)
                    pre_totals = show_ipsla_statistics_totals(pre_counters)
                    post_totals = show_ipsla_statistics_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nIPSLA statistics:'
                    result = create_result('show ipsla statistics', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'show subscriber session all summary':
                    pre_counters = show_subscriber_session_all_summary_compare(pre_list)
                    post_counters = show_subscriber_session_all_summary_compare(post_list)
                    pre_totals = show_subscriber_session_all_summary_totals(pre_counters)
                    post_totals = show_subscriber_session_all_summary_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nSubscriber Session All Summary:'
                    result = create_result('show subscriber session all summary', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'admin show controller fabric plane all detail':
                    if platform == 'crs':
                        pre_counters = crs_admin_show_controller_fabric_plane_all_detail_compare(pre_list)
                        post_counters = crs_admin_show_controller_fabric_plane_all_detail_compare(post_list)
                        pre_totals = crs_admin_show_controller_fabric_plane_all_detail_totals(pre_counters)
                        post_totals = crs_admin_show_controller_fabric_plane_all_detail_totals(post_counters)
                        pre_counters.update(pre_totals)
                        post_counters.update(post_totals)
                        ext_text = '\nCRS Fabric Summary:'
                        result = create_result('admin show controller fabric plane all detail', ext_text, pre_counters, pre_totals, post_counters)
                        response = print_results(result, pre_counters, post_counters, outfile)
                    elif platform == 'ncs6000':
                        pre_counters = ncs6k_admin_show_controller_fabric_plane_all_detail_compare(pre_list)
                        post_counters = ncs6k_admin_show_controller_fabric_plane_all_detail_compare(post_list)
                        pre_totals = ncs6k_admin_show_controller_fabric_plane_all_detail_totals(pre_counters)
                        post_totals = ncs6k_admin_show_controller_fabric_plane_all_detail_totals(post_counters)
                        pre_counters.update(pre_totals)
                        post_counters.update(post_totals)
                        ext_text = '\nNCS6K Fabric Summary:'
                        result = create_result('admin show controller fabric plane all detail', ext_text, pre_counters, pre_totals, post_counters)
                        response = print_results(result, pre_counters, post_counters, outfile)
                elif command == 'admin show controller fabric link health':
                    pre_counters = admin_show_controller_fabric_link_health_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_health_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_health_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_health_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nCRS Fabric Link Summary:'
                    result = create_result('admin show controller fabric link health', ext_text, pre_counters, pre_totals, post_counters)
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
                elif command == 'admin show controller fabric link port s1 tx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S1 Tx Down Links:'
                    result = create_result('admin show controller fabric link port s1 tx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s1 tx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S1 Tx Mismatch Links:'
                    result = create_result('admin show controller fabric link port s1 tx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s1 rx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S1 Rx Down Links:'
                    result = create_result('admin show controller fabric link port s1 rx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s1 rx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S1 Rx Mismatch Links:'
                    result = create_result('admin show controller fabric link port s1 rx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port fia tx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric FIA Tx Down Links:'
                    result = create_result('admin show controller fabric link port fia tx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port fia tx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric FIA Tx Mismatch Links:'
                    result = create_result('admin show controller fabric link port fia tx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port fia rx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric FIA Rx Down Links:'
                    result = create_result('admin show controller fabric link port fia rx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port fia rx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric FIA Rx Mismatch Links:'
                    result = create_result('admin show controller fabric link port fia rx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s2 tx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S2 Tx Down Links:'
                    result = create_result('admin show controller fabric link port s2 tx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s2 tx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S2 Tx Mismatch Links:'
                    result = create_result('admin show controller fabric link port s2 tx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s2 rx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S2 Rx Down Links:'
                    result = create_result('admin show controller fabric link port s2 rx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s2 rx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S2 Rx Mismatch Links:'
                    result = create_result('admin show controller fabric link port s2 rx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s3 tx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S3 Tx Down Links:'
                    result = create_result('admin show controller fabric link port s3 tx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s3 tx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S3 Tx Mismatch Links:'
                    result = create_result('admin show controller fabric link port s3 tx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s3 rx state down':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S3 Rx Down Links:'
                    result = create_result('admin show controller fabric link port s3 rx state down', ext_text, pre_counters, pre_totals, post_counters)
                    response = print_results(result, pre_counters, post_counters, outfile)  
                elif command == 'admin show controller fabric link port s3 rx state mismatch':
                    pre_counters = admin_show_controller_fabric_link_port_compare(pre_list)
                    post_counters = admin_show_controller_fabric_link_port_compare(post_list)
                    pre_totals = admin_show_controller_fabric_link_port_totals(pre_counters)
                    post_totals = admin_show_controller_fabric_link_port_totals(post_counters)
                    pre_counters.update(pre_totals)
                    post_counters.update(post_totals)
                    ext_text = '\nFabric S3 Rx Mismatch Links:'
                    result = create_result('admin show controller fabric link port s3 rx state mismatch', ext_text, pre_counters, pre_totals, post_counters)
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
#PI Commands       #
####################
def show_platform_compare(file, platform):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show platform
    #Each line being an item in a list
    #Determine Card state and return the pre and post results
    sh_plat = {}
    regex_string = re.compile('(\S+)\s+(\S+\s+\S+(\s\S+)?)\s+(\S+(\s\S+\s\S+)?)\s+(\S+)')
    regex_string2 = re.compile('(\S+)\s+(\S+)\s+(\S+(\s\S+\s\S+)?)\s+(\S+)')
    found_start = False
    for line in file:
        if '---------------' in line:
            found_start = True
            continue
        if found_start == True:
            if platform == 'crs':
                match = regex_string.search(line)
                if match:
                    sh_plat[match.group(1)] = {}
                    sh_plat[match.group(1)]['type'] = match.group(2)
                    sh_plat[match.group(1)]['State'] = match.group(4)
                    sh_plat[match.group(1)]['config state'] = match.group(6)
            else:
                match = regex_string2.search(line)
                if match:
                    sh_plat[match.group(1)] = {}
                    sh_plat[match.group(1)]['type'] = match.group(2)
                    sh_plat[match.group(1)]['State'] = match.group(3)
                    sh_plat[match.group(1)]['config state'] = match.group(5)
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show install active summary
    #Each line being an item in a list
    #Determine if all the same packages are loaded
    pkg_num = 0
    found_start = False
    sh_cmd = {}
    regex_string = re.compile('.*disk.*:.*')
    for line in file:
        #logger.debug("show int line is: " + line)
        if 'Active Packages' in line:
            found_start = True
        if found_start:
            match = regex_string.search(line)
            if match:
                sh_cmd[match.group(0)] = {}
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show interface description
    #Each line being an item in a list
    #Determine if status for an interface has changed
    found_start = False
    regex_string = re.compile('(\S+)\s+(\S+)\s+(\S+)(\s+(\S+.*))?')
    sh_int = {}
    for line in file:
        match = regex_string.search(line)
        if match:
            sh_int[match.group(1)] = {}
            sh_int[match.group(1)]['status'] = match.group(2)
            sh_int[match.group(1)]['protocol'] = match.group(3)
            try:
                sh_int[match.group(1)]['desc'] = match.group(5)
            except Exception as e:
                sh_int[match.group(1)]['desc'] = ' '
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
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show ipv6 interface brief
    #Each line being an item in a list
    #Determine if interface status has changed
    sh_int = {}
    regex_match = re.compile('^(\S+)\s+\[(\S+)\/(\S+)\]')
    for line in file:
        match = regex_match.search(line)
        if match:
            sh_int[match.group(1)] = {}
            sh_int[match.group(1)]['status'] = match.group(2)
            sh_int[match.group(1)]['protocol'] = match.group(3)
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show memory summary
    #Each line being an item in a list
    #Determine if memory has changed
    sh_cmd = {}
    regex_node = re.compile('node:\s+(\S+)')
    regex_appl = re.compile('Application Memory : (\S+\s\(\S+\s\S+\))')
    regex_image = re.compile('Image: (\S+\s\(\S+\s\S+\))')
    regex_reserved = re.compile('Reserved: (\S+\s\S+\s\S+\s\S+\s\S+)')
    regex_shared = re.compile('Total shared window: (\S+)')
    for line in file:
        match = regex_node.search(line)
        if match:
            node = match.group(1)
            sh_cmd[node] = {}
        match1 = regex_appl.search(line)
        match2 = regex_image.search(line)
        match3 = regex_reserved.search(line)
        match4 = regex_shared.search(line)
        if match1:
            sh_cmd[node]["Appl Memory"] = match1.group(1)
        elif match2:
            sh_cmd[node]["Image"] = match2.group(1)
        elif match3:
            sh_cmd[node]["Reserved"] = match3.group(1)
        elif match4:
            sh_cmd[node]["Total shared"] = match4.group(1)
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show filesystem
    #Each line being an item in a list
    #Determine if disk space has changed
    sh_cmd = {}
    found_node = False
    regex_node = re.compile('node:\s+(\S+)')
    regex_free = re.compile('\d+\s+(\S+)')
    for line in file:
        match = regex_node.search(line)
        if match:
            found_node = True
            node = match.group(1)
            sh_cmd[node] = {}
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
            match1 = regex_free.search(line)
            try:
                if match1:
                    megabytes = int(match1.group(1))*0.000001
                    megabytes = int(megabytes)
                    sh_cmd[node]["disk0: Free Space in MB"] = megabytes
            except Exception as e:
                if match1.group(1) == 0:
                        sh_cmd[node]["disk0: Free Space in MB"] = match1.group(1)
                else:
                    sh_cmd[node]["disk0: Free Space in Bytes"] = match1.group(1)
        elif found_node and "disk1:" in line:
            match1 = regex_free.search(line)
            try:
                megabytes = int(match1.group(1))*0.000001
                megabytes = int(megabytes)
                sh_cmd[node]["disk1: Free Space in MB"] = megabytes
            except Exception as e:
                if match1.group(1) == 0:
                    sh_cmd[node]["disk1: Free Space in MB"] = match1.group(1)
                else:
                    sh_cmd[node]["disk1: Free Space in Bytes"] = match1.group(1)
        elif found_node and " harddisk:" in line:
            match1 = regex_free.search(line)
            try:
                megabytes = int(match1.group(1))*0.000001
                megabytes = int(megabytes)
                sh_cmd[node]["harddisk: Free Space in MB"] = megabytes
            except Exception as e:
                if match1.group(1) == 0:
                    sh_cmd[node]["harddisk: Free Space in MB"] = match1.group(1)
                else:
                    sh_cmd[node]["harddisk: Free Space in Bytes"] = match1.group(1)
        elif found_node and "bootflash:" in line:
            found_node = False
        elif found_node and "nvram:" in line:
            found_node = False
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show route summary
    #Each line being an item in a list
    #Determine if number of routes has changed
    sh_cmd = {}
    found_vrf = False
    regex_connected = re.compile('connected\s+(\d+)')
    regex_local_vrrp = re.compile('local VRRP\s+(\d+)')
    regex_local_hsrp = re.compile('local HSRP\s+(\d+)')
    regex_local_lspv = re.compile('local LSPV\s+(\d+)')
    regex_local_smiap = re.compile('local SMIAP\s+(\d+)')
    regex_local = re.compile('local\s+(\d+)')
    regex_static = re.compile('static\s+(\d+)')
    regex_appl = re.compile('application\s+(\d+)')
    regex_subscriber = re.compile('subscriber\s+(\d+)')
    regex_isis = re.compile('isis\s+(\S+)\s+(\d+)')
    regex_dagr = re.compile('dagr\s+(\d+)')
    regex_bgp = re.compile('bgp\s+(\S+)\s+(\d+)')
    regex_eigrp = re.compile('eigrp\s+(\S+)\s+(\d+)')
    regex_ospf = re.compile('ospf\s+(\S+)\s+(\d+)')
    regex_total = re.compile('Total\s+(\d+)')
    regex_vrf = re.compile('VRF:\s(\S+)')
    for line in file:
        match = regex_connected.search(line)
        match1 = regex_local_vrrp.search(line)
        match2 = regex_local_hsrp.search(line)
        match3 = regex_local_lspv.search(line)
        match4 = regex_local_smiap.search(line)
        match5 = regex_local.search(line)
        match6 = regex_static.search(line)
        match7 = regex_appl.search(line)
        match8 = regex_subscriber.search(line)
        match9 = regex_isis.search(line)
        match10 = regex_dagr.search(line)
        match11 = regex_bgp.search(line)
        match12 = regex_eigrp.search(line)
        match13 = regex_ospf.search(line)
        match14 = regex_total.search(line)
        if found_vrf == False:
            if 'Route Source' in line:
                found_vrf = True
                vrf = 'default'
                sh_cmd[vrf] = {}
                continue
        elif 'VRF:' in line:
            found_vrf = True
            match15 = regex_vrf.search(line)
            vrf = match15.group(1)
            sh_cmd[vrf] = {}
            continue
        elif found_vrf:
            if match:
                sh_cmd[vrf]["Connected Routes"] = match.group(1)
            elif match1:
                sh_cmd[vrf]["Local VRRP Routes"] = match1.group(1)
            elif match2:
                sh_cmd[vrf]["Local HSRP Routes"] = match2.group(1)                                                  
            elif match3:
                sh_cmd[vrf]["Local LSPV Routes"] = match3.group(1)
            elif match4:
                sh_cmd[vrf]["Local SMIAP Routes"] = match4.group(1) 
            elif  match5:
                sh_cmd[vrf]["Local Routes"] = match5.group(1)
            elif match6:
                sh_cmd[vrf]["Static Routes"] = match6.group(1)
            elif match7:
                sh_cmd[vrf]["Application Routes"] = match7.group(1)
            elif match8:
                sh_cmd[vrf]["Subscriber Routes"] = match8.group(1)
            elif match9:
                sh_cmd[vrf]["isis " + match9.group(1) + " Routes"] = match9.group(2)
            elif match10:
                sh_cmd[vrf]["Dagr Routes"] = match10.group(1)
            elif match11:
                sh_cmd[vrf]["BGP " + match11.group(1) + " Routes"] = match11.group(2)
            elif match12:
                sh_cmd[vrf]["EIGRP " + match12.group(1) + " Routes"] = match12.group(2) 
            elif match13:
                sh_cmd[vrf]["OSPF " + match13.group(1) + " Routes"] = match13.group(2)
            elif match14:
                sh_cmd[vrf]["Total Routes"] = match14.group(1)
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show redundancy
    #Each line being an item in a list
    #Determine if redundancy state has changed
    sh_cmd = {}
    found_group = False
    regex_search = re.compile('^(\S+)')
    for line in file:
        match = regex_search.search(line)
        if "---------        ---------" in line:
            found_group = True
            continue
        elif "Process Group Details" in line:
            found_group = False
        elif found_group and "Not NSR-Ready" in line:
            sh_cmd[match.group(1)] = {}
            sh_cmd[match.group(1)]['status'] = "Not NSR-Ready"
        elif found_group and "Not Ready" in line:
            sh_cmd[match.group(1)] = {}
            sh_cmd[match.group(1)]['status'] = "Not Ready"
        elif found_group and "Ready" in line:
            sh_cmd[match.group(1)] = {}
            sh_cmd[match.group(1)]['status'] = "Ready"
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
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show bgp all all summary
    #Each line being an item in a list
    #Determine if neighbor state or prefixes have changed
    sh_cmd = {}
    found_AF = False
    neighbor_found = False
    AF_regex = re.compile('Address Family:\s(\S+\s\S+)')
    regex_string = re.compile('^((([a-f0-9:]+:+)+[a-f0-9]+)|\d+\.\d+\.\d+\.\d+)')
    regex_string2 = re.compile('^((([a-f0-9:]+:+)+[a-f0-9]+)|\d+\.\d+\.\d+\.\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+(\S+)')
    ipv6_regex_line2 = re.compile('^\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+(\S+)')
    for line in file:
        match = AF_regex.search(line)
        if match:
            found_AF = True
            AF = match.group(1)
            sh_cmd[AF] = {}
            continue
        elif '-------------' in line:
            continue
        elif found_AF:
            found = regex_string.search(line)
            #sometimes ipv6 neighbors appear on two lines instead of 1
            if found:
                neighbor_found = True
                found2 = regex_string2.search(line)
                if found2:
                    sh_cmd[AF][found2.group(1)] = 'Prefix Received: ' + found2.group(4)
                    neighbor_found = False
                else:
                    neighbor = found.group(1)
            elif neighbor_found == True:
                found3 = ipv6_regex_line2.search(line)
                if found3:
                    sh_cmd[AF][neighbor] = 'Prefix Received: ' + found3.group(1)
                neighbor_found = False
    return sh_cmd
def show_bgp_all_all_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.0.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show bgp all all summary
    #Each line being an item in a list
    #Determine total AFs and routes
    counters = {'Total AFs': 0, 'Total Neighbors': 0, 'Total Routes': 0}
    regex = re.compile('(\d+)')
    for key in sh_cmd_dict:
        counters['Total AFs'] += 1
        for value in sh_cmd_dict[key]:
            counters['Total Neighbors'] += 1
            mytotal = sh_cmd_dict[key][value]
            match = regex.search(mytotal)
            if match:
                mynewtotal = match.group(0)
                counters['Total Routes'] += int(mynewtotal)
    return counters
def show_bgp_vrf_all_ipv4_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show bgp vrf all ipv4 <> summary
    #Determine if neighbor state or prefixes have changed
    sh_cmd = {}
    found_VRF = False
    regex_string = re.compile('(\d+\.\d+\.\d+\.\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s\S+\s+(\S+)')
    vrf_regex = re.compile('VRF: (\S+)')
    for line in file:
        match = vrf_regex.search(line)
        if match:
            found_VRF = True
            VRF = match.group(1)
            sh_cmd[VRF] = {}
            continue
        elif found_VRF:
            found = regex_string.search(line)
            if found:
                sh_cmd[VRF][found.group(1)] = 'Prefix Received: ' + found.group(2)
    return sh_cmd
def show_bgp_vrf_all_ipv4_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show bgp vrf all ipv4 <> summary
    #Determine total VRFs and routes
    counters = {'Total VRFs': 0, 'Total Neighbors': 0, 'Total Routes': 0}
    regex = re.compile('(\d+)')
    for key in sh_cmd_dict:
        counters['Total VRFs'] += 1
        for value in sh_cmd_dict[key]:
            counters['Total Neighbors'] += 1
            mytotal = sh_cmd_dict[key][value]
            match = regex.search(mytotal)
            if match:
                mynewtotal = match.group(0)
                counters['Total Routes'] += int(mynewtotal)
    return counters
def show_bgp_vrf_all_ipv6_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show bgp vrf all ipv6 <> summary
    #Determine if neighbor state or prefixes have changed
    sh_cmd = {}
    found_VRF = False
    neighbor_found = False
    regex_string = re.compile('(([a-f0-9:]+:+)+[a-f0-9]+)')
    ipv6_regex_line2 = re.compile('^\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+(\S+)')
    vrf_regex = re.compile('VRF: (\S+)')
    for line in file:
        match = vrf_regex.search(line)
        if match:
            found_VRF = True
            VRF = match.group(1)
            sh_cmd[VRF] = {}
            continue
        elif found_VRF:
            found = regex_string.search(line)
            #sometimes ipv6 neighbors appear on two lines instead of 1
            if found:
                neighbor_found = True
                found2 = ipv6_regex_line2.search(line)
                if found2:
                    sh_cmd[VRF][found.group(0)] = 'Prefix Received: ' + found2.group(1)
                    neighbor_found = False
                else:
                    neighbor = found.group(0)
            elif neighbor_found == True:
                found2 = ipv6_regex_line2.search(line)
                if found2:
                    sh_cmd[VRF][neighbor] = 'Prefix Received: ' + found2.group(1)
                neighbor_found = False
    return sh_cmd
def show_bgp_vrf_all_ipv6_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show bgp vrf all ipv6 <> summary
    #Determine total VRFs and routes
    counters = {'Total VRFs': 0, 'Total Neighbors': 0, 'Total Routes': 0}
    regex = re.compile('(\d+)')
    for key in sh_cmd_dict:
        counters['Total VRFs'] += 1
        for value in sh_cmd_dict[key]:
            counters['Total Neighbors'] += 1
            mytotal = sh_cmd_dict[key][value]
            match = regex.search(mytotal)
            if match:
                mynewtotal = match.group(0)
                counters['Total Routes'] += int(mynewtotal)
    return counters
def show_l2vpn_xconnect_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show l2vpn xconnect
    #Each line being an item in a list
    #Determine if state has changed for xconnect
    sh_cmd = {}
    found_start = False
    list_test = ['UP', 'DN', 'AD', 'UR', 'SB', 'SR' 'PP']
    regex_string = re.compile('^(\S+)\s+(\S+)\s+(UP|DN|AD|UR|SB|SR|PP)')
    regex_string2 = re.compile('^(\S+)\s+(UP|DN|AD|UR|SB|SR|PP)')
    for line in file:
        if '------------------------' in line:
            found_start = True
            continue
        if found_start:
            match = regex_string.search(line)
            if match:
                sh_cmd[match.group(1) + ' ' + match.group(2)] = {}
                sh_cmd[match.group(1) + ' ' + match.group(2)]['Xconnect Status (Overall)'] = match.group(3) 
            else:
                match2 = regex_string2.search(line)
                if match:
                    sh_cmd['Unknown Xconnect Name, With Name: ' + match2.group(1)] = {}
                    sh_cmd['Unknown Xconnect Name, With Name: ' + match2.group(1)]['Xconnect Status (Overall)'] = match2.group(2)    
    return sh_cmd
def show_l2vpn_xconnect_totals(sh_cmd):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
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
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show l2vpn xconnect
    #Each line being an item in a list
    #Determine if state has changed for bridge domain
    sh_cmd = {}
    found_BG = False
    regex_string = re.compile('ACs: (\d+) \((\d+) up\), VFIs: (\d+), PWs: (\d+) \((\d+) up\), PBBs: (\d+) \((\d+) up\), VNIs: (\d+) \((\d+) up\)')
    regex_bridge = re.compile('Bridge group: (\S+), bridge-domain: (\S+),')
    for line in file:
        match = regex_bridge.search(line)
        if match:
            found_BG = True
            BG = match.group(1) + " " + match.group(2)
            sh_cmd[BG] = {}
        elif '-------------' in line:
            continue
        elif found_BG:
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
    return sh_cmd
def show_l2vpn_bridge_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show l2vpn xconnect
    #Each line being an item in a list
    #Determine total circuits and states
    counters = {'Total Circuits': 0, 'ACs in Up State': 0, 'PWs in Up State': 0, 'VNIs in Up State': 0, 'PBBs in Up State': 0}
    for key in sh_cmd_dict:
        for value in sh_cmd_dict[key]:
            myvalue = sh_cmd_dict[key][value]
            if 'Total' in value:
                counters['Total Circuits'] += int(myvalue)
            elif 'ACs Up' in value:  
                counters['ACs in Up State'] +=  int(myvalue)
            elif 'PWs Up' in value:  
                counters['PWs in Up State'] +=  int(myvalue)
            elif 'PBBs Up' in value:  
                counters['PBBs in Up State'] +=  int(myvalue)
            elif 'VNIs Up' in value:  
                counters['VNIs in Up State'] +=  int(myvalue)
    return counters
def show_nv_satellite_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show nv satellite status
    #Each line being an item in a list
    #Determine if satellite status, icl, etc has changed
    sh_cmd = {}
    regex_string = re.compile('Satellite (\d+)')
    icl_string = re.compile('\S+')
    found_satellite = False
    found_icl = False
    for line in file:
        match = regex_string.search(line)
        if match:
            found_satellite = True
            found_icl = False
            satellite = match.group(1)
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
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show ospf neighbor
    #Each line being an item in a list
    #Determine if OSPF neighborship has changed
    sh_cmd = {}
    neighbor_regex = re.compile('Neighbors for (OSPF.*)')
    regex_string = re.compile('(\d+\.\d+\.\d+\.\d+)\s+\d+\s+(\S+)\s+-?\s+\S+\s+((\d+\.\d+\.\d+\.\d+)|(\d+))\s+(\S+)')
    found_ospf = False
    for line in file:
        match = neighbor_regex.search(line)
        if match:
            found_ospf = True
            ospf = match.group(1)
            sh_cmd[ospf] = {}
            continue
        elif 'Total neighbor count' in line:
            found_ospf = False
        elif found_ospf:
            found = regex_string.search(line)
            if found:
                sh_cmd[ospf]['Neighbor ' + found.group(1) + ' ' + found.group(3) + ' ' + found.group(6) + " In State: "] = found.group(2)
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
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show isis neighbor
    #Each line being an item in a list
    #Determine isis neighbor details
    sh_cmd = {}
    regex_string = re.compile('IS-IS (\S+) neighbors:')
    regex_string2 = re.compile('(\S+)\s+(\S+\S+\d+)\s+(\S+)\s+(\S+)\s+\d+\s+\S+\s+\S+')
    found_isis = False
    for line in file:
        match = regex_string.search(line)
        if match:
            found_isis = True
            isis = match.group(1)
            sh_cmd['ISIS ' + isis] = {}
            continue
        elif found_isis:
            found = regex_string2.search(line)
            if found:
                sh_cmd['ISIS ' + isis]['Neighbor ' + found.group(1) + ' ' + found.group(2) + " in State: "] = found.group(4)
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
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show mpls ldp neighbor brief
    #Each line being an item in a list
    #Determine neighborships, labels, etc
    sh_cmd = {}
    found_group = False
    regex = re.compile('(((([a-f0-9:]+:+)+[a-f0-9]+)|\d+\.\d+\.\d+\.\d+):\d)\s+(\S)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
    regex2 = re.compile('(((([a-f0-9:]+:+)+[a-f0-9]+)|\d+\.\d+\.\d+\.\d+):\d)\s+(\S)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)')
    for line in file:
        if "-----------------" in line:
            found_group = True
            continue
        elif found_group:
            match = regex.search(line)
            match2 = regex2.search(line)
            if match:
                sh_cmd[match.group(1)] = {}
                sh_cmd[match.group(1)]['GR'] = match.group(5)
                sh_cmd[match.group(1)]['NSR'] = match.group(6)
                sh_cmd[match.group(1)]['Discovery IPv4'] = match.group(8)
                sh_cmd[match.group(1)]['Discovery IPv6'] = match.group(9)
                sh_cmd[match.group(1)]['Addresses IPv4'] = match.group(10)
                sh_cmd[match.group(1)]['Addresses IPv6'] = match.group(11)
                sh_cmd[match.group(1)]['Labels IPv4'] = match.group(12)
                sh_cmd[match.group(1)]['Labels IPv6'] = match.group(13)
            elif match2:
                sh_cmd[match2.group(1)] = {}
                sh_cmd[match2.group(1)]['GR'] = match2.group(5)
                sh_cmd[match2.group(1)]['NSR'] = match2.group(6)
                sh_cmd[match2.group(1)]['Discovery'] = match2.group(8)
                sh_cmd[match2.group(1)]['Addresses'] = match2.group(9)
                sh_cmd[match2.group(1)]['Labels IPv4'] = match2.group(10)
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
def show_mpls_traffic_eng_tunnels_p2p_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.2"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show mpls traffic-eng tunnels p2p
    #Each line being an item in a list
    #Determine tunnel state
    sh_cmd = {}
    regex_string = re.compile('Signalled-Name:\s(\S+)')
    regex_string2 = re.compile('Admin:\s(\S+)\s+Oper:\s(\S+)')
    regex_string3 = re.compile('Destination:\s(\S+)')
    found_tunnel = False
    for line in file:
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
            #this is needed when no destination is configured
            try:
                if destination_stripped not in sh_cmd['Tunnel ' + tunnel].keys():
                    sh_cmd['Tunnel ' + tunnel]['Destination'] = destination_stripped
            except Exception as e:
                sh_cmd['Tunnel ' + tunnel]['Destination'] = 'no destination'
        destination = regex_string3.search(line)
        if destination:
            destination_stripped = str(destination.group(1))
    return sh_cmd
def show_mpls_traffic_eng_tunnels_p2p_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show mpls traffic-eng tunnels p2p
    #Each line being an item in a list
    #Determine how many tunnels there are
    counters = {'Total Tunnels': 0, 'Total Admin Up Tunnels': 0, 'Total Oper Up Tunnels': 0, 'Total Destinations': 0}
    for key in sh_cmd_dict:
        counters['Total Tunnels'] += 1
        for value in sh_cmd_dict[key]:
            if value ==  'Admin State':
                if sh_cmd_dict[key][value] == 'up':
                    counters['Total Admin Up Tunnels'] += 1
            elif value ==  'Oper State':
                if sh_cmd_dict[key][value] == 'up':
                    counters['Total Oper Up Tunnels'] += 1
            elif value ==  'Destination':
                counters['Total Destinations'] += 1
    return counters
def show_mpls_traffic_eng_tunnels_p2mp_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show mpls traffic-eng tunnels p2mp
    #Each line being an item in a list
    #Determine tunnel state
    sh_cmd = {}
    regex_string = re.compile('Signalled-Name:\s(\S+)')
    regex_string2 = re.compile('Admin:\s(\S+)\s+Oper:\s(\S+)')
    regex_string3 = re.compile('Destination:\s(\S+)')
    regex_string4 = re.compile('State:\s(\S+)')
    found_tunnel = False
    for line in file:
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
            state = regex_string4.search(line)
            if state:
                sh_cmd['Tunnel ' + tunnel]['Destination ' + destination_stripped] = str(state.group(1))
    return sh_cmd
def show_mpls_traffic_eng_tunnels_p2mp_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show mpls traffic-eng tunnels p2mp
    #Each line being an item in a list
    #Determine how many tunnels there are
    counters = {'Total Tunnels': 0, 'Total Admin Up Tunnels': 0, 'Total Oper Up Tunnels': 0, 'Total Destinations': 0,'Total Up Destinations': 0, 'Total Any Other State Destinations':0}
    for key in sh_cmd_dict:
        counters['Total Tunnels'] += 1
        for value in sh_cmd_dict[key]:
            if value ==  'Admin State':
                if sh_cmd_dict[key][value] == 'up':
                    counters['Total Admin Up Tunnels'] += 1
            elif value ==  'Oper State':
                if sh_cmd_dict[key][value] == 'up':
                    counters['Total Oper Up Tunnels'] += 1
            elif 'Destination' in value:
                counters['Total Destinations'] += 1
                if sh_cmd_dict[key][value] == 'Up':
                    counters['Total Up Destinations'] += 1
                else:
                    counters['Total Any Other State Destinations'] += 1
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
def show_dhcp_ipv4_proxy_binding_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv4 proxy binding summary
    #Each line being an item in a list
    sh_cmd = {}
    regex_total = re.compile('Total number of clients: (\d+)')
    regex_string = re.compile('(\S+).*\|\s+(\d+)')
    found_line = False
    for line in file:
        if '-------------------' in line:
            found_line = True
        elif found_line == True:
            match = regex_string.search(line)
            if match:
                state = match.group(1)
                count = match.group(2)
                sh_cmd[state] = count
        else:
            match = regex_total.search(line)
            if match:
                sh_cmd['Total'] = match.group(1)
    return sh_cmd
def show_dhcp_ipv4_proxy_binding_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv4 proxy binding summary
    #Each line being an item in a list
    #Determine if bindings changes
    counters = {'DHCP Total Sessions': 0, 'DHCP INIT Sessions': 0, 'DHCP INIT_DPM_WAITING Sessions': 0, 'DHCP SELECTING Sessions': 0, 'DHCP OFFER_SENT Sessions': 0, 'DHCP REQUESTING Sessions': 0, 'DHCP REQUEST_INIT_DPM_WAITING Sessions': 0, 'DHCP ACK_DPM_WAITING Sessions': 0, 'DHCP BOUND Sessions': 0,
                'DHCP RENEWING Sessions': 0, 'DHCP INFORMING Sessions': 0, 'DHCP REAUTHORIZE Sessions': 0, 'DHCP DISCONNECT_DPM_WAIT Sessions': 0, 'DHCP ADDR_CHANGE_DPM_WAIT Sessions': 0, 'DHCP DELETING Sessions': 0, 'DHCP DISCONNECTED Sessions': 0, 'DHCP RESTARTING Sessions': 0}
    for key in sh_cmd_dict:
        value = sh_cmd_dict[key]
        if key == 'Total':
            counters['DHCP Total Sessions'] = value
        elif key == 'INIT':
            counters['DHCP INIT Sessions'] = value
        elif key == 'INIT_DPM_WAITING':
            counters['DHCP INIT_DPM_WAITING Sessions']  = value
        elif key == 'SELECTING':
            counters['DHCP SELECTING Sessions']  = value
        elif key == 'OFFER_SENT':
            counters['DHCP OFFER_SENT Sessions']  = value
        elif key == 'REQUESTING':
            counters['DHCP REQUESTING Sessions']  = value
        elif key == 'REQUEST_INIT_DPM_WAITING':
            counters['DHCP REQUEST_INIT_DPM_WAITING Sessions']  = value
        elif key == 'ACK_DPM_WAITING':
            counters['DHCP ACK_DPM_WAITING Sessions']  = value
        elif key == 'BOUND':
            counters['DHCP BOUND Sessions']  = value
        elif key == 'RENEWING':
            counters['DHCP RENEWING Sessions']  = value
        elif key == 'INFORMING':
            counters['DHCP INFORMING Sessions']  = value
        elif key == 'REAUTHORIZE':
            counters['DHCP REAUTHORIZE Sessions']  = value
        elif key == 'DISCONNECT_DPM_WAIT':
            counters['DHCP DISCONNECT_DPM_WAIT Sessions']  = value
        elif key == 'ADDR_CHANGE_DPM_WAIT':
            counters['DHCP ADDR_CHANGE_DPM_WAIT Sessions']  = value
        elif key == 'DELETING':
            counters['DHCP DELETING Sessions']  = value
        elif key == 'DISCONNECTED':
            counters['DHCP DISCONNECTED Sessions']  = value
        elif key == 'RESTARTING':
            counters['DHCP RESTARTING Sessions']  = value
    return counters 
def show_dhcp_ipv4_server_binding_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv4 server binding summary
    #Each line being an item in a list
    sh_cmd = {}
    regex_total = re.compile('Total number of clients: (\d+)')
    regex_string = re.compile('(\S+).*\|\s+(\d+)')
    found_line = False
    for line in file:
        if '-------------------' in line:
            found_line = True
        elif found_line == True:
            match = regex_string.search(line)
            if match:
                state = match.group(1)
                count = match.group(2)
                sh_cmd[state] = count
        else:
            match = regex_total.search(line)
            if match:
                sh_cmd['Total'] = match.group(1)
    return sh_cmd
def show_dhcp_ipv4_server_binding_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv4 server binding summary
    #Each line being an item in a list
    #Determine if bindings changes
    counters = {'DHCP Total Sessions': 0, 'DHCP INIT Sessions': 0, 'DHCP INIT_DPM_WAITING Sessions': 0, 'DHCP INIT_DAPS_WAITING Sessions': 0, 'DHCP SELECTING Sessions': 0, 'DHCP OFFER_SENT Sessions': 0, 'DHCP REQUESTING Sessions': 0, 'DHCP REQUEST_INIT_DPM_WAITING Sessions': 0, 'DHCP ACK_DPM_WAITING Sessions': 0, 'DHCP BOUND Sessions': 0,
                'DHCP RENEWING Sessions': 0, 'DHCP INFORMING Sessions': 0, 'DHCP REAUTHORIZE Sessions': 0, 'DHCP DISCONNECT_DPM_WAIT Sessions': 0, 'DHCP ADDR_CHANGE_DPM_WAIT Sessions': 0, 'DHCP DELETING Sessions': 0, 'DHCP DISCONNECTED Sessions': 0, 'DHCP RESTARTING Sessions': 0}
    for key in sh_cmd_dict:
        value = sh_cmd_dict[key]
        if key == 'Total':
            counters['DHCP Total Sessions'] = value
        elif key == 'INIT':
            counters['DHCP INIT Sessions'] = value
        elif key == 'INIT_DPM_WAITING':
            counters['DHCP INIT_DPM_WAITING Sessions']  = value
        elif key == 'SELECTING':
            counters['DHCP SELECTING Sessions']  = value
        elif key == 'OFFER_SENT':
            counters['DHCP OFFER_SENT Sessions']  = value
        elif key == 'REQUESTING':
            counters['DHCP REQUESTING Sessions']  = value
        elif key == 'REQUEST_INIT_DPM_WAITING':
            counters['DHCP REQUEST_INIT_DPM_WAITING Sessions']  = value
        elif key == 'INIT_DAPS_WAITING':
            counters['DHCP INIT_DAPS_WAITING Sessions']  = value
        elif key == 'ACK_DPM_WAITING':
            counters['DHCP ACK_DPM_WAITING Sessions']  = value
        elif key == 'BOUND':
            counters['DHCP BOUND Sessions']  = value
        elif key == 'RENEWING':
            counters['DHCP RENEWING Sessions']  = value
        elif key == 'INFORMING':
            counters['DHCP INFORMING Sessions']  = value
        elif key == 'REAUTHORIZE':
            counters['DHCP REAUTHORIZE Sessions']  = value
        elif key == 'DISCONNECT_DPM_WAIT':
            counters['DHCP DISCONNECT_DPM_WAIT Sessions']  = value
        elif key == 'ADDR_CHANGE_DPM_WAIT':
            counters['DHCP ADDR_CHANGE_DPM_WAIT Sessions']  = value
        elif key == 'DELETING':
            counters['DHCP DELETING Sessions']  = value
        elif key == 'DISCONNECTED':
            counters['DHCP DISCONNECTED Sessions']  = value
        elif key == 'RESTARTING':
            counters['DHCP RESTARTING Sessions']  = value
    return counters     
def show_dhcp_ipv6_proxy_binding_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv6 proxy binding summary
    #Each line being an item in a list
    sh_cmd = {}
    regex_total = re.compile('Total number of clients: (\d+)')
    regex_string = re.compile('(\S+\s*\S*\s*\S*)\s*\|\s+(\d+)\s+\|\s+(\d+)')
    found_line = False
    for line in file:
        if '-------------------' in line:
            found_line = True
        elif found_line == True:
            match = regex_string.search(line)
            if match:
                state = str(match.group(1))
                state = state.rstrip()
                count_ia_na = match.group(2)
                count_ia_pd = match.group(3)
                sh_cmd[state] = {}
                sh_cmd[state]['IA-NA'] = count_ia_na
                sh_cmd[state]['IA-PD'] = count_ia_pd
        else:
            match = regex_total.search(line)
            if match:
                sh_cmd['Total'] = match.group(1)
    return sh_cmd
def show_dhcp_ipv6_proxy_binding_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv6 proxy binding summary
    #Each line being an item in a list
    #Determine if bindings changes
    counters = {'DHCP Total Sessions': 0, 'DHCP INIT IA-NA Sessions': 0, 'DHCP SUB VALIDATING IA-NA Sessions': 0, 'DHCP ADDR/PREFIX ALLOCATING IA-NA Sessions': 0, 'DHCP REQUESTING IA-NA Sessions': 0, 'DHCP SESSION RESP PENDING IA-NA Sessions': 0, 'DHCP ROUTE UPDATING IA-NA Sessions': 0, 'DHCP BOUND IA-NA Sessions': 0,
                'DHCP INIT IA-PD Sessions': 0, 'DHCP SUB VALIDATING IA-PD Sessions': 0, 'DHCP ADDR/PREFIX ALLOCATING IA-PD Sessions': 0, 'DHCP REQUESTING IA-PD Sessions': 0, 'DHCP SESSION RESP PENDING IA-PD Sessions': 0, 'DHCP ROUTE UPDATING IA-PD Sessions': 0, 'DHCP BOUND IA-PD Sessions': 0}
    for key in sh_cmd_dict:
        if key == 'Total':
            counters['DHCP Total Sessions'] = sh_cmd_dict[key]
        else:
            value = sh_cmd_dict[key]['IA-NA']
            value2 = sh_cmd_dict[key]['IA-PD']
            if 'INIT' in key:
                counters['DHCP INIT IA-NA Sessions'] = value
                counters['DHCP INIT IA-PD Sessions'] = value2
            elif 'SUB VALIDATING' in key:
                counters['DHCP SUB VALIDATING IA-NA Sessions']  = value
                counters['DHCP SUB VALIDATING IA-PD Sessions']  = value2
            elif 'ADDR/PREFIX ALLOCATING' in key:
                counters['DHCP ADDR/PREFIX ALLOCATING IA-NA Sessions']  = value
                counters['DHCP ADDR/PREFIX ALLOCATING IA-PD Sessions']  = value2
            elif 'REQUESTING' in key:
                counters['DHCP ADDR/PREFIX ALLOCATING IA-NA Sessions']  = value
                counters['DHCP ADDR/PREFIX ALLOCATING IA-PD Sessions']  = value2
            elif 'SESSION RESP PENDING' in key:
                counters['DHCP SESSION RESP PENDING IA-NA Sessions']  = value
                counters['DHCP SESSION RESP PENDING IA-PD Sessions']  = value2
            elif 'ROUTE UPDATING' in key:
                counters['DHCP ROUTE UPDATING IA-NA Sessions']  = value
                counters['DHCP ROUTE UPDATING IA-PD Sessions']  = value2
            elif 'BOUND' in key:
                counters['DHCP BOUND IA-NA Sessions']  = value
                counters['DHCP BOUND IA-PD Sessions']  = value2
    return counters     
def show_dhcp_ipv6_server_binding_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv6 server binding summary
    #Each line being an item in a list
    sh_cmd = {}
    regex_total = re.compile('Total number of clients: (\d+)')
    regex_string = re.compile('(\S+\s*\S*\s*\S*)\s*\|\s+(\d+)\s+\|\s+(\d+)')
    found_line = False
    for line in file:
        if '-------------------' in line:
            found_line = True
        elif found_line == True:
            match = regex_string.search(line)
            if match:
                state = str(match.group(1))
                state = state.rstrip()
                count_ia_na = match.group(2)
                count_ia_pd = match.group(3)
                sh_cmd[state] = {}
                sh_cmd[state]['IA-NA'] = count_ia_na
                sh_cmd[state]['IA-PD'] = count_ia_pd
        else:
            match = regex_total.search(line)
            if match:
                sh_cmd['Total'] = match.group(1)
    return sh_cmd
def show_dhcp_ipv6_server_binding_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show dhcp ipv6 server binding summary
    #Each line being an item in a list
    #Determine if bindings changes
    counters = {'DHCP Total Sessions': 0, 'DHCP INIT IA-NA Sessions': 0, 'DHCP SUB VALIDATING IA-NA Sessions': 0, 'DHCP ADDR/PREFIX ALLOCATING IA-NA Sessions': 0, 'DHCP REQUESTING IA-NA Sessions': 0, 'DHCP SESSION RESP PENDING IA-NA Sessions': 0, 'DHCP ROUTE UPDATING IA-NA Sessions': 0, 'DHCP BOUND IA-NA Sessions': 0,
                'DHCP INIT IA-PD Sessions': 0, 'DHCP SUB VALIDATING IA-PD Sessions': 0, 'DHCP ADDR/PREFIX ALLOCATING IA-PD Sessions': 0, 'DHCP REQUESTING IA-PD Sessions': 0, 'DHCP SESSION RESP PENDING IA-PD Sessions': 0, 'DHCP ROUTE UPDATING IA-PD Sessions': 0, 'DHCP BOUND IA-PD Sessions': 0}
    for key in sh_cmd_dict:
        if key == 'Total':
            counters['DHCP Total Sessions'] = sh_cmd_dict[key]
        else:
            value = sh_cmd_dict[key]['IA-NA']
            value2 = sh_cmd_dict[key]['IA-PD']
            if 'INIT' in key:
                counters['DHCP INIT IA-NA Sessions'] = value
                counters['DHCP INIT IA-PD Sessions'] = value2
            elif 'SUB VALIDATING' in key:
                counters['DHCP SUB VALIDATING IA-NA Sessions']  = value
                counters['DHCP SUB VALIDATING IA-PD Sessions']  = value2
            elif 'ADDR/PREFIX ALLOCATING' in key:
                counters['DHCP ADDR/PREFIX ALLOCATING IA-NA Sessions']  = value
                counters['DHCP ADDR/PREFIX ALLOCATING IA-PD Sessions']  = value2
            elif 'REQUESTING' in key:
                counters['DHCP ADDR/PREFIX ALLOCATING IA-NA Sessions']  = value
                counters['DHCP ADDR/PREFIX ALLOCATING IA-PD Sessions']  = value2
            elif 'SESSION RESP PENDING' in key:
                counters['DHCP SESSION RESP PENDING IA-NA Sessions']  = value
                counters['DHCP SESSION RESP PENDING IA-PD Sessions']  = value2
            elif 'ROUTE UPDATING' in key:
                counters['DHCP ROUTE UPDATING IA-NA Sessions']  = value
                counters['DHCP ROUTE UPDATING IA-PD Sessions']  = value2
            elif 'BOUND' in key:
                counters['DHCP BOUND IA-NA Sessions']  = value
                counters['DHCP BOUND IA-PD Sessions']  = value2
    return counters     
def show_ipsla_statistics_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show ipsla statistics
    #Each line being an item in a list
    sh_cmd = {}
    regex_operation = re.compile('Entry number: (\S+)')
    regex_operation_state = re.compile('Operational state of entry    : (\S+)')
    regex_operation_return_code = re.compile('Latest operation return code  : (\S+)')
    for line in file:
        match = regex_operation.search(line)
        match2 = regex_operation_state.search(line)
        match3 = regex_operation_return_code.search(line)
        if match:
            operation = match.group(1)
            sh_cmd[operation] = {}
        elif match2:
            state = match2.group(1)
            sh_cmd[operation]['State'] = state
        elif match3:
            return_code = match3.group(1)
            sh_cmd[operation]['Return Code'] = return_code
    return sh_cmd
def show_ipsla_statistics_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show ipsla statistics
    #Each line being an item in a list
    counters = {'IPSLA Total Sessions': 0, 'IPSLA State Active': 0, 'IPSLA State Other': 0, 'IPSLA Return Code OK': 0, 'IPSLA Return Code Other': 0}
    for key in sh_cmd_dict:
        counters['IPSLA Total Sessions'] += 1
        state = sh_cmd_dict[key]['State']
        return_code = sh_cmd_dict[key]['Return Code']
        if state:
            if state == 'Active':
                counters['IPSLA State Active'] += 1
            else:
                counters['IPSLA State Other'] += 1
        if return_code:
            if return_code == 'OK':
                counters['IPSLA Return Code OK'] += 1
            else:
                counters['IPSLA Return Code Other'] += 1
    return counters     
####################
#CRS PD            #
####################
def crs_admin_show_controller_fabric_plane_all_detail_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric plane all detail
    #Each line being an item in a list
    #Determine plane state
    sh_cmd = {}
    regex = re.compile('(\d)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+')
    regex2 = re.compile('(\d)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+')
    found_group = False
    for line in file:
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
def crs_admin_show_controller_fabric_plane_all_detail_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
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
def admin_show_controller_fabric_link_health_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric link health
    #Determine link status
    sh_cmd = {}
    regex = re.compile('(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+(\d)\s+(\S+)')
    found_group = False
    found_group2 = False
    for line in file:
        #logger.debug("show int line is: " + line)
        if "Mismatched Link detail" in line:
            found_group2 = True
            continue
        if found_group2:
            if '---------------------------------------------------------------------------' in line:
                found_group = True
                continue
        if found_group:
            match = regex.search(line)
            if match:
                if match.group(4) not in sh_cmd.keys():
                    sh_cmd[match.group(4)] = {}
                sh_cmd[match.group(4)]['Sfe Port ' + match.group(1) + ' remote ' + match.group(5) + ' In State: '] = match.group(2) + ' ' + match.group(3)
    return sh_cmd   
def admin_show_controller_fabric_link_health_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric plane link health
    #Determine how many planes are affected, how many links are down, and how many are hard down
    counters = {'Total Planes With Down Links': 0, 'Total Links Down': 0, 'Total Links Oper DN/DN': 0}
    regex_string = re.compile('UP\/UP DN\/DN')
    for key in sh_cmd_dict:
        counters['Total Planes With Down Links'] += 1
        for value in sh_cmd_dict[key]:
            counters['Total Links Down'] +=1
            if value ==  'UP/UP DN/DN':
                counters['Total Links Oper DN/DN'] +=1
    return counters
####################
#ASR9K PD          #
####################
def show_subscriber_session_all_summary_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show subscriber session all summary
    #Each line being an item in a list
    sh_cmd = {}
    regex_initializing = re.compile('initializing\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_connecting = re.compile('^\s+connecting\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_connected = re.compile('connected\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_activated = re.compile('activated\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_idle = re.compile('idle\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_disconneciting = re.compile('disconnecting\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_end = re.compile('end\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_in_progress = re.compile('in progress\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_ipv4 = re.compile('ipv4-only\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_ipv6 = re.compile('ipv6-only\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_dual_partial = re.compile('dual-partial-up\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_dual = re.compile('dual-up\s+(\S+)\s+(\S+)\s+(\S+)')
    regex_lac = re.compile('lac\s+(\S+)\s+(\S+)\s+(\S+)')
    for line in file:
        match = regex_initializing.search(line)
        match2 = regex_connecting.search(line)
        match3 = regex_connected.search(line)
        match4 = regex_activated.search(line)
        match5 = regex_idle.search(line)
        match6 = regex_disconneciting.search(line)
        match7 = regex_end.search(line)
        match8 = regex_in_progress.search(line)
        match9 = regex_ipv4.search(line)
        match10 = regex_ipv4.search(line)
        match11 = regex_ipv6.search(line)
        match12 = regex_dual_partial.search(line)
        match13 = regex_lac.search(line)
        if match:
            sh_cmd['initializing'] = {}
            sh_cmd['initializing']['PPPoE'] = match.group(1)
            sh_cmd['initializing']['IPSubDHCP'] = match.group(2)
            sh_cmd['initializing']['IPSubPKT'] = match.group(3)
        elif match2:
            sh_cmd['connecting'] = {}
            sh_cmd['connecting']['PPPoE'] = match2.group(1)
            sh_cmd['connecting']['IPSubDHCP'] = match2.group(2)
            sh_cmd['connecting']['IPSubPKT'] = match2.group(3)
        elif match3:
            sh_cmd['connected'] = {}
            sh_cmd['connected']['PPPoE'] = match3.group(1)
            sh_cmd['connected']['IPSubDHCP'] = match3.group(2)
            sh_cmd['connected']['IPSubPKT'] = match3.group(3)
        elif match4:
            sh_cmd['activated'] = {}
            sh_cmd['activated']['PPPoE'] = match4.group(1)
            sh_cmd['activated']['IPSubDHCP'] = match4.group(2)
            sh_cmd['activated']['IPSubPKT'] = match4.group(3)
        elif match5:
            sh_cmd['idle'] = {}
            sh_cmd['idle']['PPPoE'] = match5.group(1)
            sh_cmd['idle']['IPSubDHCP'] = match5.group(2)
            sh_cmd['idle']['IPSubPKT'] = match5.group(3)
        elif match6:
            sh_cmd['disconnecting'] = {}
            sh_cmd['disconnecting']['PPPoE'] = match6.group(1)
            sh_cmd['disconnecting']['IPSubDHCP'] = match6.group(2)
            sh_cmd['disconnecting']['IPSubPKT'] = match6.group(3)
        elif match7:
            sh_cmd['end'] = {}
            sh_cmd['end']['PPPoE'] = match7.group(1)
            sh_cmd['end']['IPSubDHCP'] = match7.group(2)
            sh_cmd['end']['IPSubPKT'] = match7.group(3)
        elif match8:
            sh_cmd['in progress'] = {}
            sh_cmd['in progress']['PPPoE'] = match8.group(1)
            sh_cmd['in progress']['IPSubDHCP'] = match8.group(2)
            sh_cmd['in progress']['IPSubPKT'] = match8.group(3)
        elif match9:
            sh_cmd['ipv4-only'] = {}
            sh_cmd['ipv4-only']['PPPoE'] = match9.group(1)
            sh_cmd['ipv4-only']['IPSubDHCP'] = match9.group(2)
            sh_cmd['ipv4-only']['IPSubPKT'] = match9.group(3)
        elif match10:
            sh_cmd['ipv6-only'] = {}
            sh_cmd['ipv6-only']['PPPoE'] = match10.group(1)
            sh_cmd['ipv6-only']['IPSubDHCP'] = match10.group(2)
            sh_cmd['ipv6-only']['IPSubPKT'] = match10.group(3)
        elif match11:
            sh_cmd['dual-partial-up'] = {}
            sh_cmd['dual-partial-up']['PPPoE'] = match11.group(1)
            sh_cmd['dual-partial-up']['IPSubDHCP'] = match11.group(2)
            sh_cmd['dual-partial-up']['IPSubPKT'] = match11.group(3)
        elif match12:
            sh_cmd['dual-up'] = {}
            sh_cmd['dual-up']['PPPoE'] = match12.group(1)
            sh_cmd['dual-up']['IPSubDHCP'] = match12.group(2)
            sh_cmd['dual-up']['IPSubPKT'] = match12.group(3)
        elif match13:
            sh_cmd['lac'] = {}
            sh_cmd['lac']['PPPoE'] = match13.group(1)
            sh_cmd['lac']['IPSubDHCP'] = match13.group(2)
            sh_cmd['lac']['IPSubPKT'] = match13.group(3)
    return sh_cmd
def show_subscriber_session_all_summary_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.3"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show subscriber session all summary
    #Each line being an item in a list
    #Determine if sessions changed
    counters = {'initializing PPPoE': 0, 'initializing IPSubDHCP': 0, 'initializing IPSubPKT': 0, 'connecting PPPoE': 0, 'connecting IPSubDHCP': 0, 'connecting IPSubPKT': 0, 'connected PPPoE': 0, 'connected IPSubDHCP': 0, 'connected IPSubPKT': 0,
                'activated PPPoE': 0, 'activated IPSubDHCP': 0, 'activated IPSubPKT': 0, 'idle PPPoE': 0, 'idle IPSubDHCP': 0, 'idle IPSubPKT': 0, 'disconnecting PPPoE': 0, 'disconnecting IPSubDHCP': 0, 'disconnecting IPSubPKT': 0,
                'end PPPoE': 0, 'end IPSubDHCP': 0, 'end IPSubPKT': 0, 'in progress PPPoE': 0, 'in progress IPSubDHCP': 0, 'in progress IPSubPKT': 0, 'ipv4-only PPPoE': 0, 'ipv4-only IPSubDHCP': 0, 'ipv4-only IPSubPKT': 0,
                'ipv6-only PPPoE': 0, 'ipv6-only IPSubDHCP': 0, 'ipv6-only IPSubPKT': 0, 'dual-partial-up PPPoE': 0, 'dual-partial-up IPSubDHCP': 0, 'dual-partial-up IPSubPKT': 0, 'dual-up PPPoE': 0, 'dual-up IPSubDHCP': 0, 'dual-up IPSubPKT': 0,
                'lac PPPoE': 0, 'lac IPSubDHCP': 0, 'lac IPSubPKT': 0,}
    for key in sh_cmd_dict:
        for key2 in sh_cmd_dict[key]:
            if key == 'initializing':
                if key2 == 'PPPoE':
                    counters['initializing PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['initializing IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['initializing IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'connecting':
                if key2 == 'PPPoE':
                    counters['connecting PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['connecting IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['connecting IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'connected':
                if key2 == 'PPPoE':
                    counters['connected PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['connected IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['connected IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'activated':
                if key2 == 'PPPoE':
                    counters['activated PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['activated IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['activated IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'idle':
                if key2 == 'PPPoE':
                    counters['idle PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['idle IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['idle IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'disconnecting':
                if key2 == 'PPPoE':
                    counters['disconnecting PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['disconnecting IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['disconnecting IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'end':
                if key2 == 'PPPoE':
                    counters['end PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['end IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['end IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'in progress':
                if key2 == 'PPPoE':
                    counters['in progress PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['in progress IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['in progress IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'ipv4-only':
                if key2 == 'PPPoE':
                    counters['ipv4-only PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['ipv4-only IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['ipv4-only IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'ipv6-only':
                if key2 == 'PPPoE':
                    counters['ipv6-only PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['ipv6-only IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['ipv6-only IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'dual-partial-up':
                if key2 == 'PPPoE':
                    counters['dual-partial-up PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['dual-partial-up IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['dual-partial-up IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'dual-up':
                if key2 == 'PPPoE':
                    counters['dual-up PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['dual-up IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['dual-up IPSubPKT'] = sh_cmd_dict[key][key2]
            elif key == 'lac':
                if key2 == 'PPPoE':
                    counters['lac PPPoE'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubDHCP':
                    counters['lac IPSubDHCP'] = sh_cmd_dict[key][key2]
                elif key2 == 'IPSubPKT':
                    counters['lac IPSubPKT'] = sh_cmd_dict[key][key2]
    return counters
def show_pfm_loc_all_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show pfm loc all
    #Each line being an item in a list
    #Determine alarm state
    sh_cmd = {}
    found_node = False
    regex_node = re.compile('node:\s(\S+)')
    regex_string = re.compile('(\w+\s)?(\w+\s+\d+\s+\d+\:\d+\:\d+)(\s\d+)?(\|--\||\|\d+\s?\|)(\S+)(\|)?.*\|(\S+).*\|\S+.*\|\S+.*\|(0x\S+)')
    regex2 = re.compile('(\w+\s)?(\w+\s+\d+\s+\d+\:\d+\:\d+)(\s\d+)?(\|--\||\|\d+\s?\|)(\S+)')
    for line in file:
        match = regex_node.search(line)
        if match:
            found_node = True
            node = match.group(1)
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
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show pfm loc all
    #Each line being an item in a list
    #Determine alarm state
    counters = {'Total Nodes': 0, 'Total Alarms': 0, 'Total Emergency/Alert alarms': 0, 'Total Critical Alarms': 0, 'Total Error Alarms': 0}
    for key in sh_cmd_dict:
        counters['Total Nodes'] += 1
        for value in sh_cmd_dict[key]:
            if "NO" not in sh_cmd_dict[key][value]:
                counters['Total Alarms'] += 1
                if "E/A" in sh_cmd_dict[key][value]:
                    counters['Total Emergency/Alert alarms'] += 1
                if "CR" in sh_cmd_dict[key][value]:
                    counters['Total Critical Alarms'] += 1
                if "ER" in sh_cmd_dict[key][value]:
                    counters['Total Error Alarms'] += 1 
    return counters
####################
#NCS5500 PD        #
####################
def show_controllers_npu_resources_all_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show controllers npu resources all loc all
    #Each line being an item in a list
    #Determine NPU resources
    sh_cmd = {}
    found_location = False
    current_usage = False
    OOR_found = False
    total_found = False
    regex_location = re.compile('HW Resource Information For Location: (\d\/\d+\/CPU0)')
    regex_name = re.compile('Name\s+:\s(\S+)')
    regex_npu = re.compile('NPU-(\d+)')
    regex_oor_state = re.compile('OOR State\s+:\s(\S+)')
    regex_total_inuse = re.compile('Total In-Use\s+:\s(\d+)')
    for line in file:
        match = regex_location.search(line)
        match2 = regex_name.search(line)
        match3 = regex_npu.search(line)
        match4 = regex_oor_state.search(line)
        match5 = regex_total_inuse.search(line)
        if match:
            found_location = True
            location = match.group(1)
            sh_cmd[location] = {}
        elif match2:
            if total_found == True:
                sh_cmd[location][found_memory + ' ' + npu + ' Total In-Use'] = total
            found_memory = match2.group(1)
            current_usage = False
            OOR_found = False
            total_found = False
        elif match3 and current_usage == False:
            if OOR_found == True:
                sh_cmd[location][found_memory + ' ' + npu + ' OOR State'] = OOR_state
            npu = match3.group(1)
        elif match4:
            OOR_found = True
            OOR_state = match4.group(1)
        elif 'Current Usage' in line:
            current_usage = True
            sh_cmd[location][found_memory + ' ' + npu + ' OOR State'] = OOR_state
        #elif match3 and current_usage == True:
            #if total_found == True:
                #sh_cmd[location][found_memory + ' ' + npu + ' Total In-Use'] = total
            #npu = match3.group(1)
        elif match5:
            total_found = True
            total = match5.group(1)
            sh_cmd[location][found_memory + ' ' + npu + ' Total In-Use'] = total
    return sh_cmd
def show_controllers_npu_resources_all_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show controllers npu resources all loc all
    #Each line being an item in a list
    #Determine NPU OOR Status
    counters = {'lem Green State': 0, 'lem Other State': 0, 'lpm Green State': 0, 'lpm Other State': 0, 'encap Green State': 0, 'encap Other State': 0,
                'fec Green State': 0, 'fec Other State': 0, 'ecmp_fec Green State': 0, 'ecmp_fec Other State': 0}
    for key in sh_cmd_dict:
        for value in sh_cmd_dict[key]:
            if 'Total' not in value:
                if 'lem' in value:
                    if 'Green' in sh_cmd_dict[key][value]:
                        counters['lem Green State'] += 1
                    else:
                        counters['lem Other State'] += 1
                elif 'lpm' in value:
                    if 'Green' in sh_cmd_dict[key][value]:
                        counters['lpm Green State'] += 1
                    else:
                        counters['lpm Other State'] += 1
                elif 'encap' in value:
                    if 'Green' in sh_cmd_dict[key][value]:
                        counters['encap Green State'] += 1
                    else:
                        counters['encap Other State'] += 1
                elif 'ecmp_fec' in value:
                    if 'Green' in sh_cmd_dict[key][value]:
                        counters['ecmp_fec Green State'] += 1
                    else:
                        counters['ecmp_fec Other State'] += 1
                elif 'fec' in value:
                    if 'Green' in sh_cmd_dict[key][value]:
                        counters['fec Green State'] += 1
                    else:
                        counters['fec Other State'] += 1
    return counters
def show_controllers_fia_diag_alloc_all_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.1"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for show controllers fia diagshell 0 "diag alloc all" location all
    #Each line being an item in a list
    #Determine resource allocation
    sh_cmd = {}
    found_location = False
    regex_node = re.compile('Node ID: (\d\/\d+\/CPU0)')
    regex_string = re.compile('^(\^M)?\s(.*\S+)\s+Total number of entries: (\d+)\s+Used entries (\d+).*$')
    current_usage = False
    OOR_found = False
    total_found = False
    for line in file:
        match = regex_node.search(line)
        if match:
            found_location = True
            location = match.group(1)
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
#NCS6K PD          #
####################
def ncs6k_admin_show_controller_fabric_plane_all_detail_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric plane all detail
    #Each line being an item in a list
    #Determine plane state
    sh_cmd = {}
    regex = re.compile('(\d)\s+(\S+)\s+(\S+)\s+\S+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
    found_group = False
    for line in file:
        if "-----------------" in line:
            found_group = True
            continue
        elif found_group:
            match = regex.search(line)
            if match:
                sh_cmd[match.group(1)] = {}
                sh_cmd[match.group(1)]['Admin/Plane State'] = match.group(2) + ' ' + match.group(3)
                sh_cmd[match.group(1)]['Total Bundles'] = match.group(6)
                sh_cmd[match.group(1)]['Down Bundles'] = match.group(7)
    return sh_cmd
def ncs6k_admin_show_controller_fabric_plane_all_detail_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric plane all detail
    #Each line being an item in a list
    #Determine Oper State and Bundle States
    counters = {'Total Planes': 0, 'Total Planes in UP UP State': 0, 'Total Planes in Any Other State': 0, 'Total Bundles': 0, 'Total Bundles Down': 0}
    for key in sh_cmd_dict:
        counters['Total Planes'] += 1
        if sh_cmd_dict[key]['Admin/Plane State'] == 'UP UP':
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
def admin_show_controller_fabric_link_port_compare(file):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric link port <>
    #Determine how many links are down or mismatched
    sh_cmd = {}
    found_links = False
    regex_string = re.compile('^\S+')
    for line in file:
        if '------------------' in line:
            found_links = True
            sh_cmd[link] = {}
        elif found_links == True:
            match = regex_string.search(line)
            if match:
                sh_cmd[link][str(match.group(1))] = str(match.group(2))
    return sh_cmd
def admin_show_controller_fabric_link_port_totals(sh_cmd_dict):
    ###__author__     = "Sam Milstead"
    ###__copyright__  = "Copyright 2020 (C) Cisco TAC"
    ###__version__    = "1.1.0"
    ###__status__     = "alpha"
    #Perform some magic on the pre and post lines of output for admin show controller fabric link port <>
    #Determine how many links are not good
    counters = {'Total Links Not Good': 0}
    for key in sh_cmd_dict:
        counters['Total Links Not Good'] += 1
    return counters



####################
#call main task    #
####################
if __name__ == '__main__':
    task()