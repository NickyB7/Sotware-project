from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

root = Tk()
root.geometry('800x500')
root.title('Python - Notepad')
root.iconbitmap('icons/pypad.ico')


def popup(event, cmenu=None):
    cmenu.tk_popup(event.x_root, event.y_root, 0)

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    elif not val:
        infobar.pack_forget()


def update_line_number(event=None):
    txt = ''
    if showln.get():
        endline, endcolumn = textPad.index('end-1c').split('.')
        txt = '\n'.join(map(str, range(1, int(endline))))
    lnlabel.config(text=txt, anchor='nw')
    currline, curcolumn = textPad.index("insert").split('.')
    infobar.config(text='Line: %s | Column: %s' % (currline, curcolumn))


def highlight_line(interval=100):
    textPad.tag_remove("active_line", 1.0, "end")
    textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
    textPad.after(interval, toggle_highlight)


def undo_highlight():
    textPad.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()

def exit_editor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', exit_editor)


def select_all(event=None):
    textPad.tag_add('sel', '1.0', 'end')


def on_find(event=None):
    t2 = Toplevel(root)
    t2.title('Find')
    t2.geometry('300x65+200+250')
    t2.transient(root)
    Label(t2, text="Find All:").grid(row=0, column=0, pady=4, sticky='e')
    v = StringVar()
    e = Entry(t2, width=25, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
    c = IntVar()
    Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(t2, text='Find All', underline=0, command=lambda: search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0,
                                                                                                                column=2,
                                                                                                                sticky='e' + 'w',
                                                                                                                padx=2,
                                                                                                                pady=4)

    def close_search():
        textPad.tag_remove('match', '1.0', END)
        t2.destroy()

    t2.protocol('WM_DELETE_WINDOW', close_search)


def search_for(needle, cssnstv, textPad, t2, e):
    textPad.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
            if not pos: break
            lastpos = '%s+%dc' % (pos, len(needle))
            textPad.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
        textPad.tag_config('match', foreground='red', background='yellow')
    e.focus_set()
    t2.title('%d matches found' % count)


def undo():
    textPad.event_generate("<<Undo>>")
    update_line_number()


def redo():
    textPad.event_generate("<<Redo>>")
    update_line_number()


def cut():
    textPad.event_generate("<<Cut>>")
    update_line_number()


def copy():
    textPad.event_generate("<<Copy>>")
    update_line_number()


def paste():
    textPad.event_generate("<<Paste>>")
    update_line_number()


def new_file(event=None):
    global filename
    filename = None
    root.title("Untitled - Tkeditor")
    textPad.delete(1.0, END)
    update_line_number()


def open_file(event=None):
    global filename
    filename = filedialog.askopenfilename(defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if filename == "":
        filename = None
    else:
        root.title(os.path.basename(filename) + " - Tkeditor")
        textPad.delete(1.0, END)
        fh = open(filename, "r")
        textPad.insert(1.0, fh.read())
        fh.close()
    update_line_number()


def save(event=None):
    global filename
    try:
        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
    except:
        save_as()


def save_as():
    try:

        f = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        fh = open(f, 'w')
        global filename
        filename = f
        textoutput = textPad.get(1.0, END)
        fh.write(textoutput)
        fh.close()
        root.title(os.path.basename(f) + " - Tkeditor")
    except:
        pass



# icons
newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file='icons/open_file.gif')
saveicon = PhotoImage(file='icons/Save.gif')
cuticon = PhotoImage(file='icons/Cut.gif')
copyicon = PhotoImage(file='icons/Copy.gif')
pasteicon = PhotoImage(file='icons/Paste.gif')
undoicon = PhotoImage(file='icons/Undo.gif')
redoicon = PhotoImage(file='icons/Redo.gif')


menubar = Menu(root)


filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command=new_file)
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=openicon, underline=0, command=open_file)
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command=save)
filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S', command=save_as)
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_editor)
menubar.add_cascade(label="File", menu=filemenu)


editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", compound=LEFT, image=undoicon, accelerator='Ctrl+Z', command=undo)
editmenu.add_command(label="Redo", compound=LEFT, image=redoicon, accelerator='Ctrl+Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", compound=LEFT, image=cuticon, accelerator='Ctrl+X', command=cut)
editmenu.add_command(label="Copy", compound=LEFT, image=copyicon, accelerator='Ctrl+C', command=copy)
editmenu.add_command(labe="Paste", compound=LEFT, image=pasteicon, accelerator='Ctrl+V', command=paste)
editmenu.add_separator()
editmenu.add_command(label="Find", underline=0, accelerator='Ctrl+F', command=on_find)
editmenu.add_separator()
editmenu.add_command(label="Select All", accelerator='Ctrl+A', underline=7, command=select_all)


viewmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="Show Line Number", variable=showln)
showinbar = IntVar()
showinbar.set(1)
viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
viewmenu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=toggle_highlight)

root.config(menu=menubar)

lnlabel = Label(root, width=2, bg='antique white')
lnlabel.pack(side=LEFT, fill=Y)


textPad = Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)


infobar = Label(textPad, text='Line: 1 | Column:0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

textPad.bind('<Control-N>', new_file)
textPad.bind('<Control-n>', new_file)
textPad.bind('<Control-O>', open_file)
textPad.bind('<Control-o>', open_file)
textPad.bind('<Control-S>', save)
textPad.bind('<Control-s>', save)
textPad.bind('<Control-A>', select_all)
textPad.bind('<Control-a>', select_all)
textPad.bind('<Control-f>', on_find)
textPad.bind('<Control-F>', on_find)


textPad.bind("<Any-KeyPress>", update_line_number)
textPad.tag_configure("active_line", background="ivory2")
root.mainloop()

