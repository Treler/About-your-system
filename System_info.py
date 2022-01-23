import os
import socket
import GPUtil
import psutil
import platform
import speedtest
from time import asctime
from requests import get


def system_values():
    new = dict()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    public_ip = get('http://api.ipify.org').text
    new["System"] = platform.system()
    new["System release"] = platform.release()
    new["System full"] = platform.platform()
    new["System time"] = asctime()
    users = psutil.users()
    for i in range(len(users)):
        new[f"User{i}"] = f"{users[i].name} {round(users[i].started / 60 / 60 / 24)} days"
    new["IP-public"] = public_ip
    new["IP-local"] = local_ip
    disks = psutil.disk_partitions()
    for i in range(len(disks)):
        new[f"Disk{i}"] = f"{disks[i].device} {round(psutil.disk_usage(disks[i].device).total / 1024 / 1024 / 1024)} GB"
    new["RAM"] = str(round(psutil.virtual_memory().total / 1024 / 1024 / 1024)) + " GB"
    new["CPU name"] = platform.processor()
    new["Cores count"] = psutil.cpu_count()
    gpus = GPUtil.getGPUs()
    for i in range(len(gpus)):
        new[f"GPU{i}"] = f"{gpus[i].name}"
        new[f"GPU{i} memory"] = f"{round(gpus[i].memoryTotal)} GB"
    test = speedtest.Speedtest()
    download = round(test.download() / 1024 / 1024 / 8)
    upload = round(test.upload() / 1024 / 1024 / 8)
    new["Inet speed down"] = str(download) + " MB/s"
    new["Inet speed upl"] = str(upload) + " MB/s"
    new["Battery charge"] = psutil.sensors_battery()

    return new


def write_data_to_file():
    data = system_values()
    path_to_temp = ""
    system_name = platform.system()
    main_disk = os.environ['HOMEDRIVE']

    if system_name == "Windows":
        path_to_temp = f"{main_disk}\\Users\\{os.getlogin()}\\AppData\\Local\\Temp\\System info.txt"

    if system_name == "Linux":
        path_to_temp = "/tmp/System info.txt"

    if system_name == "Darwin":
        path_to_temp = "/Library/Caches/TemporaryItems/System info.txt"

    with open(path_to_temp, "w", encoding="utf-8") as txt:
        for i in data.keys():
            txt.write(f"{i}: {data[i]}" + "\n")
    os.startfile(path_to_temp)


write_data_to_file()
