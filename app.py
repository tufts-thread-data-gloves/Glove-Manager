from ThreadDeviceDriverWrapper import ThreadDeviceDriverWrapper
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pathlib
import os
import time

LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
GREY = "#444547"
BUTTON_BLUE = "#399CFC"
SUCCESS_GREEN = "#1DB817"
FAILURE_RED = "#EB1331"

global td
td = ThreadDeviceDriverWrapper()

class ManagerWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        try:
            td.connect()
        except Exception as e:
            print("Failed to connect to glove driver with exception", e)
            exit(1)

        # setup up tkinter screen
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(width=1000, height=700)
        self.title("Salmon Glove Manager")

        menu_container = tk.Frame(self)
        menu_container.pack(side="top", fill="both", expand=True)
        menu_container.configure(bg="white")

        # grids for the 'menubar' buttons
        menu_container.grid_columnconfigure(0, weight=1)
        menu_container.grid_columnconfigure(1, weight=1)

        topLeftFrame = tk.Frame(menu_container, relief='solid', bg="white")
        topLeftFrame.grid(row=0, column=0, padx=10, sticky="w")

        self.info_button = tk.Button(topLeftFrame, text="Info", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                command=lambda: self.show_frame(InfoPage))
        self.setup_button = tk.Button(topLeftFrame, text="Setup", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                 command=lambda: self.show_frame(SetupPage))
        self.demo_button = tk.Button(topLeftFrame, text="Demo", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                command=lambda: self.show_frame(DemoPage))

        self.info_button.grid(row=0, column=0, padx=10, pady=10)
        self.setup_button.grid(row=0, column=1, padx=10, pady=10)
        self.demo_button.grid(row=0, column=2, padx=10, pady=10)

        topRightFrame = tk.Frame(menu_container, relief='solid', bg="white")
        topRightFrame.grid(row=0, column=1, padx=10, sticky="e")

        self.help_button = tk.Button(topRightFrame, text="Help", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                command=lambda: self.show_frame(HelpPage))
        self.about_button = tk.Button(topRightFrame, text="About", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                 command=lambda: self.show_frame(AboutPage))
        self.help_button.grid(row=0, column=0, padx=10, pady=10)
        self.about_button.grid(row=0, column=1, padx=10, pady=10)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, InfoPage, SetupPage, DemoPage, HelpPage, AboutPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")



        self.show_frame(HomePage)

    def show_frame(self, cont):
        # set all buttons back to normal first
        self.info_button.configure(bg="white", fg=GREY)
        self.setup_button.configure(bg="white", fg=GREY)
        self.demo_button.configure(bg="white", fg=GREY)
        self.help_button.configure(bg="white", fg=GREY)
        self.about_button.configure(bg="white", fg=GREY)

        frame = self.frames[cont]
        frame.tkraise()
        frame.updateContent()

        if cont == InfoPage:
            self.info_button.configure(bg=GREY, fg="white")
        elif cont == SetupPage:
            self.setup_button.configure(bg=GREY, fg="white")
        elif cont == DemoPage:
            self.demo_button.configure(bg=GREY, fg="white")
        elif cont == HelpPage:
            self.help_button.configure(bg=GREY, fg="white")
        elif cont == AboutPage:
            self.about_button.configure(bg=GREY, fg="white")


    def is_glove_connected(self):
        return td.is_glove_connected()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.welcome_label = tk.Label(self, text="Welcome!", font=("Verdana", 22), bg=GREY, anchor="center", fg="white")
        self.welcome_label.pack(fill='x', ipady=10)

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.glove_image = tk.Label(self, image=self.img)
        self.glove_image.pack(pady=20)

        self.start_button = tk.Button(self, text="Start!",
                                   command=lambda: controller.show_frame(InfoPage), font=("Verdana", 14),
                                   background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
        self.start_button.pack(pady=20, ipadx=40, ipady=5)

    def updateContent(self):
        # no-op for now
        return



class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.glove_connected_label = tk.Label(self, text="Glove Not Connected", font=("Verdana", 22), bg=FAILURE_RED, anchor="center", fg="white")
        self.glove_connected_label.pack(fill='x', ipady=10)

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.glove_image = tk.Label(self, image=self.img)
        self.glove_image.pack(pady=20)

        self.refresh_button = tk.Button(self, text="Refresh Connection",
                                      command=lambda: self.is_glove_connected(), font=("Verdana", 14),
                                      background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
        self.refresh_button.pack(pady=20, ipadx=20, ipady=5)

        self.is_glove_connected() # call this on init

    def is_glove_connected(self):
        self.glove_connected = td.is_glove_connected()
        if self.glove_connected:
            self.glove_connected_label.configure(text="Connection Successful!", bg=SUCCESS_GREEN)
        else:
            self.glove_connected_label.configure(text="Glove Not Connected", bg=FAILURE_RED)

    def updateContent(self):
        self.is_glove_connected()

class SetupPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Setup Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.is_calibrated = False

        # empty widgets used in overlays
        self.description = None
        self.countdown_timer = None
        self.cal_button = None
        self.label_notconn = None
        self.remaining = 0

        print(td.is_glove_connected())

        if not td.is_glove_connected():
            # should not display calibration options yet if glove is not connected
            self.label_notconn = tk.Label(self, font=MEDIUM_FONT, wraplength=100, text="Please connect the Salmon Glove before continuing with setup. When the glove has been connected, please use the refresh connection button on the Info page.")
            self.label_notconn.pack(pady=5, padx=5)
        else:
            self.is_calibrated = td.is_calibrated()
            self.label_cal_status = tk.Label(self, font=MEDIUM_FONT)
            if self.is_calibrated:
                self.label_cal_status.configure(text="Salmon Glove is Calibrated!")
            else:
                self.label_cal_status.configure(text="Salmon Glove is not Calibrated")
            self.label_cal_status.pack(pady=5, padx=5)

            # button to start calibration from saved file, or do it fresh
            self.button_calfromfile = tk.Button(self, command=lambda: self.showCalFileOverlay())
            self.button_calnew = tk.Button(self, command=lambda: self.showCalNewOverlay())
            if self.is_calibrated:
                self.button_calfromfile.configure(text="Recalibrate from saved file")
                self.button_calnew.configure(text="Recalibrate with new data")
            else:
                self.button_calfromfile.configure(text="Calibrate from saved file")
                self.button_calnew.configure(text="Calibrate with new data")
            self.button_calfromfile.pack(padx=5, pady=5)
            self.button_calnew.pack(padx=5, pady=5)

        # At the top we want it to say if it is calibrated or not/connected or not
        # Label that describes directions for setting new calibration settings

    def updateContent(self):
        # this should hide overlays and show main options
        try:
            self.description.pack_forget()
            self.cal_button.pack_forget()
            self.countdown_timer.pack_forget()
            self.showCalMainPage()
        except:
            return

    def showCalFileOverlay(self):
        self.hideCalMainPage()

        # overlay for doing saved file calibration
        # we want description, button to select file, result
        self.description = tk.Label(self, font=MEDIUM_FONT, text="To start a calibration with saved information, select a file below and then press calibrate with saved file.")
        self.cal_button = tk.Button(self, font=MEDIUM_FONT, text="Select File", command=lambda : self.selectSavedFile())
        self.description.pack(padx=5, pady=5)
        self.cal_button.pack(padx=5, pady=5)

    def selectSavedFile(self):
        filepath = filedialog.askopenfilename()
        self.cal_button.configure(text="Finish Calibrating with Selected File", command=lambda : self.calibrateWithSavedFile(filepath))

    def calibrateWithSavedFile(self, filepath):
        td.set_calibration_with_file(filepath)
        self.is_calibrated = td.is_calibrated()

        # clean up
        self.description.pack_forget()
        self.cal_button.pack_forget()
        self.showCalMainPage()


    def showCalNewOverlay(self):
        self.hideCalMainPage()

        # overlay for doing new calibration
        # we want description, countdown timer, start button, and saved file
        self.description = tk.Label(self, font=MEDIUM_FONT,
            text="To start a new calibration press the button below labeled 'Start Calibration'. "  \
                "Once pressed, you will have 10 seconds to open your hand as wide as possible and close it into a tight fist.")
        self.countdown_timer = tk.Label(self, font=MEDIUM_FONT, text="Time Left: 10 seconds")
        self.cal_button = tk.Button(self, text="Start Calibration", command=lambda: self.startCalibration())
        self.description.pack(padx=5, pady=5)
        self.countdown_timer.pack(padx=5, pady=5)
        self.cal_button.pack(padx=5, pady=5)

    def startCalibration(self):
        filepath = str(pathlib.Path().absolute()) + "\\" + str(int(time.time())) + "calibration.txt"

        # start calibration
        td.start_calibration(10, filepath)

        self.cal_button.pack_forget()

        # countdown and change countdown timer text
        self.countdown(10)

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        time_left = "Time Left: " + str(self.remaining) + " seconds"
        self.countdown_timer.configure(text=time_left)
        self.countdown_timer.pack(padx=5, pady=5)
        if self.remaining <= 0:
            # when done, remove overlay and update is calibrated
            self.countdown_timer.pack_forget()
            self.description.pack_forget()
            self.cal_button.pack_forget()
            self.is_calibrated = True
            self.showCalMainPage()
        else:
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

    def hideCalMainPage(self):
        if not self.label_notconn == None:
            self.label_notconn.pack_forget()
        self.label_cal_status.pack_forget()
        self.button_calnew.pack_forget()
        self.button_calfromfile.pack_forget()

    def showCalMainPage(self):
        if self.is_calibrated:
            self.label_cal_status.configure(text="Salmon Glove is Calibrated!")
        else:
            self.label_cal_status.configure(text="Salmon Glove is not Calibrated")
        self.label_cal_status.pack(pady=5, padx=5)

        # button to start calibration from saved file, or do it fresh
        self.button_calfromfile = tk.Button(self, command=lambda: self.showCalFileOverlay())
        self.button_calnew = tk.Button(self, command=lambda: self.showCalNewOverlay())
        if self.is_calibrated:
            self.button_calfromfile.configure(text="Recalibrate from saved file")
            self.button_calnew.configure(text="Recalibrate with new data")
        else:
            self.button_calfromfile.configure(text="Calibrate from saved file")
            self.button_calnew.configure(text="Calibrate with new data")
        self.button_calfromfile.pack(padx=5, pady=5)
        self.button_calnew.pack(padx=5, pady=5)

class DemoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Demo Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    def updateContent(self):
        # no-op for now
        return

class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="HELP!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    def updateContent(self):
        # no-op for now
        return

class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="About", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    def updateContent(self):
        # no-op for now
        return



app = ManagerWindow()
app.mainloop()