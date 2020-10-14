# Import all the neccessary modules
import subprocess
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os # For path manipulation

"""
The class PyIDE contains the application code
"""


class PyIDE:
    def __init__(self):
        # Instanciate some controls (Btw I am not sure if in Python is called Instantiation I am more familiar with C#)
        self.root = Tk()
        self.menu = Menu(self.root)
        self.scroll = Scrollbar(self.root)
        self.m1 = Menu(self.menu, tearoff=0)
        self.m2 = Menu(self.menu, tearoff=0)
        self.output = Text(self.root, yscrollcommand=self.scroll.set)
        self.codeEditor = Text(self.root, undo=1, tabs=1, yscrollcommand=self.scroll.set, font=35)
        self.frame = Frame(self.root, bg="grey")
        # Declare some variables
        self.filepath = ""
        self.filename = "Untitled"
        self.filetypes = (["Python File", "*.py"], ["Python Compiled Bytecode", "*.pyc"])
        # Create the GUI
        self.CreateWindow()
        # Display the GUI
        self.root.mainloop()

    def ConfigureMenus(self):
        # Create File menu
        self.m1.add_command(label="Open", command=self.OpenFile)
        self.m1.add_command(label="Save", command=self.SaveFile)
        self.m1.add_command(label="Save As", command=self.SaveAsFile)
        self.m1.add_command(label="New File", command=self.NewFile)
        self.m1.add_separator()
        self.m1.add_command(label="Run", command=self.Run)
        # Create About Menu
        self.m2.add_command(label="About", command=self.AboutUs)
        # Cascade the menus
        self.menu.add_cascade(label="File", menu=self.m1)
        self.menu.add_cascade(label="Help", menu=self.m2)

    def CreateWindow(self):
        self.__UpdateTitle()
        self.root.iconbitmap('pyidelogo.ico')
        # Configure the menus
        self.ConfigureMenus()
        self.root.config(menu=self.menu)
        self.frame.pack(side=LEFT, fill=Y)
        self.scroll.pack(side=RIGHT, fill=Y, ipady=140)
        self.codeEditor.pack(fill=BOTH, ipady=10)
        self.scroll.config(command=self.codeEditor.yview)
        self.output.insert("end-1c",
                           "Your output will be shown here\n1.Write your code above\n2.Save it\n3.Run")
        self.output.config(state=DISABLED)
        self.scroll.config(command=self.output.yview)
        self.scroll.pack(side=RIGHT, fill=Y, ipady=140)
        self.output.pack(fill=X, side=BOTTOM)

    def AboutUs(self):
        messagebox.showinfo("About",
                            "The project is Open Source (available on github) and maintained by Jaspreet Singh")

    def OpenFile(self):
        try:
            # Open File and get its contents
            self.file = filedialog.askopenfile(parent=self.root, filetypes=self.filetypes)  # Open File
            # Store FilePath
            self.filepath = self.file.name
            self.fileContents = self.file.read()  # Get File Contents
            # Close the file
            self.file.close()
            # Write Contents to Editor
            self.codeEditor.delete(0.0, END)
            self.codeEditor.insert(END, self.fileContents)
            # Configure Window Title
            self.filename = os.path.split(self.filepath)[1]  # Get Filename
            self.__UpdateTitle()
        except PermissionError:
            messagebox.showerror("Oops!", "It seems like you do not have permission to modify this file")

    """
    Returns True if the function saves the file without needing to call SaveAsFile
    """
    def SaveFile(self):
        try:
            if self.filepath != "":
                self.file = open(self.filepath, "w", encoding='utf-8')
                self.file.write(self.codeEditor.get(0.0, END))
                self.file.close()
                return True
            else:
                self.SaveAsFile()
        except PermissionError:
            messagebox.showerror("Oops!", "It seems like you do not have permission to modify this file")
        except:
            messagebox.showerror("Oops!", "Something went wrong!")

    def NewFile(self):
        self.filepath = ""
        self.filename = "Untitled"
        self.codeEditor.delete(0.0, END)
        self.__UpdateTitle()

    def __UpdateTitle(self):
        # Pretty straight forward. It just changes the title to the current filename
        self.root.title(f"PyIDE - {self.filename}")

    def Run(self):
        # If the file has not been saved it will attempt to automatically save it
        if not self.SaveFile():
            return # if the user closes the dialog then return
        self.output.delete('1.0', END)
        self.process = subprocess.Popen(f"py {self.filepath}", stdout=subprocess.PIPE, shell=True,
                                            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        self.out, self.err = self.process.communicate()
        # Show the output
        self.output.config(state=NORMAL) # Enable writing
        self.output.delete(0.0, END)
        self.output.insert("end-1c", self.out)
        self.output.insert("end-1c", self.err)
        self.output.config(state=DISABLED) # Make Read-Only

    """
    Returns True if the file is saved successfully
    """
    def SaveAsFile(self):
        try:
            self.file = filedialog.asksaveasfile(mode="w", initialfile=self.filename, defaultextension="*.txt",
                                                 filetypes=self.filetypes)  # Open File
            self.file.write(self.codeEditor.get(0.0, END))  # Write to file
            self.filepath = self.file.name  # Get filepath
            # Close File
            self.file.close()
            # Configure Window
            self.filename = os.path.split(self.file.name)[1]  # Get Filename
            self.__UpdateTitle()
            return True
        except AttributeError:
            pass
        except PermissionError:
            messagebox.showerror("Oops!", "It seems like you do not have permission to modify this file")
        except Exception:
            messagebox.showerror("Oops!", "It seems like something went wrong while trying to save this file")


if __name__ == "__main__":
    window = PyIDE()
