# MP
Creation of New Datasets for Decentralized Federated Learning
# File structure
* /monitors: Directory containing the monitoring scripts (RES, KERN, SYS, NET, FLSYS, IO).
* install_source.sh: File to install all needed dependencies
# Differences between the monitors:
* KERN: Monitors HPC and Ressource usage -> Provided by Dr.Huertas and Dr.Feng (5 seconds time window)
* RES: Also monitors HPC & Ressource usage -> Provided by Dr.Huertas and Dr.Feng (5 seconds time window)
* SYS: Monitors Systemcalls -> Provided by Dr.Huertas and Dr.Feng (10 seconds time window)
* NET: Monitors events coming from the network (10 seconds time window)
* IO: Monitors events coming from the input/output (10 seconds time window)
* FLSYS: Monitors events coming from the file system (*** seconds time window)
# Prerequisite:
You will need to enable SSH on your main machine:
* sudo apt-get install openssh-server
* sudo systemctl enable ssh
* sudo systemctl start ssh
# Malware samples:
See the wike page (https://github.com/JingHan0724/MP/wiki) for installation guidance.
# Installation:
* apt-get git
* git clone https://github.com/JingHan0724/MP.git
* cd MP
* chmod +x install_source.sh
* ./install_source.sh -s username@desktopipaddress
# Collecting data:
* cd controller
* source env/bin/activate
* python3 collect.py

