# Import all the neccessary modules
import subprocess
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
from threading import *
import time

"""
The class PyIDE contains the application code
"""


class PyIDE:
    def __init__(self):
        # Create our window
        self.root = Tk()
        # Declare some variables
        self.filepath = ""
        self.filename = "Untitled"
        self.filetypes = (["Python File", "*.py"], ["All Files", "*.*"])
        # Creates the GUI
        self.CreateWindow()
        # Make the window start in the size of the screen
        self.width, self.height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (self.width, self.height))
        # Configure bindings
        self.configBindings()
        # Start the Syntax Thread
        self.syntaxThread = Thread(target=self.SyntaxHighlighting)
        self.syntaxThread.setDaemon(True)
        self.syntaxThread.start()
        # Display the GUI
        self.root.mainloop()

    # This method is executed by a thread
    def SyntaxHighlighting(self):
        # The color scheme
        self.colorMap = {"print": "light sky blue", "def": "gold", "import": "orange", "from": "orange",
                         "for": "orange", "while": "orange", "True": "blue", "False": "red", "self": "purple",
                         "\\n": "green2", "\\r": "green2", "class": "orange2", "None": "brown3"}
        self.delay = 0.02  # If there is no delay the app will freeze
        while True:
            time.sleep(self.delay)
            for word in self.colorMap:
                self.start_pos = self.codeEditor.search(word, '1.0', stopindex=END)
                if self.start_pos:
                    self.end_pos = '{}+{}c'.format(self.start_pos, len(word))
                    self.codeEditor.tag_add(word, self.start_pos, self.end_pos)
                    self.codeEditor.tag_config(word, foreground=self.colorMap[word])

    def configBindings(self):
        # Right Click
        self.codeEditor.bind("<Button-3>", self.RightClickMenu)
        # Key bindings
        self.root.bind_all("<Control-o>", self.OpenFile)
        self.root.bind_all("<Control-s>", self.SaveFile)
        self.root.bind_all("<Control-r>", self.Run)
        self.root.bind_all("Control-n", self.NewFile)

    def RightClickMenu(self, event=None):
        self.popup = Menu(self.root, tearoff=0)
        self.popup.add_command(label="Copy", command=self.Copy)
        self.popup.add_command(label="Paste", command=self.Paste)
        self.popup.add_command(label="Delete", command=self.Delete)
        self.popup.add_command(label="Cut", command=self.Cut)
        self.popup.add_separator()
        self.popup.add_command(label="Select All", command=self.SelectAll)
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    # ==================================== #
    # Basic Commands
    def Copy(self):
        selected = self.codeEditor.get(SEL_FIRST, SEL_LAST)
        self.codeEditor.clipboard_clear()
        self.codeEditor.clipboard_append(selected)

    def Paste(self):
        self.codeEditor.insert(INSERT, self.codeEditor.clipboard_get())

    def Delete(self):
        self.codeEditor.delete(SEL_FIRST, SEL_LAST)

    def Cut(self):
        self.Copy()
        self.Delete()

    def SelectAll(self):
        self.codeEditor.tag_add(SEL, "1.0", END)

    # ==================================== #

    def CreateFileSystemMenu(self):
        # Create Project Submenu
        self.projectMenu = Menu(self.menu, tearoff=0)
        self.projectMenu.add_command(label="Reload", command=self.Reload)
        self.projectMenu.add_command(label="Copy Path", command=self.CopyPath)
        self.projectMenu.add_command(label="Open in Explorer", command=self.OpenInExplorer)
        self.projectMenu.add_command(label="Open Console", command=self.OpenConsole)
        # Create File menu
        self.fileMenu = Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.OpenFile, accelerator="Ctrl+O")
        self.fileMenu.add_command(label="Save", command=self.SaveFile, accelerator="Ctrl+S")
        self.fileMenu.add_command(label="Save As", command=self.SaveAsFile)
        self.fileMenu.add_command(label="New File", command=self.NewFile, accelerator="Ctrl+N")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Run", command=self.Run, accelerator="Ctrl+R")
        self.fileMenu.add_separator()
        self.fileMenu.add_cascade(label="Project", menu=self.projectMenu)  # This will create a sub-menu
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.Exit)

    def CreateEditMenu(self):
        # Create the Edit Menu
        self.editMenu = Menu(self.menu, tearoff=0)
        self.editMenu.add_command(label="Copy", command=self.Copy, accelerator="Ctrl+C")
        self.editMenu.add_command(label="Paste", command=self.Paste, accelerator="Ctrl+V")
        self.editMenu.add_command(label="Delete", command=self.Delete, accelerator="Delete")
        self.editMenu.add_command(label="Cut", command=self.Cut, accelerator="Ctrl+X")
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Select All", command=self.SelectAll, accelerator="Ctrl+A")

    def CreateViewMenu(self):
        self.viewMenu = Menu(self.menu, tearoff=0)
        self.viewMenu.add_checkbutton(label="Full Screen", command=self.fullScreen, onvalue=1, offvalue=0,
                                      variable=self.isFullScreen)

    def CreateAboutMenu(self):
        self.aboutMenu = Menu(self.menu, tearoff=0)
        self.aboutMenu.add_checkbutton(label="About", command=self.AboutUs)

    def ConfigureMenus(self):
        # Menu needed variables
        self.isFullScreen = BooleanVar()
        self.isFullScreen.set(False)
        # Our initial Menu
        self.menu = Menu(self.root)
        # Create File Menu
        self.CreateFileSystemMenu()
        # Create the View Menu
        self.CreateViewMenu()
        # Create About Menu
        self.CreateAboutMenu()
        # Create Edit Menu
        self.CreateEditMenu()
        # Cascade the menus
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        self.menu.add_cascade(label="View", menu=self.viewMenu)
        self.menu.add_cascade(label="Help", menu=self.aboutMenu)
        # Assign the menu to the window
        self.root.config(menu=self.menu)

    def CopyPath(self):
        self.codeEditor.clipboard_clear()
        self.codeEditor.clipboard_append(self.filepath)

    def Reload(self):
        if self.filepath == "":
            return  # break if there is no path to load
        try:
            # Open File and get its contents
            self.file = open(self.filepath, encoding="utf-8")
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

    def fullScreen(self):
        if self.isFullScreen.get():
            self.root.attributes('-fullscreen', True)
        else:
            self.root.attributes('-fullscreen', False)

    def CreateWindow(self):
        self.scroll = Scrollbar(self.root)
        self.output = Text(self.root, yscrollcommand=self.scroll.set)
        self.codeEditor = Text(self.root, undo=1, tabs=1, yscrollcommand=self.scroll.set, font=35)
        self.frame = Frame(self.root, bg="grey")
        self.__UpdateTitle()
        self.root.iconbitmap('pyidelogo.ico')
        # Configure the menus
        self.ConfigureMenus()
        # Package all the controls / components
        self.PackageWindow()

    def PackageWindow(self):
        self.frame.pack(side=LEFT, fill=Y)
        self.scroll.pack(side=RIGHT, fill=Y, ipady=140)
        self.codeEditor.pack(fill=BOTH, ipady=10)
        self.scroll.config(command=self.codeEditor.yview)
        self.output.insert("end-1c",
                           "Your output will be shown here\n1.Write your code\n2.Save it\n3.Run")
        self.output.config(state=DISABLED)
        self.scroll.config(command=self.output.yview)
        self.scroll.pack(side=RIGHT, fill=Y, ipady=140)
        self.output.pack(fill=X, side=BOTTOM)
        self.scroll.config(command=self.codeEditor.yview)

    def AboutUs(self):
        messagebox.showinfo("About",
                            "The project is Open Source (available on github) and maintained by Jaspreet Singh")

    def OpenFile(self, event=None):
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

    def SaveFile(self, event=None):
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

    def NewFile(self, event=None):
        self.filepath = ""
        self.filename = "Untitled"
        self.codeEditor.delete(0.0, END)
        self.__UpdateTitle()

    def __UpdateTitle(self):
        # Pretty straight forward. It just changes the title to the current filename
        self.root.title(f"PyIDE - {self.filename}")

    def Run(self, event=None):
        # If the file has not been saved it will attempt to automatically save it
        if not self.SaveFile():
            return  # if the user closes the dialog then return
        self.output.delete('1.0', END)
        self.process = subprocess.Popen(f"py {self.filepath}", stdout=subprocess.PIPE, shell=True,
                                        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        self.out, self.err = self.process.communicate()
        # Show the output
        self.output.config(state=NORMAL)  # Enable writing
        self.output.delete(0.0, END)
        self.output.insert("end-1c", self.out)
        self.output.insert("end-1c", self.err)
        self.output.config(state=DISABLED)  # Make Read-Only

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
        except Exception as e:
            messagebox.showerror("Oops!", f"It seems like something went wrong while trying to save this file | {e}")

    def OpenInExplorer(self):
        # The file explorer needs a filepath with backslashes
        self.newfilepath = self.filepath.replace("/", "\\")
        # Run the command
        subprocess.Popen(rf'explorer /select, "{self.newfilepath}"')

    def Exit(self):
        self.root.destroy()

    def OpenConsole(self):
        self.newfilepath = self.filepath.replace("/", "\\")
        os.system(rf"start cmd /K cd {self.newfilepath}")


if __name__ == "__main__":
    window = PyIDE()
