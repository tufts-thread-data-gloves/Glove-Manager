from ThreadDeviceDriverWrapper import ThreadDeviceDriverWrapper
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pathlib
import webbrowser
import time
from datetime import datetime

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
        self.minsize(width=950, height=700)
        self.title("Salmon Glove Manager")

        menu_container = tk.Frame(self)
        menu_container.pack(side="top", fill="both", expand=True)
        menu_container.configure(bg="white")

        # grids for the 'menubar' buttons
        menu_container.grid_columnconfigure(0, weight=1)
        menu_container.grid_columnconfigure(1, weight=1)

        topLeftFrame = tk.Frame(menu_container, relief='solid', bg="white")
        topLeftFrame.grid(row=0, column=0, padx=10, sticky="w")

        self.info_button = tk.Button(topLeftFrame, text="CONNECTION", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                     command=lambda: self.show_frame(InfoPage))
        self.setup_button = tk.Button(topLeftFrame, text="CALIBRATION", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                      command=lambda: self.show_frame(SetupPage))
        self.demo_button = tk.Button(topLeftFrame, text="DEMO", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                     command=lambda: self.show_frame(DemoPage))

        self.info_button.grid(row=0, column=0, padx=10, pady=10)
        self.setup_button.grid(row=0, column=1, padx=10, pady=10)
        self.demo_button.grid(row=0, column=2, padx=10, pady=10)

        topRightFrame = tk.Frame(menu_container, relief='solid', bg="white")
        topRightFrame.grid(row=0, column=1, padx=10, sticky="e")

        self.help_button = tk.Button(topRightFrame, text="HELP", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
                                     command=lambda: self.show_frame(HelpPage))
        self.about_button = tk.Button(topRightFrame, text="ABOUT", bg="white", bd=0, fg=GREY, font=("Verdana", 16),
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
        # banner
        self.welcome_label = tk.Label(self, text="Welcome to the Data Glove Manager!", font=("Verdana", 22), bg=GREY,
                                      anchor="center", fg="white")
        self.welcome_label.pack(fill='x', ipady=10)

        # sub-frame
        subFrame = tk.Frame(self)
        subFrame.pack(fill="both", expand=True)
        subFrame.configure(bg="white")

        subFrame.grid_columnconfigure(0, weight=1)
        subFrame.grid_columnconfigure(1, weight=1)
        leftFrame = tk.Frame(subFrame, relief='solid', bg="white")
        leftFrame.grid(row=0, column=0, padx=25, pady=20, sticky="w")
        rightFrame = tk.Frame(subFrame, relief='solid', bg="white")
        rightFrame.grid(row=0, column=1, padx=25, pady=20)

        subFrame.grid_columnconfigure(0, weight=1)
        subFrame.grid_columnconfigure(1, weight=1)

        # right frame content
        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.glove_image = tk.Label(rightFrame, image=self.img, bg="white")
        self.glove_image.pack(pady=20)

        self.start_button = tk.Button(rightFrame, text="CALIBRATE",
                                      command=lambda: controller.show_frame(InfoPage), font=("Verdana", 12),
                                      background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
        self.start_button.pack(pady=10, ipadx=20, ipady=5)

        # left frame content
        quickSetupLabel = tk.Label(leftFrame, text="Quick Setup Guide", anchor='w', justify="left",
                                   font=("Verdana", 18), bg="white")
        step1 = tk.Label(leftFrame, text="1. Place your hand inside the glove.", anchor='w', justify="left",
                         font=("Verdana", 16), bg="white")
        step2 = tk.Label(leftFrame, text="2. Power ON the glove.", anchor='w', justify="left",
                         font=("Verdana", 16), bg="white")
        step3 = tk.Label(leftFrame, text="3. Calibrate the glove with this application.", anchor='w', justify="left",
                         font=("Verdana", 16), bg="white")
        note = tk.Label(leftFrame, text="Note: The glove pairs automatically through bluetooth.", anchor='w',
                        justify="left",
                        font=("Verdana", 12), bg="white")
        quickSetupLabel.pack(pady=20, padx=15, fill="both")
        step1.pack(pady=10, padx=25, fill="both")
        step2.pack(pady=10, padx=25, fill="both")
        step3.pack(pady=10, padx=25, fill="both")
        note.pack(pady=25, padx=15, fill="both")

    def updateContent(self):
        # no-op for now
        return


class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.glove_connected_label = tk.Label(self, text="Glove Not Connected", font=("Verdana", 22), bg=FAILURE_RED,
                                              anchor="center", fg="white")
        self.glove_connected_label.pack(fill='x', ipady=10)

        self.time_connected_label = tk.Label(self, font=("Verdana", 20))

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.glove_image = tk.Label(self, image=self.img)
        self.glove_image.pack(pady=20)

        self.help_labela = tk.Label(self, text="1. Try powering the glove ON and OFF", font=("Verdana", 12),
                                    anchor="center")
        self.help_labelb = tk.Label(self, text="2. Try restarting this application", font=("Verdana", 12),
                                    anchor="center")

        self.refresh_button = tk.Button(self, text="Refresh Connection",
                                        command=lambda: self.is_glove_connected(), font=("Verdana", 14),
                                        background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
        self.refresh_button.pack(pady=20, ipadx=20, ipady=5)

        self.is_glove_connected()  # call this on init

    def is_glove_connected(self):
        self.glove_connected = td.is_glove_connected()
        if self.glove_connected:
            self.glove_connected_label.configure(text="Connection Successful!", bg=SUCCESS_GREEN)
            self.help_labela.pack_forget()
            self.help_labelb.pack_forget()
            # add the time label it was connected at
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("Connected on: %m/%d/%Y at %H:%M")
            self.time_connected_label.configure(text=dt_string)
            self.glove_image.pack_forget()
            self.refresh_button.pack_forget()
            self.time_connected_label.pack(pady=20)
            self.glove_image.pack(pady=20)
            self.refresh_button.pack(pady=20, ipadx=20, ipady=5)

        else:
            self.glove_connected_label.configure(text="Glove Not Connected", bg=FAILURE_RED)
            self.refresh_button.pack_forget()
            self.time_connected_label.pack_forget()
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
        self.current_filepath_str = ""  # used to store the file in use for calibration

        # empty widgets used in overlays
        self.description = None
        self.countdown_timer = None
        self.cal_button = None
        self.label_notconn = None
        self.time_connected_label = tk.Label(self, font=("Verdana", 20))
        self.file_connected_label = tk.Label(self, font=("Verdana", 20))

        # button to start calibration from saved file, or do it fresh
        self.button_calfromfile = tk.Button(self, command=lambda: self.showCalFileOverlay(), font=("Verdana", 14),
                                            background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
        self.button_calnew = tk.Button(self, command=lambda: self.showCalNewOverlay(), font=("Verdana", 14),
                                       background=BUTTON_BLUE, anchor="center", fg="white", bd=0)
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

        if self.description is not None:
            self.description.pack_forget()
        if self.cal_button is not None:
            self.cal_button.pack_forget()
        if self.cal_button is not None:
            self.countdown_timer.pack_forget()

        self.button_calfromfile.pack_forget()
        self.button_calnew.pack_forget()
        self.showCalMainPage()

        if self.is_glove_connected:
            try:
                self.label_notconn.pack_forget()
            except:
                pass
        else:
            self.banner_label.configure(text="Glove Not Connected", bg=FAILURE_RED,
                                        anchor="center", fg="white")
            self.label_notconn.pack(pady=20, padx=5)

    def showCalFileOverlay(self):
        self.hideCalMainPage()

        # overlay for doing saved file calibration
        self.banner_label.configure(text="Calibration From File", bg=BUTTON_BLUE)
        self.cal_button = tk.Button(self, font=("Verdana", 14), background=BUTTON_BLUE, anchor="center", fg="white",
                                    bd=0, text="Select File", command=lambda: self.selectSavedFile())
        self.cal_button.pack(ipadx=20, ipady=5, pady=10)

    def selectSavedFile(self):
        filepath = filedialog.askopenfilename()
        self.current_filepath_str = filepath

        try:
            td.set_calibration_with_file(filepath)
            self.is_calibrated = True
        except:
            # bad file/wrong format
            self.is_calibrated = False

        # clean up
        self.cal_button.pack_forget()
        self.showCalMainPage()

    def showCalNewOverlay(self):
        self.hideCalMainPage()

        # overlay for doing new calibration
        # we want description, countdown timer, start button, and saved file
        self.banner_label.configure(text="New Calibration", bg=BUTTON_BLUE)
        self.description = tk.Label(self, font=("Verdana", 16), wraplength=600,
                                    text="When ready, press start, then open your hand as wide as possible and close it into a tight fist.")
        # self.countdown_timer = tk.Label(self, font=MEDIUM_FONT, text="Time Left: 10 seconds")
        self.cal_button = tk.Button(self, text="Start", background=BUTTON_BLUE, anchor="center", fg="white",
                                    bd=0, font=("Verdana", 14), command=lambda: self.startCalibration())

        self.description.pack(pady=20)
        self.cal_button.pack(ipadx=25, ipady=5, pady=10)

    def startCalibration(self):
        filepath = str(pathlib.Path().absolute()) + "\\" + str(int(time.time())) + "calibration.txt"
        self.current_filepath_str = filepath

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
        self.time_connected_label.pack_forget()
        self.file_connected_label.pack_forget()

    def showCalMainPage(self):
        if self.is_calibrated:
            # new calibration, so set the date/time label to now
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("Last Calibration: %m/%d/%Y at %H:%M")
            self.time_connected_label.configure(text=dt_string)
            fileInUse = "File in Use: " + self.current_filepath_str
            self.file_connected_label.configure(text=fileInUse, wraplength=700)

            self.banner_label.configure(text="Calibration Successful!", bg=SUCCESS_GREEN)
            self.cal_image.pack_forget()
            self.time_connected_label.pack(pady=20)
            self.file_connected_label.pack(pady=20)
            self.cal_image.pack(pady=20)
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

        self.banner_label = tk.Label(self, text="Demonstration Video", font=("Verdana", 22), bg=GREY,
                                     anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)
        label = tk.Label(self,
                         text="This video highlight's the glove components and shows how to setup the glove.",
                         font=LARGE_FONT)
        label.pack(pady=20)
        button_video = tk.Button(self, text="Watch Video", command=lambda: self.open_demo_video(), bd=0, bg=BUTTON_BLUE,
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
        self.banner_label = tk.Label(self, text="Help", font=("Verdana", 22), bg=GREY,
                                     anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)

        faq_header = tk.Label(self, text="Frequently Asked Questions", font=("Verdana", 20), anchor='w')

        a = tk.Label(self, wraplength=600, anchor='w', justify="left", text="How do I power on the glove?",
                     font=("Verdana", 16))
        a_ans = tk.Label(self, wraplength=600, anchor='w', justify="left",
                         text="-> Plug the USB cord into the on-glove and battery and make sure the green LED light on the palm is on.",
                         font=("Verdana", 12))

        b = tk.Label(self, wraplength=600, anchor='w', justify="left", text="What software works with the glove?",
                     font=("Verdana", 16))
        b_ans = tk.Label(self, wraplength=600, anchor='w', justify="left",
                         text="-> A Unity demo application is available on our GitHub page. In addition, any software that runs on Windows 10 can connect with the API endpoints of the device driver.",
                         font=("Verdana", 12))

        trouble = tk.Label(self, wraplength=600, anchor='w', text="Troubleshooting Tips", font=("Verdana", 20))
        a_t = tk.Label(self, wraplength=600, anchor='w', justify="left", font=("Verdana", 12),
                       text="-> Calibrate the glove everytime to ensure accuracy.")
        b_t = tk.Label(self, wraplength=600, anchor='w', justify="left", font=("Verdana", 12),
                       text="-> Restart the application and the device driver if the glove can not connect.")

        morehelp = tk.Button(self, text="More Help and Documentation", fg="white",
                             command=lambda: self.open_github_link(),
                             font=("Verdana", 14), background=BUTTON_BLUE, anchor="center", bd=0)

        faq_header.pack(pady=25, fill='both', padx=15)
        a.pack(pady=25, fill='both', padx=20)
        a_ans.pack(pady=10, fill='both', padx=25)
        b.pack(pady=25, fill='both', padx=20)
        b_ans.pack(pady=10, fill='both', padx=25)
        trouble.pack(pady=25, fill='both', padx=15)
        a_t.pack(pady=10, fill='both', padx=20)
        b_t.pack(pady=10, fill='both', padx=20)
        morehelp.pack(ipady=5, ipadx=10, pady=20)

    def updateContent(self):
        # no-op for now
        return

    def open_github_link(self):
        webbrowser.open_new("https://github.com/tufts-thread-data-gloves")


class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.banner_label = tk.Label(self, text="About", font=("Verdana", 22), bg=GREY,
                                     anchor="center", fg="white")
        self.banner_label.pack(fill='x', ipady=10)

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.glove_image = tk.Label(self, image=self.img)
        self.glove_image.pack(pady=20)

        info_label = tk.Label(self,
                              text="Glove Components: Bluetooth Low Energy, Arduino 33 Nano BLE, Gyroscope, Accelerometer, Thread Resistors, Battery Source",
                              font=MEDIUM_FONT, wraplength=600)
        team_label = tk.Label(self,
                              text="The Team: Aaron Epstein (CS), Danny Bronshvayg (EE), Ben Santaus (CE), Nadya Ganem (HFE)",
                              font=MEDIUM_FONT)
        info_label.pack(pady=10)
        team_label.pack(pady=10)

    def updateContent(self):
        # no-op for now
        return


app = ManagerWindow()
app.mainloop()
