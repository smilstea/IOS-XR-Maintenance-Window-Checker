
**About**
<br>
IOS XR Maintenance Window Checker is a collection of scripts used to gather data from an IOS XR router multiple times and in a deterministic way find the differences and output any changes in a simple to read manner.

**Installation Notes**

<br>

Scripts were written and tested using python 3.6.8

<br>

No installation is required or compiling of the scripts, only requirement is python 3 with following libraries:
- pexpect
- os
- sys
- getpass
- re
<br>
In addition if telnet is the method of transport the telnet package on your system must be installed (not just the pexpect package).

<br>
<br>

**Running the Scripts**

<br>

To call the scripts make sure their permissions are set to executable then call them like so (telnet is default for gatherer):

python ios_xr_mw_gatherer.py --file pre_mw_file --ipv4addr 172.18.120.188 --username smilstea --ssh

python ios_xr_mw_gatherer.py --file post_mw_file --ipv4addr 172.18.120.188 --username smilstea --ssh

python ios_xr_mw_comparer.py --pre pre_mw_file --post post_mw_file --compare comparison_filename

<br>

Syntax for each file is below:

Usage: python ios_xr_mw_gatherer.py [--file <filename>][--ipv4addr <ipv4 address>][--username <username>](--ssh)(--timeout <seconds>) (--vsm)
  
Usage: python ios_xr_mw_comparer.py [--pre <filename>|--post <filename>][--compare <filename>](--minimal)(--vsm)

<br>

**Special Keywords**
  
<br>
  
--timeout
Specifies the timeout from commands, by default this is 10s for a few reasons.
1. Because some commands may not output immediately
2. Some commands pause mid-way through output
3. General delay in getting data output
This allows for the collection of outputs properly as they are generated and a pause in case a command does not output immediately, pauses, or python catches up to the end of the available data
Using this keyword and changing the timeout is NOT recommended unless a command is taking longer than 10s to complete.

 <br>
 
--vsm
Specifies to get ASR9K VSM specific outputs, without this option no VSM commands will be run

 <br>
  
--minimal
Reduces the output of the comparer script so that only WARNING messages are output on the terminal and only a summary view like without this keyword are printed to the compare file.
Without minimal a summary of all commands whether there is an alarm raised or not will be printed, and in the compare file a full dump of all the 'relevant' data used for comparions which is very verbose

 <br>

**Output**

<br>
  
Some output will be displayed on the screen, but this is kept to a minimum, only displaying differences or a summary for each command.
Outfiles will have the full outputs.

<br>

**Bugs / Enhancements / etc**

<br>

Contact smilstea@cisco.com for any issues, please include terminal logs and the output files for faster debugging.

<br>
  
Don't see a feature or command you want in this tool, contact smilstea@cisco.com preferably with examples.
