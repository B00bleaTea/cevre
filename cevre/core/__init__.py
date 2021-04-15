import os
import json
import getpass
import socket
import platform
import psutil
import datetime
import requests
import pathlib
import webbrowser
import urllib
import GPUtil

# * boot *#
boot_time = psutil.boot_time()
boot_time = datetime.datetime.fromtimestamp(boot_time)
########


# * cpu *#
CPU_INFO = {}
CPU_INFO["cores"] = {}
CPU_FREQ = psutil.cpu_freq()

CPU_INFO["max_freq"] = CPU_FREQ.max
CPU_INFO["min_freq"] = CPU_FREQ.min
CPU_INFO["freq"] = CPU_FREQ.current

CPU_INFO["total_cores"] = psutil.cpu_count(logical=True)
CPU_INFO["physical_cores"] = psutil.cpu_count(logical=False)

for core, usage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    CPU_INFO["cores"][f"core_{core}"] = usage
CPU_INFO["total"] = psutil.cpu_percent()
#########


# * disk *#
PARTITIONS = psutil.disk_partitions()
DISK_IO = psutil.disk_io_counters()
DISK_INFO = {}
for partition in PARTITIONS:
    DISK_INFO[partition.device] = {
        "mountpoint": partition.mountpoint,
        "fstype": partition.fstype
    }
    try:
        DISK_INFO[partition.device]["usage"] = {
            "total": psutil.disk_usage(partition.mountpoint).total >> 30,
            "available": psutil.disk_usage(partition.mountpoint).free >> 30,
            "used": psutil.disk_usage(partition.mountpoint).used >> 30,
            "used_%": psutil.disk_usage(partition.mountpoint).percent
        }
    except PermissionError:
        continue

DISK_INFO["read"] = DISK_IO.read_bytes >> 20
DISK_INFO["write"] = DISK_IO.write_bytes >> 20
#########


# * interfaces *#
IF_ADDR = psutil.net_if_addrs()
INTERFACE_INFO = {}
for interface_name, interface_addresses in IF_ADDR.items():
    for address in interface_addresses:
        INTERFACE_INFO[interface_name] = {}
        INTERFACE_INFO[interface_name]["ip"] = address.address
        INTERFACE_INFO[interface_name]["netmask"] = address.netmask
        INTERFACE_INFO[interface_name]["broadcast"] = address.broadcast
NET_IO = psutil.net_io_counters()
INTERFACE_INFO["sent"] = NET_IO.bytes_sent >> 20
INTERFACE_INFO["recv"] = NET_IO.bytes_recv >> 20
###############


# * GPUs *#
GPUS = GPUtil.getGPUs()
GPU_INFO = {}
for gpu in GPUS:
    GPU_INFO[gpu.name] = {
        "id": gpu.id,
        "load": gpu.load * 100,
        "temperature": gpu.temperature,
        "uuid": gpu.uuid,
        "memory": {
            "total": gpu.memoryTotal,
            "free": gpu.memoryFree,
            "used": gpu.memoryUsed
        }
    }
########


# * memory *#
MEMORY_INFO = {}
MEMORY_INFO["RAM"] = {
    "total": psutil.virtual_memory().total >> 20,
    "available": psutil.virtual_memory().available >> 20,
    "used": psutil.virtual_memory().used >> 20,
    "usage_%": psutil.virtual_memory().percent
}
MEMORY_INFO["swap"] = {
    "total": psutil.swap_memory().total >> 10,
    "available": psutil.swap_memory().free >> 10,
    "used": psutil.swap_memory().used >> 10,
    "usage_%": psutil.swap_memory().percent
}


#########


def connected():
    try:
        urllib.request.urlopen("https://google.com/")
        return True
    except Exception:
        return False


with open(pathlib.Path(os.path.abspath("core/config.json")), "r") as f:
    CONFIG = json.load(f)

SYSTEM = platform.uname()

# * network *#
if CONFIG["network"]:
    NET_INFO: dict = requests.get('https://ipinfo.io/').json()
    NET_INFO.pop("readme")
else:
    NET_INFO: None = None
############
