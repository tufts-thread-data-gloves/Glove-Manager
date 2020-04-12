from ThreadDeviceDriverWrapper import ThreadDeviceDriverWrapper
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pathlib
import webbrowser
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
        self.minsize(width=850, height=700)
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

        self.help_labela = tk.Label(self, text="1. Try powering the glove ON and OFF", font=("Verdana", 12), anchor="center")
        self.help_labelb = tk.Label(self, text="2. Try restarting this application", font=("Verdana", 12), anchor="center")

        self.refresh_button = tk.Button(self, text="Refresh Connection",
                                      command=lambda: self.is_glove_connected(), font=("Verdana", 14),
                                      background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
        self.refresh_button.pack(pady=20, ipadx=20, ipady=5)

        self.is_glove_connected() # call this on init

    def is_glove_connected(self):
        self.glove_connected = td.is_glove_connected()
        if self.glove_connected:
            self.glove_connected_label.configure(text="Connection Successful!", bg=SUCCESS_GREEN)
            self.help_labela.pack_forget()
            self.help_labelb.pack_forget()
        else:
            self.glove_connected_label.configure(text="Glove Not Connected", bg=FAILURE_RED)
            self.refresh_button.pack_forget()
            self.help_labela.pack(ipady=5)
            self.help_labelb.pack(ipady=5)
            self.refresh_button.pack(pady=20, ipadx=20, ipady=5)

    def updateContent(self):
        self.is_glove_connected()

class SetupPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.is_calibrated = False
        self.is_glove_connected = td.is_glove_connected()

        # empty widgets used in overlays
        self.description = None
        self.countdown_timer = None
        self.cal_button = None
        self.label_notconn = None
        self.remaining = 0

        # banner label and calibration image
        self.banner_label = tk.Label(self, text="Glove Not Connected", font=("Verdana", 22), bg=FAILURE_RED,
                                              anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)

        self.img = ImageTk.PhotoImage(Image.open("calibration_img.png"))
        self.cal_image = tk.Label(self, image=self.img)
        self.cal_image.pack(pady=20)

        if self.is_glove_connected:
            self.is_calibrated = td.is_calibrated()
            if self.is_calibrated:
                self.banner_label.configure(text="Calibration Successful!", bg=SUCCESS_GREEN)
            else:
                self.banner_label.configure(text="Glove Not Calibrated", bg=FAILURE_RED)

            # button to start calibration from saved file, or do it fresh
            self.button_calfromfile = tk.Button(self, command=lambda: self.showCalFileOverlay(), font=("Verdana", 14),
                                      background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
            self.button_calnew = tk.Button(self, command=lambda: self.showCalNewOverlay(), font=("Verdana", 14),
                                      background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
            if self.is_calibrated:
                self.button_calfromfile.configure(text="Recalibrate from saved file")
                self.button_calnew.configure(text="Recalibrate with new data")
            else:
                self.button_calfromfile.configure(text="Calibrate from saved file")
                self.button_calnew.configure(text="Calibrate with new data")
            self.button_calfromfile.pack(ipadx=20, ipady=5, pady=10)
            self.button_calnew.pack(ipadx=20, ipady=5, pady=10)
        else:
            # should not display calibration options yet if glove is not connected
            self.label_notconn = tk.Label(self, font=MEDIUM_FONT, wraplength=400,
                                      text="Please connect the Glove before continuing with setup. When the glove has been connected, please use the refresh connection button on the Info page.")
            self.label_notconn.pack(pady=20, padx=5)

    def updateContent(self):
        # this should hide overlays and show main options
        self.is_glove_connected = td.is_glove_connected()
        self.is_calibrated = td.is_calibrated()
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
        self.banner_label.configure(text="Calibration From File", bg=BUTTON_BLUE)
        self.cal_button = tk.Button(self, font=("Verdana", 14), background=BUTTON_BLUE, anchor="center", fg="white",
                                    bd=0, text="Select File", command=lambda : self.selectSavedFile())
        self.cal_button.pack(ipadx=20, ipady=5, pady=10)

    def selectSavedFile(self):
        filepath = filedialog.askopenfilename()

        td.set_calibration_with_file(filepath)
        self.is_calibrated = td.is_calibrated()

        # clean up
        self.cal_button.pack_forget()
        self.showCalMainPage()


    def showCalNewOverlay(self):
        self.hideCalMainPage()

        # overlay for doing new calibration
        # we want description, countdown timer, start button, and saved file
        self.banner_label.configure(text="New Calibration", bg=BUTTON_BLUE)
        self.description = tk.Label(self, font=("Verdana", 16),
            text="You will have 10 seconds to open your hand as wide as possible and close it into a tight fist")
        #self.countdown_timer = tk.Label(self, font=MEDIUM_FONT, text="Time Left: 10 seconds")
        self.cal_button = tk.Button(self, text="Start", background=BUTTON_BLUE, anchor="center", fg="white",
                                    bd=0, font=("Verdana", 14), command=lambda: self.startCalibration())

        self.description.pack(pady=20)
        self.cal_button.pack(ipadx=25, ipady=5, pady=10)

    def startCalibration(self):
        filepath = str(pathlib.Path().absolute()) + "\\" + str(int(time.time())) + "calibration.txt"

        # start calibration
        td.start_calibration(10, filepath)

        # do not need the calibration image here
        self.cal_image.pack_forget()
        self.countdown_timer = tk.Label(self, font=("Verdana", 24), text="10 Seconds")

        self.cal_button.pack_forget()
        self.description.pack_forget()
        self.countdown_timer.pack(pady=20)
        self.description.pack(pady=20)
        self.cal_button.configure(text="Restart", bg=FAILURE_RED, command=lambda: self.restartCalibration())
        self.cal_button.pack(ipadx=25, ipady=5, pady=10)

        # countdown and change countdown timer text
        self.countdown(10)

    def restartCalibration(self):
        self.cal_button.pack_forget()
        self.description.pack_forget()
        self.countdown_timer.pack_forget()
        self.cal_image.pack(pady=20)
        self.showCalNewOverlay()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        time_left = str(self.remaining) + " seconds"
        self.countdown_timer.configure(text=time_left)
        self.countdown_timer.pack(pady=20)
        if self.remaining <= 0:
            # when done, remove overlay and update is calibrated
            self.countdown_timer.pack_forget()
            self.description.pack_forget()
            self.cal_button.pack_forget()
            self.cal_image.pack(pady=20)
            self.is_calibrated = True
            self.showCalMainPage()
        else:
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

    def hideCalMainPage(self):
        if not self.label_notconn == None:
            self.label_notconn.pack_forget()
        self.button_calnew.pack_forget()
        self.button_calfromfile.pack_forget()

    def showCalMainPage(self):
        self.is_calibrated = td.is_calibrated()
        if self.is_calibrated:
            self.banner_label.configure(text="Calibration Successful!", bg=SUCCESS_GREEN)
        else:
            self.banner_label.configure(text="Glove Not Calibrated", bg=FAILURE_RED)

        if self.is_calibrated:
            self.button_calfromfile.configure(text="Recalibrate from saved file")
            self.button_calnew.configure(text="Recalibrate with new data")
        else:
            self.button_calfromfile.configure(text="Calibrate from saved file")
            self.button_calnew.configure(text="Calibrate with new data")
        self.button_calfromfile.pack(ipadx=20, ipady=5, pady=10)
        self.button_calnew.pack(ipadx=20, ipady=5, pady=10)

class DemoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.banner_label = tk.Label(self, text="Demo", font=("Verdana", 22), bg=GREY,
                                     anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)
        label = tk.Label(self,
                         text="For a demo of how to calibrate and use the glove:",
                         font=LARGE_FONT)
        label.pack(pady=20)
        button_video = tk.Button(self, text="Demo Video", command=lambda: self.open_demo_video(), bd=0, bg=BUTTON_BLUE,
                                 fg="white", font=("Verdana", 14))
        button_video.pack(ipadx=15, ipady=5, pady=10)

    def updateContent(self):
        # no-op for now
        return

    def open_demo_video(self):
        webbrowser.open_new("https://www.youtube.com/watch?v=XF3agju379w&feature=youtu.be")

class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.banner_label = tk.Label(self, text="FAQ", font=("Verdana", 22), bg=GREY,
                                     anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)

        a = tk.Label(self, wraplength=600, text="1. I still can't get the glove to connect, what else should I try?", font=("Verdana", 16))
        a_ans = tk.Label(self, wraplength=600, text="-> Stop the execution of the device driver and quit out of this. Power off the glove, and then back on, start the device driver, and then start the Glove Manager.",
                         font=("Verdana", 12))

        b = tk.Label(self, wraplength=600, text="2. What is a saved calibration file?", font=("Verdana", 16))
        b_ans = tk.Label(self, wraplength=600, text="-> A saved calibration file is a .txt file with two lines of sensor readings. These are default saved to files with the pattern #####calibration.txt where the ##### is a number that signifies the timestamp when the calibration was done.",
                         font=("Verdana", 12))

        c = tk.Label(self, wraplength=600, text="3. Where can I find more documentation on this glove and how to interface with it?", font=("Verdana", 16))
        c_ans = tk.Label(self, wraplength=600, text="-> Full documentation for this glove can be found on the GitHub repository linked on the about page.",
                         font=("Verdana", 12))

        a.pack(pady=25)
        a_ans.pack(pady=10)
        b.pack(pady=25)
        b_ans.pack(pady=10)
        c.pack(pady=25)
        c_ans.pack(pady=10)

    def updateContent(self):
        # no-op for now
        return

class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.banner_label = tk.Label(self, text="FAQ", font=("Verdana", 22), bg=GREY,
                                     anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.glove_image = tk.Label(self, image=self.img)
        self.glove_image.pack(pady=20)

        team_label = tk.Label(self, text="The Team: Aaron Epstein (CS), Danny Bronshvayg (EE), Ben Santaus (CE), Nadya Ganem (HF)", font=MEDIUM_FONT)
        info_label = tk.Label(self, text="This glove was produced as part of a Senior Design Project and is licensed under ****", font=MEDIUM_FONT)
        github_link = tk.Button(self, text="GitHub Repository", fg="white", command=lambda: self.open_github_link(),
                                font=("Verdana", 14), background=BUTTON_BLUE, anchor="center", bd=0)

        team_label.pack(pady=10)
        info_label.pack(pady=10)
        github_link.pack(ipadx=20, ipady=5, pady=10)

    def updateContent(self):
        # no-op for now
        return

    def open_github_link(self):
        webbrowser.open_new("https://github.com/tufts-thread-data-gloves")



app = ManagerWindow()
app.mainloop()