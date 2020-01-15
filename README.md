# IOS-XR-Maintenance-Window-Checker
a way to capture data from an IOS XR router and in a deterministic way find the differences and output any changes in a simple to read manner


===
Installation Notes
===
Scripts ios_xr_mw_gatherer.py and ios_xr_mw_comparer.py were written and tested using python 2.7.5

No installation is required or compiling of the scripts, only requirement is python 2.7.x with following libraries:
- paramiko
- telnetlib
- os
- time
- sys
- getpass
- re


===
Running the Scripts
===
To call the scripts make sure their permissions are set to executable then call them like so (telnet is default for gatherer):
python ios_xr_mw_gatherer.py --file pre_mw_file --ipv4addr 172.18.120.188 --username smilstea --ssh
python ios_xr_mw_gatherer.py --file post_mw_file --ipv4addr 172.18.120.188 --username smilstea --ssh
python ios_xr_mw_comparer.py --pre pre_mw_file --post post_mw_file --compare comparison_filename

Syntax for each file is below:
Usage: python ios_xr_mw_gatherer.py [--file <filename>][--ipv4addr <ipv4 address>][--username <username>]{--ssh}
Usage: python ios_xr_mw_comparer.py [--pre <filename>|--post <filename>][--compare <filename>]


===
Output
===
Some output will be displayed on the screen, but this is kept to a minimum, only displaying differences or a summary for each command.
Outfiles will have the full outputs.

===
Bugs / Enhancements / etc
===
Contact smilstea@cisco.com for any issues, please include terminal logs and the output files for faster debugging.

Don't see a feature or command you want in this tool, contact smilstea@cisco.com preferably with examples.
