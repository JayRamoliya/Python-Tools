import tkinter as tk
from tkinter import messagebox
import time, threading, os, platform

BG_COLOR = "#f3f4f6"
PRIMARY_COLOR = "#4f46e5"
SECONDARY_COLOR = "#6366f1"
TEXT_COLOR = "#111827"
BTN_COLOR = "#4338ca"
BTN_HOVER = "#6366f1"
FONT = ("Segoe UI", 11)

class TimeProductivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⌛ Time & Productivity Toolkit")
        self.root.geometry("520x420")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)

        title = tk.Label(
            self.root,
            text="⌛ Time & Productivity Toolkit",
            font=("Segoe UI", 16, "bold"),
            fg=PRIMARY_COLOR,
            bg=BG_COLOR
        )
        title.pack(pady=20)

        self.container = tk.Frame(self.root, bg=BG_COLOR)
        self.container.pack(expand=True)

        # Create Stylish Buttons
        self.create_button("⏰ Alarm Clock", self.alarm_window)
        self.create_button("⏳ Countdown Timer", self.countdown_window)
        self.create_button("🍅 Pomodoro Timer", self.pomodoro_window)
        self.create_button("⏱️ Stopwatch", self.stopwatch_window)
        self.create_button("💻 Auto Shutdown / Restart", self.shutdown_window)

    def create_button(self, text, command):
        btn = tk.Button(
            self.container,
            text=text,
            font=FONT,
            bg=BTN_COLOR,
            fg="white",
            activebackground=BTN_HOVER,
            activeforeground="white",
            relief="flat",
            width=30,
            height=2,
            command=command
        )
        btn.pack(pady=8)

        # Add hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))

    # ---------------- Alarm Clock ----------------
    def alarm_window(self):
        win = self.create_popup("⏰ Alarm Clock")
        tk.Label(win, text="Set Time (HH:MM:SS)", font=FONT, bg="white").pack(pady=5)
        entry = tk.Entry(win, width=15, font=FONT)
        entry.pack(pady=5)

        def set_alarm():
            alarm_time = entry.get()
            def alarm_check():
                while True:
                    current = time.strftime("%H:%M:%S")
                    if current == alarm_time:
                        messagebox.showinfo("Alarm", "⏰ Time's up!")
                        break
                    time.sleep(1)
            threading.Thread(target=alarm_check, daemon=True).start()

        self.popup_button(win, "Set Alarm", set_alarm)

    # ---------------- Countdown Timer ----------------
    def countdown_window(self):
        win = self.create_popup("⏳ Countdown Timer")
        tk.Label(win, text="Enter seconds:", font=FONT, bg="white").pack(pady=5)
        entry = tk.Entry(win, width=15, font=FONT)
        entry.pack(pady=5)
        label = tk.Label(win, text="", font=("Segoe UI", 14, "bold"), bg="white", fg=PRIMARY_COLOR)
        label.pack(pady=10)

        def start_countdown():
            try:
                total = int(entry.get())
                def run():
                    nonlocal total
                    while total > 0:
                        mins, secs = divmod(total, 60)
                        label.config(text=f"{mins:02}:{secs:02}")
                        time.sleep(1)
                        total -= 1
                    label.config(text="⏳ Done!")
                    messagebox.showinfo("Countdown", "⏳ Countdown Finished!")
                threading.Thread(target=run, daemon=True).start()
            except:
                messagebox.showerror("Error", "Enter valid number")

        self.popup_button(win, "Start", start_countdown)

    # ---------------- Pomodoro Timer ----------------
    def pomodoro_window(self):
        win = self.create_popup("🍅 Pomodoro Timer")
        label = tk.Label(win, text="🍅 25:00", font=("Segoe UI", 18, "bold"), bg="white", fg=SECONDARY_COLOR)
        label.pack(pady=10)

        running = [False]

        def start_pomodoro():
            if running[0]:
                return
            running[0] = True
            def run():
                work_time = 25 * 60
                while work_time > 0 and running[0]:
                    mins, secs = divmod(work_time, 60)
                    label.config(text=f"🍅 {mins:02}:{secs:02}")
                    time.sleep(1)
                    work_time -= 1
                messagebox.showinfo("Pomodoro", "☕ Take a 5 min Break!")
                break_time = 5 * 60
                while break_time > 0 and running[0]:
                    mins, secs = divmod(break_time, 60)
                    label.config(text=f"☕ {mins:02}:{secs:02}")
                    time.sleep(1)
                    break_time -= 1
                label.config(text="✅ Pomodoro Finished")
                running[0] = False
            threading.Thread(target=run, daemon=True).start()

        def stop_pomodoro():
            running[0] = False
            label.config(text="🍅 25:00")

        self.popup_button(win, "Start", start_pomodoro)
        self.popup_button(win, "Stop", stop_pomodoro)

    # ---------------- Stopwatch ----------------
    def stopwatch_window(self):
        win = self.create_popup("⏱️ Stopwatch")
        label = tk.Label(win, text="00:00:00", font=("Segoe UI", 18, "bold"), bg="white", fg=PRIMARY_COLOR)
        label.pack(pady=10)

        running = [False]
        elapsed = [0]

        def update_time():
            while running[0]:
                time.sleep(1)
                elapsed[0] += 1
                h, rem = divmod(elapsed[0], 3600)
                m, s = divmod(rem, 60)
                label.config(text=f"{h:02}:{m:02}:{s:02}")

        def start():
            if not running[0]:
                running[0] = True
                threading.Thread(target=update_time, daemon=True).start()

        def stop():
            running[0] = False

        def reset():
            running[0] = False
            elapsed[0] = 0
            label.config(text="00:00:00")

        self.popup_button(win, "Start", start)
        self.popup_button(win, "Stop", stop)
        self.popup_button(win, "Reset", reset)

    # ---------------- Shutdown Scheduler ----------------
    def shutdown_window(self):
        win = self.create_popup("💻 Auto Shutdown / Restart")
        tk.Label(win, text="Enter minutes:", font=FONT, bg="white").pack(pady=5)
        entry = tk.Entry(win, width=15, font=FONT)
        entry.pack(pady=5)

        def shutdown():
            try:
                mins = int(entry.get())
                secs = mins * 60
                if platform.system() == "Windows":
                    os.system(f"shutdown /s /t {secs}")
                else:
                    os.system(f"shutdown -h +{mins}")
                messagebox.showinfo("Shutdown", f"PC will shutdown in {mins} minutes")
            except:
                messagebox.showerror("Error", "Invalid input")

        def restart():
            try:
                mins = int(entry.get())
                secs = mins * 60
                if platform.system() == "Windows":
                    os.system(f"shutdown /r /t {secs}")
                else:
                    os.system(f"shutdown -r +{mins}")
                messagebox.showinfo("Restart", f"PC will restart in {mins} minutes")
            except:
                messagebox.showerror("Error", "Invalid input")

        self.popup_button(win, "Shutdown", shutdown)
        self.popup_button(win, "Restart", restart)

    # ---------------- UI Helpers ----------------
    def create_popup(self, title):
        win = tk.Toplevel(self.root, bg="white")
        win.title(title)
        win.geometry("360x250")
        win.resizable(False, False)
        tk.Label(win, text=title, font=("Segoe UI", 14, "bold"), fg=PRIMARY_COLOR, bg="white").pack(pady=10)
        return win

    def popup_button(self, win, text, command):
        btn = tk.Button(
            win,
            text=text,
            font=FONT,
            bg=BTN_COLOR,
            fg="white",
            activebackground=BTN_HOVER,
            activeforeground="white",
            relief="flat",
            width=15,
            height=1,
            command=command
        )
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TimeProductivityApp(root)
    root.mainloop()
