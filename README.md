# MP
Creation of New Datasets for Decentralized Federated Learning
# File structure
* /controller: Directory containing the control script to run monitoring scripts
* /monitors: Directory containing the monitoring scripts (RES, KERN, SYS, NET, FLSYS, IO)
* /server: Directory containing the listeners for data transmission (run on the server side)
* install_source.sh: File to install all needed dependencies
# Differences between the monitors:
* KERN: Monitors HPC and Ressource usage -> Provided by Dr.Huertas and Dr.Feng (5 seconds time window)
* RES: Also monitors HPC & Ressource usage -> Provided by Dr.Huertas and Dr.Feng (5 seconds time window)
* SYS: Monitors Systemcalls -> Provided by Dr.Huertas and Dr.Feng (10 seconds time window)
* NET: Monitors events coming from the network (5 seconds time window)
* IO_block: Monitors events coming from the input/output (10 seconds time window)
* IO_entropy: Calculate the entropy from the input/output (10 seconds time window)
* FLSYS: Monitors events coming from the file system (5 seconds time window)
# Prerequisite:
You will need to enable SSH on your main machine:

`sudo apt-get install openssh-server`

`sudo systemctl enable ssh`

`sudo systemctl start ssh`

`pip3 install scapy, requests`

`sudo apt-get install sysstat`

# Malware samples:
* Botnet: Bashlite
* Backdoor: HttpBackdoor, Backdoor, The Tick
* Ransomware: Ransomware‐PoC
* Cryptojacker: Linux.MulDrop.14
* Rootkits: Beurk, Bdvl

See the wike page (https://github.com/JingHan0724/MP/wiki) for installation guidance.
# Installation:

`sudo apt install git`

`git clone https://github.com/JingHan0724/MP.git`

`cd MP`

`chmod +x install_source.sh`

`./install_source.sh -s username@desktopipaddress`

# Collecting data:
(1) Server side (your personal computer):

Adjust the listening scripts to utilize your specific IP address and designate a data directory of your choice. Then execute the data transmission scripts.

(2) Client side (Raspberry Pi):

`cd controller`

`source env/bin/activate`

`python3 collect.py`

