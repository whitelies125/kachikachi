import os
import sys
import subprocess
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image
from pystray import Icon, Menu, MenuItem

from thread_manager import threadManager

class Tray:
    def __init__(self):
        self.plot_submenu = Menu(
            MenuItem("all", self.on_plot),
            MenuItem("today", self.on_plot),
            MenuItem("seven day", self.on_plot),
            MenuItem("this month", self.on_plot),
            MenuItem("this year", self.on_plot),
            MenuItem("custome_date", self.on_custom_date)
        )
        menu = Menu(
            MenuItem(f"Status: Recording", None),
            MenuItem("Stop record", self.on_stop),
            MenuItem("Plot", self.plot_submenu),
            MenuItem("Exit", self.on_exit)
        )
        self.icon = Icon("kachikachi", self.create_image(), "Kachikachi", menu = menu)

    def create_image(self):
        path  = os.path.dirname(__file__)
        image_path = os.path.join(path, "clock_icon_64x64.ico")
        image = Image.open(image_path)
        return image

    def on_stop(self, icon, item):
        threadManager.record_event.clear()
        icon.menu = Menu(
            MenuItem("Status: Stopping", None),
            MenuItem("Continue record", self.on_continue),
            MenuItem("Plot", self.plot_submenu),
            MenuItem("Exit", self.on_exit)
        )

    def on_continue(self, icon, item):
        threadManager.record_event.set()
        icon.menu = Menu(
            MenuItem("Status: Recording", None),
            MenuItem("Stop record", self.on_stop),
            MenuItem("Plot", self.plot_submenu),
            MenuItem("Exit", self.on_exit)
        )

    def on_exit(self, icon, item):
        threadManager.exit_event.set()
        self.icon.stop()

    def on_plot(self, icon, item):
        para = '-all'
        if item.text == 'today': para = '-today'
        if item.text == 'seven day': para = '-seven_day'
        if item.text == 'this month': para = '-month'
        if item.text == 'this year': para = '-year'
        print(para)
        subprocess.Popen([sys.executable, 'plot.py', para])

    def on_custom_date(icon, item):
        # Create a tkinter window for date selection
        root = tk.Tk()
        root.title("Select start and end dates, range: [start, end)")

        # Frame to hold the calendars side by side
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        # Create the start date calendar and label
        label_start = tk.Label(frame, text="Select start date(include):")
        label_start.grid(row=0, column=0, padx=5, pady=5)
        cal_start = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal_start.grid(row=1, column=0, padx=5, pady=5)

        # Create the end date calendar and label
        label_end = tk.Label(frame, text="Select end date(exclude):")
        label_end.grid(row=0, column=1, padx=5, pady=5)
        cal_end = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal_end.grid(row=1, column=1, padx=5, pady=5)

        # Function to handle the selection
        def on_confirm():
            start_date_str = cal_start.get_date()
            end_date_str = cal_end.get_date()

            start_time = int(datetime.strptime(start_date_str, "%Y-%m-%d").timestamp())
            end_time = int(datetime.strptime(end_date_str, "%Y-%m-%d").timestamp())
            # Print and store the selected dates
            print(f"Selected Start Date: {start_time}")
            print(f"Selected End Date: {end_time}")
            if start_time >= end_time:
                return

            subprocess.Popen([sys.executable, 'plot.py', '-start_time', str(start_time), '-end_time', str(end_time)])
            # Close the tkinter window
            root.destroy()

        # Add a confirm button
        confirm_btn = tk.Button(root, text="Confirm", command=on_confirm)
        confirm_btn.pack(pady=10)

        root.mainloop()
        print("root end")

    def run(self):
        self.icon.run()

trayInst = Tray()
