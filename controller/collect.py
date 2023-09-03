import os
import time
import socket
import threading
from array import array
from re import ASCII 
import random
import dotenv

 
def check_monitors(monitors: str):
    """
    Shuts down the systemd services, if they are still running.
    Creates an array with the systemd services to activate for the 
    monitoring process.
    """
    try:
        array_monitors = monitors.split(",")
    except:
        print("Please use the correct format for monitors.")
        return
    active_services = []
    print("Stopping Services if they are still running...")
    os.system("systemctl stop RES.service > /dev/null")
    os.system("systemctl stop KERN.service > /dev/null")
    os.system("systemctl stop SYS.service > /dev/null")
    os.system("systemctl stop NET.service > /dev/null")
 #   os.system("systemctl stop FLSYS.service > /dev/null")
 #   os.system("systemctl stop IO.service > /dev/null")
    # Get all active services for new todo:
    for monitor in array_monitors:
        if monitor == "RES":
            active_services.append('RES.service')
        elif monitor == "KERN":
            active_services.append('KERN.service')
        elif monitor == "SYS":
            active_services.append('SYS.service')
        elif monitor == "NET":
            active_services.append('NET.service')
        elif monitor == "IO":
            active_services.append('IO.service')
        elif monitor == "FLSYS":
            active_services.append('FLSYS.service')
        else:
            print("You have entered an invalid monitor!")
            return
    return array_monitors, active_services
    
def wait_till_counter_starts(active_services: list):
    """
    Checks if data is available in the /tmp/monitor directory:
    """
    start_time = time.time()
    error = True
    while True:

        list_of_file_numbers = []

        # Check if the files are present in the directories:
        for service in active_services:
            monitor = service.split(".")[0]
            list_of_file_numbers.append(len(os.listdir("/tmp/monitors/{monitor}".format(monitor=monitor))))
      

        if time.time() - start_time > 60:
            print("You have been waiting for 60 seconds, there must be something wrong with your setup!")
            print("Stopping Services if they are still running...")
            os.system("systemctl stop RES.service > /dev/null")
            os.system("systemctl stop KERN.service > /dev/null")
            os.system("systemctl stop SYS.service > /dev/null")
            break

        # Checks if all numbers in the list_of_file_numbers are > 0:
        if all(x > 0 for x in list_of_file_numbers):
            error = False
            break
        else:
            time.sleep(1)
    
    return error

def send_data(server, services):
    """
    This sends the data to the server every 10 seconds
    """
    for service in services:
        monitor = service.split(".")[0]
        if monitor != "SYS":
            os.system("rsync -r /tmp/monitors/{monitor}/ {server}/{monitor} > /dev/null".format(monitor=monitor, server=server))


def check_services(services):
    """
    Checks if the services are still running and restarts them if they are not
    """
    for service in services:
        status = os.system('systemctl is-active --quiet {service}'.format(service=service))
        if status != 0:
            os.system("systemctl restart {service} > /dev/null".format(service=service))


def thread_work(server: str, active_services: array, total: int):
    """
    This is the thread that runs concurrently to the for loop
    1. It sends the data of monitor 10 seconds to the server
    2. It checks all 10 seconds if the services are still running and restarts them if needed
    """
    # Send data every hour:
    send_data(server, active_services)
    check_services(active_services)

    
def start_monitor(seconds: int, active_services: array, server: str):
    total = 0
    print("Please wait {seconds} seconds to start a new Monitoring Todo".format(seconds=seconds))
    for service in active_services:
        os.system("systemctl start {service} > /dev/null".format(service=service))
    # Wait to let all services properly start up:
    error = wait_till_counter_starts(active_services=active_services)
    if error:
        print("Error: Could not start all services!")
        return error
    start = time.perf_counter()
    while total < seconds:
        time.sleep(1)
        if total % 10 == 0 and total != 0:
            t1 = threading.Thread(target=thread_work, args=(server, active_services, total))
            t1.start()   
        total += 1
    finish = time.perf_counter()
    actual_running_time = round(finish-start, 2)
    print("Finished montioring for {total} seconds.".format(total=actual_running_time))
    for service in active_services:
        os.system("systemctl stop {service} > /dev/null".format(service=service))
    return error
    
 

    
def replace_env(server: str ,seconds: int):
    """
    Changes the environmental variables in SYS.env and 
    reloads the systemd service.
    """
    print(server)
    dotenv_file = dotenv.find_dotenv()
    print(dotenv_file)
    dotenv.load_dotenv(dotenv_file)
    os.environ["RSYNCF"] = "{}/SYS".format(server)
    os.environ["SECONDS"] = "{}\seconds".format(str(seconds))
    dotenv.set_key(dotenv_file, "RSYNCF", os.environ["RSYNCF"])
    dotenv.set_key(dotenv_file, "SECONDS", os.environ["SECONDS"])
    os.system("cp .env /etc/systemd/system/SYS.env")
    os.system("sudo systemctl daemon-reload")
    
    
def check_directories_on_device():
    """
    Creates the temporary directories to save the .csv/.log and .txt files if it does not exist
    """
    if os.path.exists("/tmp/monitors"):
        os.system("rm -rf /tmp/monitors")

    os.system("mkdir /tmp/monitors")
    os.system("mkdir /tmp/monitors/RES")
    os.system("mkdir /tmp/monitors/KERN")
    os.system("mkdir /tmp/monitors/SYS")
    os.system("mkdir /tmp/monitors/NET")
    os.system("mkdir /tmp/monitors/FLSYS")
    os.system("mkdir /tmp/monitors/IO")
    
     
def create_directories_server(mltype: str, monitors: array, server:str):
    """
    Creates the directories on the server.
    """
    server_arr = server.split(':')
    server_path = server_arr[1]
    server_ssh = server_arr[0]
   
    path = "{server_path}/{mltype}".format(server_path=server_path, mltype=mltype)
    
    for monitor in monitors:
        print(monitor)
        os.system("ssh {server_ssh} mkdir -p {path}/{monitor}".format(server_ssh=server_ssh, path=path, monitor=monitor))
    new_path = server_ssh + ":" + path
    return new_path
    

def send_delete(server, monitor):
    """
    Sends contents of the directory via rsync to the server and deletes all files in the directory
    """
    print("Sending data to server  for monitor {}...".format(monitor))
    os.system("rsync -vr /tmp/monitors/{monitor}/ {server}/{directory} > /dev/null".format(server=server, directory=monitor))
    print("Data sent to server and deleted from local directory")
    

def monitoring(duration, malware_type, monitors, server_path):
    arr_monitors, active_services = check_monitors(monitors)
    server = create_directories_server(malware_type, arr_monitors, server_path)
    check_directories_on_device()   
    replace_env(server,duration)
    print("Start monitoring and running for {seconds} seconds".format(seconds=duration))
    error = start_monitor(duration,active_services,server)
    if error:
        return
    for monitor in arr_monitors:
        send_delete(server,monitor)    
    return

if __name__ == "__main__":
    # Input parameters
    duration = input("Enter the time of monitoring in seconds(e.g., 60 seconds): ")
    malware_type = input("Enter the malware type (e.g., BASHLITE): ") 
    monitors = input("Enter the monitoring script to use (e.g., RES): ")
    server_path = input("Enter the server path (e.g., root@192.168.1.104:/root/data): ")
 
    monitoring(duration, malware_type, monitors, server_path)



