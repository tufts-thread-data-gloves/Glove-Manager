import ThreadDeviceDriverWrapper as td
import tkinter as tk

LARGE_FONT = ("Verdana", 12)

class ManagerWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(width=500, height=300)
        self.title("Salmon Glove Manager")
        menubar = tk.Menu(self)

        menubar.add_command(label="Info", command=lambda: self.show_frame(InfoPage))
        menubar.add_command(label="Setup", command=lambda: self.show_frame(SetupPage))
        menubar.add_command(label="Demo", command=lambda: self.show_frame(DemoPage))
        menubar.add_command(label="Help", command=lambda: self.show_frame(HelpPage))

        self.config(menu=menubar)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (InfoPage, SetupPage, DemoPage, HelpPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(InfoPage)

    def do_nothing(self):
        print("nah")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Info Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

class SetupPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Setup Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

class DemoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Demo Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="HELP!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = ManagerWindow()
app.mainloop()