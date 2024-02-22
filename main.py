import os
import logging
import platform
import threading
import subprocess
import tkinter as tk
from tkinter import ttk
from Utils.utils import grepFileName

# Basic logging configuration
logger = logging.getLogger(grepFileName(__file__))
logger.setLevel(logging.INFO)

handler = logging.FileHandler('log.log', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(levelname)s %(name)s -> %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

class BaseFrame:
    def __init__(self, root):
        self.root = root

        # Variables that the user will pass
        self.username = ''
        self.hashtags = ''
        self.message = ''

        # Setting the styles of the widgets
        self.style = ttk.Style()
        self.style.configure('TLabel', foreground='yellow', background='black', font=('Arial', 15), justify=tk.CENTER, width=30, anchor=tk.CENTER, wraplength=300)
        self.style.configure('TEntry', foreground='black', background='white', font=('Arial', 15), justify=tk.CENTER, width=30, anchor=tk.CENTER)
        self.style.configure('TButton', foreground='black', background='black', font=('Arial', 10), justify=tk.CENTER, width=25, anchor=tk.CENTER)

        # Elements
        self.label = ttk.Label(self.root)
        self.input = ttk.Entry(self.root)
        self.button = ttk.Button(self.root)
        self.first()

        # Loading Features
        self.load = ['Loading', 'Loading.', 'Loading..', 'Loading...']
        self.counter = 0

        # Subprocess output
        self.output = None

        # Flag to track subprocess completion
        self.subprocessComplete = False

    '''
    The basic states of the GUI are the following :
    first : the user is asked to insert the username (to see if it already exists)
    second : the user is asked to log on Instagram, that's the case if the username does not exist
    third : the user is asked to insert the target influencer to make the spams
    '''
    def first(self):
        logger.info('In the first state of the GUI')
        self.label.configure(text='Select your username')
        self.button.configure(text='Submit', command=self.checkUsername)
        self.label.place(relx=0.5, rely=0.4, anchor=tk.CENTER, bordermode='outside')
        self.input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def second(self):
        logger.info('In the second state of the GUI')
        self.refresh()
        self.label.configure(text='That username does not exist!\nPlease log on Instagram.')
        self.button.configure(text='Log on Instagram', command=self.saveCookies)
        self.label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # The third state and the fourth state work together, is just a matter of getting the desired hashtag
    # and the desired message to spam
        
    def third(self):
        logger.info('In the third state of the GUI')
        self.refresh()
        self.label.configure(text='Target hashtags:')
        self.input.configure()
        self.button.configure(text='Submit', command=self.checkHashtags)
        self.label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def checkHashtags(self) :
        self.hashtags = self.input.get().strip()
        self.refresh()
        logger.info(f'Checking the following hashtags: {self.hashtags}')

        if(len(self.hashtags) == 0) :
            self.label.configure(text='Please, you need to insert a hashtag.')
            self.button.configure(text='Back', command=self.third)
        elif(not '#' in self.hashtags) :
            self.label.configure(text='Insert the hashtag in a correct form like\n#ruyter#ruytercortes')
            self.button.configure(text='Back', command=self.third)
        # If everything is ok, can go the fourth state
        else :
            self.fourth()
        
        self.label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


    def fourth(self):
        logger.info('In the fourth state of the GUI')
        self.refresh()
        self.label.configure(text='Message to spam:')
        self.input.configure()
        self.button.configure(text='Submit', command=self.spam)
        self.label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # It is called by the second state
    def saveCookies(self):
        self.refresh()
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        try:
            threading.Thread(target=self.runSubprocess, args=('cookiesSaver.py',)).start()
        except Exception as e:
            print(e)
            exit()

        self.loading()

    # It is called by the third state
    def spam(self):
        self.message = self.input.get().strip()
        self.refresh()
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        try:
            threading.Thread(target=self.runSubprocess, args=('spam.py', self.username ,self.hashtags, self.message)).start()
        except Exception as e:
            print(e)
            exit()

        self.loading()

    def checkUsername(self):
        dirname = os.path.dirname(os.path.abspath(__file__))

        # Check if the cookies dir exists, if not create it
        if(not os.path.exists(os.path.join(dirname, 'Cookies'))): os.mkdir(os.path.join(dirname, 'Cookies'))

        for f in os.listdir(os.path.join(dirname, 'Cookies')):
            with open(os.path.join(dirname, 'Cookies', f), 'r') as file:
                if self.input.get().strip() in file.readline():
                    # Load the third state if the username exists
                    self.username = self.input.get().strip()
                    self.third()
                    return

        # Load the second state if the username does not exist
        self.second()

    def runSubprocess(self, *args):
        # Basic treatment of the arguments
        dirname = os.path.dirname(os.path.abspath(__file__))
        activate = os.path.join(dirname, 'venv', 'Scripts', 'activate.bat')
        p = 'python'

        if platform.system() == 'Linux':
            p = 'python3'
            x = ['bash', '-c', f'source {os.path.join(dirname, "venv", "bin", "activate")} && {p} {os.path.join(dirname, args[0])}']
        else : 
            x = [activate, '&&', p , os.path.join(dirname, args[0])]

        if len(args) == 4: 
            x.append(args[1])
            x.append(args[2])
            x.append(args[3])

        logger.info(f'Calling the subprocess: {x}')
        result = subprocess.run(x, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info(f'Subprocess result: {result}')
        self.output = result.stdout 
        self.subprocessComplete = True  # Set the flag to indicate subprocess completion

    def loading(self):
        if self.subprocessComplete:
            self.label.configure(text='Done!\nYou can close the window now.')
            if not self.subprocessComplete:
                self.root.after(10000, self.root.destroy)  # Close the window after 10 seconds if subprocess not complete
            return

        self.label.configure(text=self.load[self.counter])
        if self.counter >= 3:
            self.counter = 0
        else:
            self.counter += 1

        self.root.after(500, self.loading)

    def refresh(self):
        self.label.place_forget()
        self.input.place_forget()
        self.input.delete(0, tk.END)
        self.button.place_forget()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Influencer Spammer')
    root.configure(background='black')
    root.geometry('400x400')
    base = BaseFrame(root)
    root.mainloop()

'''
Even this simple program illustrates the following key Tk concepts:

widgets
A Tkinter user interface is made up of individual widgets. Each widget is represented as a Python object, instantiated from classes like ttk.Frame, ttk.Label, and ttk.Button.

widget hierarchy
Widgets are arranged in a hierarchy. The label and button were contained within a frame, which in turn was contained within the root window. When creating each child widget, its parent widget is passed as the first argument to the widget constructor.

configuration options
Widgets have configuration options, which modify their appearance and behavior, such as the text to display in a label or button. Different classes of widgets will have different sets of options.

geometry management
Widgets aren’t automatically added to the user interface when they are created. A geometry manager like grid controls where in the user interface they are placed.

event loop
Tkinter reacts to user input, changes from your program, and even refreshes the display only when actively running an event loop. If your program isn’t running the event loop, your user interface won’t update.


To get any information do as follows:

btn = ttk.Button(frm, ...)
print(btn.configure().keys())
'''