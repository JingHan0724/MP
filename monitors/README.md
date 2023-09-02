# Monitor Scripts 

## Differences between the monitors:
* KERN: Monitors HPC and Ressource usage -> Provided by Dr.Huertas and Dr.Feng (5 seconds time window)
* RES: Also monitors HPC & Ressource usage -> Provided by Dr.Huertas and Dr.Feng (5 seconds time window)
* SYS: Monitors Systemcalls -> Provided by Dr.Huertas and Dr.Feng (10 seconds time window)
* NET: Monitors events coming from the network (10 seconds time window)
* IO: Monitors events coming from the input/output (*** seconds time window)
* FLSYS: Monitors events coming from the file system (*** seconds time window)

## Requirements:
1. You will need Python 3 (https://www.python.org/downloads/) and python-venv installed: `sudo apt install python3-venv` 
2. You will need to make the shell scripts executable `sudo chmod + x ./***.sh`
3. For RES please create a venv and install the requirements.txt if you want to run it as source
```
cd MP/monitors/RES
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
```



