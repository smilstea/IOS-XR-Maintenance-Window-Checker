=========================
Installation Notes
=========================
Scripts were written and tested using python 3.6.8

No installation is required or compiling of the scripts, only requirement is python 3 with following libraries:
- pexpect
- os
- sys
- getpass
- re

In addition if telnet is the method of transport the telnet package on your system must be installed (not just the pexpect package).


=========================
Running the Scripts
=========================
To call the scripts make sure their permissions are set to executable then call them like so (telnet is default for gatherer):
python ios_xr_mw_gatherer.py --file pre_mw_file --ipv4addr 172.18.120.188 --username smilstea --ssh
python ios_xr_mw_gatherer.py --file post_mw_file --ipv4addr 172.18.120.188 --username smilstea --ssh
python ios_xr_mw_comparer.py --pre pre_mw_file --post post_mw_file --compare comparison_filename

Syntax for each file is below:
Usage: python ios_xr_mw_gatherer.py [--file <filename>][--ipv4addr <ipv4 address>][--username <username>]{--ssh}
Usage: python ios_xr_mw_comparer.py [--pre <filename>|--post <filename>][--compare <filename>]

=======================
Output
=======================
Some output will be displayed on the screen, but this is kept to a minimum, only displaying differences or a summary for each command.
Outfiles will have the full outputs.

=========================
Bugs / Enhancements / etc
=========================
Contact smilstea@cisco.com for any issues, please include terminal logs and the output files for faster debugging.

Don't see a feature or command you want in this tool, contact smilstea@cisco.com preferably with examples.
