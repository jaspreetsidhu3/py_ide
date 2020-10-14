import subprocess
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import filedialog
root = Tk()
scroll1 = Scrollbar(root)
text1 = Text(root, yscrollcommand=scroll1.set)
frame = Frame(root, bg="grey")


def openfile():
    file_path = filedialog.askopenfilename()

    try:
        with open(file_path, "r+") as f:
            read = f.readlines()
        text.delete('1.0', END)
        for i in read:
            text.insert("end-1c", i)
    except Exception as e:
        messagebox.showerror("Not Supported file format", "Please open .txt file")


def aboutus():
    messagebox.showinfo("Developed by", "Jaspreet Singh")


def run():
    try:
        text1.delete('1.0', END)
        process = subprocess.Popen(f"py {USER_INP}.py", stdout=subprocess.PIPE, shell=True,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        print(process)
        out, err = process.communicate()
        text1.insert("end-1c", out)
    except Exception as e:
        print(e)
        messagebox.showinfo("save it", "Please save before run")


def Submitmenu():
    global USER_INP
    USER_INP = simpledialog.askstring(title="Save as",
                                      prompt="File name ?")

    with open(USER_INP + ".py", "w+") as f:
        f.write(text.get('1.0', END))


if __name__ == '__main__':
    try:
        root.title("HelloWorld")
        menu = Menu(root)
        root.iconbitmap('pyidelogo.ico')
        m1 = Menu(menu, tearoff=0)
        m1.add_command(label="About", command=aboutus)
        m1.add_command(label="Open", command=openfile)
        m1.add_command(label="Run", command=run)
        m1.add_command(label="Save", command=Submitmenu)
        menu.add_cascade(label="File", menu=m1)
        root.config(menu=menu)
        frame.pack(side=LEFT, fill=Y)
        scroll = Scrollbar(root)
        text = Text(root, undo=1, tabs=1, yscrollcommand=scroll.set, font=35)
        scroll.pack(side=RIGHT, fill=Y, ipady=140)
        text.pack(fill=BOTH, ipady=10)
        scroll.config(command=text.yview)
        text1.insert("end-1c",
                     "Your output will be shown here\n1.Write your code above\n2.Save it\n3.Run\n *Please don't type here*")
        scroll1.config(command=text1.yview)
        scroll1.pack(side=RIGHT, fill=Y, ipady=140)
        text1.pack(fill=X, side=BOTTOM)

        root.mainloop()
    except Exception as e:
        print(e)
        text1.insert("end-1c", e)
