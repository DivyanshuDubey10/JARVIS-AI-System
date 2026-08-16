import psutil
import shutil
import platform 

class SystemInfoHandler:
    def handle(self, command):
        query = command.raw_text.lower()
        
        if "cpu" in query and (
            "usage" in query or
            "load" in query
        ):
            usage = psutil.cpu_percent(interval=1)
            return f"CPU usage is {usage:.0f} percent."
        
        if "ram" in query or "memory" in query:
            memory = psutil.virtual_memory()
            
            total = memory.total / (1024 ** 3)
            used = memory.used / (1024 ** 3)
            
            return (
                f"You have {total:.1f} gigabytes of RAM, "
                f"with {used:.1f} gigabytes currently in use."
            )
            
        if ("storage" in query
            or "disk space" in query
            or "free space" in query
        ):
            disk = shutil.disk_usage("C:\\")

            total = disk.total / (1024 ** 3)
            free = disk.free / (1024 ** 3)

            return (
                f"Your C drive has {total:.0f} gigabytes of total storage "
                f"with {free:.0f} gigabytes free."
            )

        # Battery
        if "battery" in query:

            battery = psutil.sensors_battery()

            if battery is None:
                return "I couldn't detect a battery."

            percent = battery.percent

            if battery.power_plugged:
                return f"Battery is at {percent:.0f} percent and charging."

            return f"Battery is at {percent:.0f} percent."

        # Operating system
        if (
            "operating system" in query
            or "windows version" in query
            or "os version" in query
        ):

            return f"You are running {platform.system()} {platform.release()}."

        return None