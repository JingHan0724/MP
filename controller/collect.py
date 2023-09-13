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
 #   os.system("systemctl stop RES.service > /dev/null")
    os.system("systemctl stop KERN.service > /dev/null")
 #   os.system("systemctl stop SYS.service > /dev/null")
    os.system("systemctl stop NET.service > /dev/null")
 #   os.system("systemctl stop FLSYS.service > /dev/null")
    os.system("systemctl stop BLOCK.service > /dev/null")
    os.system("systemctl stop ENTROPY.service > /dev/null")
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
        elif monitor == "BLOCK":
            active_services.append('BLOCK.service')
        elif monitor == "ENTROPY":
            active_services.append('ENTROPY.service')
        elif monitor == "FLSYS":
            active_services.append('FLSYS.service')
        else:
            print("You have entered an invalid monitor!")
            return
    return array_monitors, active_services


def check_services(services):
    """
    Checks if the services are still running and restarts them if they are not
    """
    for service in services:
        status = os.system('systemctl is-active --quiet {service}'.format(service=service))
        if status != 0:
            os.system("systemctl restart {service} > /dev/null".format(service=service))


def thread_work(active_services: array, total: int):
    """
    This is the thread that runs concurrently to the for loop
    1. It sends the data of monitor 10 seconds to the server
    2. It checks all 10 seconds if the services are still running and restarts them if needed
    """
    check_services(active_services)

    
def start_monitor(seconds: int, active_services: array):
    total = 0
    for service in active_services:
        os.system("systemctl start {service} > /dev/null".format(service=service))
    start = time.perf_counter()
    while total < int(seconds):
        time.sleep(1)
        if total % 10 == 0 and total != 0:
            t1 = threading.Thread(target=thread_work, args=(active_services, total))
            t1.start()   
        total += 1
    finish = time.perf_counter()
    actual_running_time = round(finish-start, 2)
    print("Finished montioring for {total} seconds.".format(total=actual_running_time))
    for service in active_services:
        os.system("systemctl stop {service} > /dev/null".format(service=service))
  

def monitoring(duration, monitors):
    arr_monitors, active_services = check_monitors(monitors)
    print("Start monitoring and running for {seconds} seconds".format(seconds=duration))
    start_monitor(duration,active_services)


if __name__ == "__main__":
    # Input parameters
    duration = input("Enter the time of monitoring in seconds(e.g., 60 seconds): ")
    monitors = input("Enter the monitoring script to use (e.g., RES): ")

    monitoring(duration, monitors)



