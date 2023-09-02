# Monitor Scripts 

## Differences between the monitors:
* Monitor 1: Monitors HPC and Ressource usage -> Created in a BA Thesis (5 seconds time window)
* Monitor 2: Also monitors HPC & Ressource usage -> Created by Dr.Huertas (5 seconds time window)
* Monitor 3: Monitors Systemcalls and is also part of a BA Thesis (10 seconds time window)

## Requirements:
1. You will need Python 3 (https://www.python.org/downloads/) and python-venv installed: `sudo apt install python3-venv` 
2. You will need to make the two shell scripts of monitor 1 & monitor 2 executable `sudo chmod + x ./example.sh`
3. For Monitor 1 please create a venv and install the requirements.txt if you want to run it as source
```
cd BA_Thesis_ds/monitors/monitor1
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
```

## Setup of the Monitors:
For each of these monitor scripts a different systemd service needs to be created: `m1,m2,m3`.
Sample service files can be found in the service folder of this repository. Please copy the contents in the following files:
* For monitor 1: `vim /etc/systemd/system/m1.service`
* For monitor 2: `vim /etc/systemd/system/m2.service`
* For monitor 3: `vim /etc/systemd/system/m3.service`

```
# For each newly added service:
sudo systemctl daemon-reload
# To test:
sudo systemctl start {m1,m2 or m3}.service
sudo systemctl stop {m1,m2 or m3}.service
```


