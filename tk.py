import os
import subprocess
import threading
from tkinter import *
from tkinter import ttk

# Global variables
counter = 0
l = ['Loading', 'Loading.', 'Loading..', 'Loading...']
subprocess_running = False  # Variable to track subprocess status

# Auxiliary functions
def loadingLabelChange():
    global counter
    if not subprocess_running:
        return  # Stop the animation if subprocess is finished

    loading.configure(text=l[counter])

    if counter >= 3:
        counter = 0
    else:
        counter += 1

    root.after(1000, loadingLabelChange)  # Schedule the next update

def runSubprocess():
    global subprocess_running
    try:
        dirname = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(['python', os.path.join(dirname, 'main.py'), input.get().strip()], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print('stdout:', result.stdout)
        print('stderr:', result.stderr)
        result.check_returncode()  # Check for non-zero return code
    except subprocess.CalledProcessError as e:
        print('Error while running the subprocess:', e)
    finally:
        subprocess_running = False  # Set subprocess_running to False when subprocess is finished
        root.quit()  # Close the root window



def stateClicked():
    global subprocess_running
    if subprocess_running:
        return  # Return if subprocess is alre ady running

    # Hide the input, label, and button
    input.pack_forget()
    label.pack_forget()
    btn.pack_forget()

    # Show the loading label
    loading.pack(pady=150)

    # Call the loading function
    subprocess_running = True
    threading.Thread(target=runSubprocess).start()

    # Start the loadingLabelChange function
    loadingLabelChange()


if __name__ == '__main__' :
    root = Tk()
    root.title('Influencers Spam')
    root.geometry('400x400+500+210')
    root.configure(background='grey')

    # Label
    label = ttk.Label(root, text='Influencers Spam', font=('Arial', 20, 'bold'), background='grey', foreground='black')
    label.pack(pady=10)

    # Input
    input = ttk.Entry(root, width=30, font=('Arial', 15, 'bold'), cursor='ibeam', justify='center')
    input.pack(pady=10)

    # Button
    btn = ttk.Button(root, text='Send', width=20, cursor='hand2', command=stateClicked, style='TButton')
    btn.pack(pady=10)

    # Loading
    loading = ttk.Label(root, text='Loading...', font=('Arial', 20, 'bold'), background='grey', foreground='black')

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