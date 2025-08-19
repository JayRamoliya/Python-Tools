# import platform
# import psutil
# import shutil
# import speedtest
# import os

# # -------------------------
# # System Info Viewer
# # -------------------------
# def system_info():
#     print("===== 🖥️ System Information =====")
#     print(f"System: {platform.system()}")
#     print(f"Node Name: {platform.node()}")
#     print(f"Release: {platform.release()}")
#     print(f"Version: {platform.version()}")
#     print(f"Machine: {platform.machine()}")
#     print(f"Processor: {platform.processor()}")
#     print(f"CPU Cores (Physical): {psutil.cpu_count(logical=False)}")
#     print(f"CPU Cores (Logical): {psutil.cpu_count(logical=True)}")
#     print(f"Total RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
#     print()

# # -------------------------
# # Battery Percentage Checker
# # -------------------------
# def battery_info():
#     print("===== 🔋 Battery Information =====")
#     battery = psutil.sensors_battery()
#     if battery:
#         print(f"Battery Percentage: {battery.percent}%")
#         print(f"Power Plugged In: {'Yes' if battery.power_plugged else 'No'}")
#         if not battery.power_plugged:
#             print(f"Time Left: {battery.secsleft // 60} minutes")
#     else:
#         print("No battery detected.")
#     print()

# # -------------------------
# # CPU & RAM Usage Monitor
# # -------------------------
# def usage_monitor():
#     print("===== 📊 CPU & RAM Usage =====")
#     print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
#     memory = psutil.virtual_memory()
#     print(f"RAM Usage: {memory.percent}% ({round(memory.used / (1024**3), 2)} GB / {round(memory.total / (1024**3), 2)} GB)")
#     print()

# # -------------------------
# # Disk Space Analyzer
# # -------------------------
# def disk_analyzer():
#     print("===== 💽 Disk Usage =====")
#     partitions = psutil.disk_partitions()
#     for partition in partitions:
#         try:
#             usage = psutil.disk_usage(partition.mountpoint)
#             print(f"Drive: {partition.device}")
#             print(f"  Mountpoint: {partition.mountpoint}")
#             print(f"  File system: {partition.fstype}")
#             print(f"  Total Size: {round(usage.total / (1024**3), 2)} GB")
#             print(f"  Used: {round(usage.used / (1024**3), 2)} GB")
#             print(f"  Free: {round(usage.free / (1024**3), 2)} GB")
#             print(f"  Usage: {usage.percent}%")
#             print("-" * 30)
#         except PermissionError:
#             continue
#     print()

# # -------------------------
# # Network Speed Test
# # -------------------------
# def network_speed_test():
#     print("===== 🌐 Network Speed Test =====")
#     st = speedtest.Speedtest()
#     st.get_best_server()
#     download = st.download() / 1_000_000  # Convert to Mbps
#     upload = st.upload() / 1_000_000
#     ping = st.results.ping
#     print(f"Download Speed: {download:.2f} Mbps")
#     print(f"Upload Speed: {upload:.2f} Mbps")
#     print(f"Ping: {ping:.2f} ms")
#     print()

# # -------------------------
# # Main Function
# # -------------------------
# if __name__ == "__main__":
#     system_info()
#     battery_info()
#     usage_monitor()
#     disk_analyzer()
#     network_speed_test()








import tkinter as tk
from tkinter import ttk, scrolledtext
import platform
import psutil
import speedtest
import threading

# -------------------------
# System Functions
# -------------------------
def get_system_info():
    info = []
    info.append("===== 🖥️ System Information =====")
    info.append(f"System: {platform.system()}")
    info.append(f"Node Name: {platform.node()}")
    info.append(f"Release: {platform.release()}")
    info.append(f"Version: {platform.version()}")
    info.append(f"Machine: {platform.machine()}")
    info.append(f"Processor: {platform.processor()}")
    info.append(f"CPU Cores (Physical): {psutil.cpu_count(logical=False)}")
    info.append(f"CPU Cores (Logical): {psutil.cpu_count(logical=True)}")
    info.append(f"Total RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    return "\n".join(info)

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return (f"===== 🔋 Battery Information =====\n"
                f"Battery Percentage: {battery.percent}%\n"
                f"Power Plugged In: {'Yes' if battery.power_plugged else 'No'}\n"
                f"{'Time Left: ' + str(battery.secsleft // 60) + ' minutes' if not battery.power_plugged else ''}")
    return "===== 🔋 Battery Information =====\nNo battery detected."

def get_usage_info():
    memory = psutil.virtual_memory()
    return (f"===== 📊 CPU & RAM Usage =====\n"
            f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n"
            f"RAM Usage: {memory.percent}% "
            f"({round(memory.used / (1024**3), 2)} GB / {round(memory.total / (1024**3), 2)} GB)")

def get_disk_info():
    info = ["===== 💽 Disk Usage ====="]
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            info.append(f"Drive: {partition.device}")
            info.append(f"  Total: {round(usage.total / (1024**3), 2)} GB")
            info.append(f"  Used: {round(usage.used / (1024**3), 2)} GB")
            info.append(f"  Free: {round(usage.free / (1024**3), 2)} GB")
            info.append(f"  Usage: {usage.percent}%")
            info.append("-" * 30)
        except PermissionError:
            continue
    return "\n".join(info)

def get_network_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    return (f"===== 🌐 Network Speed Test =====\n"
            f"Download Speed: {download:.2f} Mbps\n"
            f"Upload Speed: {upload:.2f} Mbps\n"
            f"Ping: {ping:.2f} ms")

# -------------------------
# GUI Functions
# -------------------------
def show_info(func):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, func())

def run_speedtest():
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Running speed test... Please wait ⏳")
    def task():
        result = get_network_speed()
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result)
    threading.Thread(target=task).start()

# -------------------------
# Tkinter UI Setup
# -------------------------
root = tk.Tk()
root.title("🖥️ System Info & Monitoring")
root.geometry("750x550")
root.config(bg="#1e1e2f")  # dark theme background

# Style
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                foreground="white",
                background="#007acc",
                padding=8)

style.map("TButton",
          background=[("active", "#005f99")])

title_label = tk.Label(root,
                       text="🖥️ System Info & Monitoring",
                       font=("Segoe UI", 16, "bold"),
                       bg="#1e1e2f",
                       fg="white")
title_label.pack(pady=10)

# Buttons Frame
frame = ttk.Frame(root)
frame.pack(pady=10)

btn1 = ttk.Button(frame, text="System Info", command=lambda: show_info(get_system_info))
btn2 = ttk.Button(frame, text="Battery Info", command=lambda: show_info(get_battery_info))
btn3 = ttk.Button(frame, text="CPU & RAM Usage", command=lambda: show_info(get_usage_info))
btn4 = ttk.Button(frame, text="Disk Info", command=lambda: show_info(get_disk_info))
btn5 = ttk.Button(frame, text="Network Speed Test", command=run_speedtest)

btn1.grid(row=0, column=0, padx=8, pady=8)
btn2.grid(row=0, column=1, padx=8, pady=8)
btn3.grid(row=0, column=2, padx=8, pady=8)
btn4.grid(row=1, column=0, padx=8, pady=8)
btn5.grid(row=1, column=1, padx=8, pady=8)

# Output Box
output_box = scrolledtext.ScrolledText(root,
                                       wrap=tk.WORD,
                                       width=85,
                                       height=20,
                                       font=("Consolas", 10),
                                       bg="#252526",
                                       fg="white",
                                       insertbackground="white")
output_box.pack(padx=10, pady=10)

root.mainloop()
