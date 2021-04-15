from core import *

DATA = {
    "env": os.environ.copy(),
    "os_type": SYSTEM.system,
    "os_release": SYSTEM.release,
    "os_ver": SYSTEM.version,
    "arc": SYSTEM.machine,
    "processor": SYSTEM.processor,
    "cpu_info": CPU_INFO,
    "gpu_info": GPU_INFO,
    "user": getpass.getuser(),
    "host": socket.gethostname(),
    "memory": MEMORY_INFO,
    "disk_info": DISK_INFO,
    "time_n": datetime.datetime.today().ctime(),
    "browser": webbrowser.get().name,
    "connected": connected(),
    "interfaces": INTERFACE_INFO,
    "boot_time": f"{boot_time.year}/{boot_time.month}/{boot_time.day} {boot_time.hour}:{boot_time.minute}:{boot_time.second}",
    "network": NET_INFO
}

print(json.dumps(DATA, indent=2))
