#!usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import time
import sys
import platform
import Tkinter as tk
import pygmyplot # pip install pygmyplot
import ScrolledText
from multiprocessing import Process  
from threading import Thread
import json
from PIL import ImageTk
from app.func import *
import Tix as tix
import textwrap

class HoverInfo():
    """Allow to display an info window near a Tkinter widget. Based on
    ToolTipBase object from evandrix (idlelib)
    
    Parameters
    ----------
        master : Tkinter widget
        text : str
            Text to display in the info window.
        width : int
            Max width of the info window in character length. Default 40.
        duration : int
            Time in ms to wait before seing the info window to popup.
    """
    def __init__(self, master, text='', width=40, duration=1000):
        self.master = master
        if not isinstance(text, str):
            raise ValueError('"text" parameter must be a string')
        if not isinstance(duration, int):
            raise ValueError('"duration" parameter must be an integer')
        if not isinstance(width, int):
            raise ValueError('"width" parameter must be an integer')
        self.text_info = text
        self.width = width
        self.duration = duration
        self.infowindow = None
        self.id = None
        self.x = self.y = 0
        self._id1 = self.master.bind('<Enter>', self.enter)
        self._id2 = self.master.bind('<Leave>', self.leave)
        self._id3 = self.master.bind('<ButtonPress>', self.leave)
 
    def enter(self, event=None):
        self.schedule()
 
    def leave(self, event=None):
        self.unschedule()
        self.hideinfo()
 
    def schedule(self):
        self.unschedule()
        self.id = self.master.after(self.duration, self.showinfo)
 
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.master.after_cancel(id)
 
    def showinfo(self):
        if self.infowindow:
            return
        # Place the infowindow outside the master
        x = self.master.winfo_rootx() + 20
        y = self.master.winfo_rooty() + self.master.winfo_height() + 1
        self.infowindow = tw = tk.Toplevel(self.master)
        tw.wm_overrideredirect(1)
        tw.wm_geometry('+%d+%d' % (x, y))
        # Wrap text_info to avoid too large infowindow
        _text = '\n'.join(textwrap.wrap(self.text_info, width=self.width))
        label = tk.Label(self.infowindow, text=_text, justify='left',font=("Helvetica", 10),
                         background="lemonchiffon", borderwidth=1.5, fg='black')
        label.pack()
 
    def hideinfo(self):
        tw = self.infowindow
        self.infowindow = None
        if tw:
            tw.destroy()

class RedirectText(Thread):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor"""
        Thread.__init__(self)
        self.output = text_ctrl
 
    #----------------------------------------------------------------------
    def write(self, string):
        """"""
        self.output.insert(END, string)
        self.output.see(END)
        self.output.update_idletasks()
    def flush(self):
        sys.__stdout__.flush()
        
class Application(Frame):
    from app.func import plot,new_file,search_for,show_info_bar,update_line_number,theme 
    from app.func import highlight_line,undo_highlight,toggle_highlight,select00,select01
    from app.func import select02,select03,select04,select07,select08,select09,select10,popup
    from app.func import save,save_as,undo,redo,cut,copy,paste,select_all,data_up,exit_editor
    from app.func import Draw,save1,save2,save3,save4,save5,new1,new2,new3,new4,new5
    from app.func import on_find,open_file
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        self.root = Tk()
        self.root.title('Sotution of the Transport Equation by Multigroup Methods')
        self.root.geometry("980x655+250+50")
        #self.root.config(bg='blue')
        #self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        #self.root.rowconfigure(2, weight=1)
        #self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(7, weight=1)
        
        # Color GUI
        self.pientur = 'white' # '#66ff00'#'#000033'  #'#00ff00'
        self.labell  = 'grey76'  # '#99ccff' 
        self.boutton = 'grey76' #grey50
        #/////////////////////////////////////////////////////////////////////////////////////////
        self.root2 = LabelFrame(self.root,relief=RAISED,borderwidth=4,bg='blue')
        # SUNKEN, RAISED, GROOVE, and RIDGE
        self.root2.grid(row=0, column=0,columnspan=7,rowspan=8,sticky=NSEW) 
        self.root2.columnconfigure(1, weight=1)
        self.root2.rowconfigure(7, weight=1)
        #self.update_clock()
        #/////////////////////////////////////////////////////////////////////////////////////////
        # construction Frame01
        Frame01 = LabelFrame(self.root2, width=500, height=40, text="Calculation Method",
                             fg='blue',font=("Helvetica", 10),bg=self.pientur)
        Frame01.grid(row=1, column=0,columnspan=4,sticky=NSEW) 
        self.value00 = StringVar()
        self.value01 = StringVar()
        self.value02 = StringVar()
        self.value03 = StringVar()
        self.value04 = StringVar()
        self.value00.set(open('app/link/script00.py', "r" ).read())
        self.value01.set(open('app/link/script01.py', "r" ).read())
        self.value02.set(open('app/link/script02.py', "r" ).read())
        self.value03.set(open('app/link/script03.py', "r" ).read())
        self.value04.set(open('app/link/script04.py', "r" ).read())
        msg1 = ['Collision Probability (CP) Method','Discrete Ordinates (SN) Method','Method Of Characteristics (MOC)']
        self.button = [0]*3
        for (n,method,value,select) in [(0, '   CP      ',self.value00,self.select00),(1, '   Sn      ',self.value01,self.select01),
                                        (2, 'MOC    ',self.value02,self.select02)]:
                                        
            
            self.button[n] = Checkbutton(Frame01, text=method, font='Times',relief='raised',borderwidth=4)
            self.button[n].config(variable=value, onvalue="1",command=select)
            self.button[n].config(height=1, width=8) 
            self.button[n].config(bg='gray76' , fg='black',highlightbackground='blue')
            self.button[n].grid(row =0, column =n ,sticky=NSEW)
            hover = HoverInfo(self.button[n], msg1[n])
        #/////////////////////////////////////////////////////////////////////////////////////////
        # construction Frame02
        Frame02 = LabelFrame(self.root2, width=155, height=40 , text="Input Parametres",font=("Helvetica", 10), 
                             fg='blue', bg=self.pientur)
        Frame02.grid(row=2, column=0,rowspan=4 , sticky=NSEW)
       
        self.value07 = StringVar()
        self.value07.set(open('app/link/script07.py', "r" ).read())
        self.lab0 = [0]*5
        self.ent0 = [0]*5
        for (n,field)  in [(0, 'Energy Group Number'),(1, 'Number of Regions'),
                           (2, 'Number of Materials'),(3, 'Angular Discretization'),
                           (4, 'Legendre Order') ]:
            Frame20 = LabelFrame(Frame02, width=155, height=40, bg=self.pientur)
            Frame20.grid(row=n, column=0, sticky=NSEW)
            self.lab0[n] = Label(Frame20, width=18,height=1, text=field, anchor='w',bg=self.labell)
            if n == 3 :
                self.ent0[n] = Spinbox(Frame20, width=6,from_=0, to=5000,increment=2)
            else:
                self.ent0[n] = Spinbox(Frame20, width=6,from_=0, to=5000)
            self.lab0[n].grid(row=n, column=0,sticky=NSEW)
            self.ent0[n].grid(row=n, column=1,sticky=NSEW)
        if  int(self.value00.get())==1:
            self.button[0].config(bg='#00ffff') 
        if  int(self.value01.get())==1:
            self.button[1].config(bg='#00ffff')
        if  int(self.value02.get())==1:
            self.button[2].config(bg='#00ffff')

 
        
        self.Delta  = [0]*1
        self.NFMR   = [0]*1
        self.REGMAT = [0]*1
        self.SigT   = [[0]*1]*1
        self.NuSigF = [[0]*1]*1
        self.SigS   = [[[0]*1]*1]*1
        self.Chi    = [[0]*1]*1
        self.Vect1  = [0]*1
        self.Vect2  = [0]*1
        self.Vect3  = [0]*1
        self.Vect4  = [0]*1
        button = [0]*4
        self.img1 = ImageTk.PhotoImage(file='app/icons/SigT.png')
        self.img2 = ImageTk.PhotoImage(file='app/icons/SigF.png')
        self.img3 = ImageTk.PhotoImage(file='app/icons/SigS.png')
        self.img4 = ImageTk.PhotoImage(file='app/icons/Chi.png')
        for (n,controle,com,field) in [(5, 'Insert',self.new1, 'Size/NFMR/Materials'),
                             (6, 'Insert',self.new2, self.img1),(7, 'Insert',self.new3, self.img2),
                             (8, 'Insert',self.new4,self.img3),(9, 'Insert',self.new5,self.img4)]:
            Frame20 = LabelFrame(Frame02, width=155, height=40, bg=self.pientur)
            Frame20.grid(row=n, column=0, sticky=NSEW)
            if n==5:
                self.lab = Label(Frame20,width=18, text=field, anchor='w',bg=self.labell)
            else:
                self.lab = Label(Frame20,width=145, image=field)
            button = Button(Frame20, text=controle, font='Times', relief='raised',borderwidth=4)
            button.config(command=com)
            button.config(bg=self.boutton , fg='black')
            button.config(height=1, width=4)
            button.grid(row =n, column =1,sticky=NSEW)
            self.lab.grid(row=n, column=0,sticky=NSEW)
        #/////////////////////////////////////////////////////////////////////////////////////////
        Frame03 = LabelFrame(self.root2, width=155, height=40, text="Iteration Parameters",
                            font=("Helvetica", 10), fg='blue', bg=self.pientur)
        Frame03.grid(row=6, column=0, sticky=NSEW)
       
        self.lab1 = [0]*3
        self.ent1 = [0]*3            
        number = IntVar()
        for (n,field,number)  in [(0, 'Maximum Iterations',200),(1, 'Tolerance keff',1e-6),
                           (2, 'Tolerance Flux',1e-6)]:
            Frame20 = LabelFrame(Frame03, width=155, height=40, bg=self.pientur)
            Frame20.grid(row=n, column=0, sticky=NSEW)
            
            self.lab1[n] = Label(Frame20, width=18,height=1, text=field, anchor='w',bg=self.labell)
            if n==1:
                self.ent1[n] = Spinbox(Frame20, width=6,from_=0.00000001, to=0.000001,
                                       increment=0.0000009,textvariable=number)
                self.ent1[n].delete(0,'end')
                self.ent1[n].insert(0,number)
                self.lab1[n].grid(row=n, column=0,sticky=NSEW)
                self.ent1[n].grid(row=n, column=1,sticky=NSEW)
            elif n==0:
                self.ent1[n] = Spinbox(Frame20, width=6,from_=0, to=100000,textvariable=number)
                self.ent1[n].delete(0,'end')
                self.ent1[n].insert(0,number)
                self.lab1[n].grid(row=n, column=0,sticky=NSEW)
                self.ent1[n].grid(row=n, column=1,sticky=NSEW)
            else:
                self.ent1[n] = Spinbox(Frame20, width=6,from_=0.00000001, to=0.000001,
                                       increment=0.0000009,textvariable=number)
                self.ent1[n].delete(0,'end')
                self.ent1[n].insert(0,number)
                self.lab1[n].grid(row=n, column=0,sticky=NSEW)
                self.ent1[n].grid(row=n, column=1,sticky=NSEW)
            
        Frame04 = LabelFrame(self.root2, width=155, height=40, text="Generate Input",
                            font=("Helvetica", 10), fg='blue', bg=self.pientur)
        Frame04.grid(row=7, column=0, sticky=NSEW)
        b1 = Button(Frame04, text ='Data Up', command =self.data_up,relief='raised',borderwidth=4)
        b1.config(width=23)
        b1.config(bg=self.labell , fg='black',highlightbackground='blue')
        b1.grid(row =0, column =0,sticky=EW)
        #/////////////////////////////////////////////////////////////////////////////////////////
        # construction Frame04
        Frame04 = LabelFrame(self.root2, width=155, height=40, text="Boundary conditions",
                            font=("Helvetica", 10), fg='blue',bg=self.pientur)
        Frame04.grid(row=2, column=3, sticky=NSEW)
        self.value08 = StringVar()
        self.value08.set(open('app/link/script08.py', "r" ).read())
        button = [0]*4
        for (n,boundary,boun) in [(0, 'Vacuum                     ',"vacuum"),
                                  (1, 'Reflective                   ',"reflective"),
                                  (2, 'Vacuum Reflective      ',"vacuum_reflective"),
                                  (3, 'Reflective Vacuum      ',"reflective_vacuum")]:
        
         
            button[n] = Radiobutton(Frame04, text=boundary,relief='raised')
            button[n].config(variable=self.value08, value=boun,command=self.select08)
            button[n].config(bg=self.labell , fg='black',highlightbackground='blue')
            button[n].config(height=2,width=18)
            button[n].grid(row =n, column =0,sticky=NSEW)

        #/////////////////////////////////////////////////////////////////////////////////////////
        Frame09 = LabelFrame(self.root2, width=50, height=40, text="Approximation Scheme",
                             font=("Helvetica", 10), fg='blue',bg=self.pientur)
        Frame09.grid(row=3, column=3,sticky=NSEW)
        self.value09 = StringVar()
        self.value09.set(open('app/link/script09.py', "r" ).read())
        # initial value
        self.value09.set('Diamond Difference')
        choices = ['Diamond Difference','Step Difference   ']
        self.option = OptionMenu(Frame09, self.value09, *choices,  command =self.select09)
        self.option["menu"].config(foreground='black')
        self.option.config(height=2, width=16,highlightbackground='blue')
        self.option.grid(row=0, column=0, sticky=NSEW)
        hover = HoverInfo(self.option, 'Choose Discritization Scheme for the Discrete Ordinates (SN) Method') 
        #-----------------------------------------------------------------------------------------
        self.value10 = StringVar()
        self.value10.set(open('app/link/script10.py', "r" ).read())
        # initial value
        self.value10.set('Step Characteristics')
        choices = ['Step Characteristics','DD0','DD1']
        self.option = OptionMenu(Frame09, self.value10, *choices,  command =self.select10)
        self.option["menu"].config(foreground='black')
        self.option.config(height=2, width=16,highlightbackground='blue')
        self.option.grid(row=1, column=0, sticky=NSEW)
        hover = HoverInfo(self.option, 'Choose Discritization Scheme for the Method Of Characteristics (MOC)') 
        #/////////////////////////////////////////////////////////////////////////////////////////
        Frame10 = LabelFrame(self.root2, width=50, height=40, text="Geometry Visualization",
                            font=("Helvetica", 10), fg='blue',bg=self.pientur)
        Frame10.grid(row=4, column=3,sticky=NSEW)

        b1 = Button(Frame10, text ='Apply', command =self.Draw,relief='raised',borderwidth=4)
        b1.config(width=17)
        b1.config(bg=self.labell , fg='black',highlightbackground='blue')
        #b1.config(state="disabled")
        b1.grid(row =4, column =3,sticky=NSEW)

        style = ttk.Style()
        style.configure('.', font=('Times', 11),fg='blue')
        Frame05 = LabelFrame(self.root2, width=600,  height=286, text="Notebooks",
                            font=("Helvetica", 10), fg='blue', bg=self.pientur)
        Frame05.grid(row=2, column=1, rowspan=6, columnspan=2,sticky=NSEW)

        notebook = ttk.Notebook(Frame05, width=600, height=286)
        framenotebook1 = Frame(notebook)
        framenotebook2 = Frame(notebook)
        notebook.add(framenotebook1, text=' Terminal   ')
        notebook.add(framenotebook2, text=' Text editor')
        notebook.pack(expand=YES, fill=BOTH)
        
        self.output = Text(framenotebook1,background = 'white', fg='black', bg=self.pientur)
        self.output.bind("<Key>", lambda e: "break")
        self.output.configure(state='normal')
        self.output.pack(expand=YES, fill=BOTH)
        scrollbar = Scrollbar(self.output)
        self.output.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        #redirect stdout
        redir = RedirectText(self.output)
        sys.stdout = redir
        self.output.bind("<1>", lambda event: self.output.focus_set())

        Frame07 = LabelFrame(self.root2, width=50, height=40, text="Controls",
                            font=("Helvetica", 10), fg='blue',bg=self.pientur)
        Frame07.grid(row=5, column=3,rowspan=3,sticky=NSEW )
        

        button = [0]*3
        for (n,controle,com) in [(0, 'Compile',compile),(1, 'Run',run),
                             (2, 'Plot',self.plot)]:  
       
            button[n] = Button(Frame07, text=controle, font='Times', relief='raised',borderwidth=4)
            button[n].config(command = com)
            button[n].config(bg=self.labell , fg='black',highlightbackground='blue')
            button[n].config(height=1, width=17, activebackground ='#00ffff')
            button[n].grid(row =n, column =3,sticky=NSEW)
        ######################################################################
        #defining icons for compund menu demonstration
        self.eyeicon = PhotoImage(file='app/icons/eye.gif')
        self.ploticon = PhotoImage(file='app/icons/self.plot.gif')
        self.runicon = PhotoImage(file='app/icons/run.gif')
        self.geoicon = PhotoImage(file='app/icons/geometry.gif')
        self.slabicon = PhotoImage(file='app/icons/slab.gif')
        self.sphereicon = PhotoImage(file='app/icons/sphere.gif')
        self.cylindericon = PhotoImage(file='app/icons/cylinder.gif')
        self.compileicon = PhotoImage(file='app/icons/compile.gif')
        self.newicon = PhotoImage(file='app/icons/self.new_file.gif')
        self.openicon = PhotoImage(file='app/icons/self.open_file.gif')
        self.saveicon = PhotoImage(file='app/icons/self.save.gif')
        self.saveasicon = PhotoImage(file='app/icons/self.save_as.gif')
        self.exiticon = PhotoImage(file='app/icons/self.exit_editor.gif')
        self.cuticon = PhotoImage(file='app/icons/self.cut.gif')
        self.copyicon = PhotoImage(file='app/icons/self.copy.gif')
        self.pasteicon = PhotoImage(file='app/icons/self.paste.gif')
        self.undoicon = PhotoImage(file='app/icons/self.undo.gif')
        self.redoicon = PhotoImage(file='app/icons/self.redo.gif')
        self.findicon = PhotoImage(file='app/icons/self.on_find.gif')
        self.abouticon = PhotoImage(file='app/icons/about.gif')
        self.helpicon = PhotoImage(file='app/icons/help_box.gif')

        #Define a menu bar
        menubar = Menu(self.root2)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Compile", accelerator='Ctrl+E', compound=LEFT, image=self.compileicon, underline=0)
        filemenu.add_command(label="Run", accelerator='Ctrl+R', compound=LEFT, image=self.runicon, underline=0)
        filemenu.add_command(label="Plot", accelerator='Ctrl+P', compound=LEFT, image=self.ploticon, underline=0)
        submenu = Menu(menubar, tearoff=0)
        submenu.add_command(label="Slab", compound=LEFT, image=self.slabicon, underline=0)
        submenu.add_command(label="Sphere", compound=LEFT, image=self.sphereicon, underline=0)
        submenu.add_command(label="Cylinder", compound=LEFT, image=self.cylindericon, underline=0)
        filemenu.add_cascade(label="Geometry", accelerator='Ctrl+G', compound=LEFT, image=self.geoicon, menu=submenu, underline=0)
        


        filemenu.add_separator()
        filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=self.newicon, underline=0, command=self.new_file)
        filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=self.openicon, underline=0, command=self.open_file)
        filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=self.saveicon, underline=0, command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S',compound=LEFT, image=self.saveasicon, underline=0,  command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", accelerator='Alt+F4',compound=LEFT, image=self.exiticon, underline=0, command=self.exit_editor)
        menubar.add_cascade(label="File", menu=filemenu) 

        #Edit menu
        editmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Undo", compound=LEFT, image=self.undoicon, accelerator='Ctrl+Z', command=self.undo)
        editmenu.add_command(label="Redo", compound=LEFT, image=self.redoicon, accelerator='Ctrl+Y', command=self.redo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", compound=LEFT, image=self.cuticon, accelerator='Ctrl+X', command=self.cut)
        editmenu.add_command(label="Copy", compound=LEFT, image=self.copyicon, accelerator='Ctrl+C', command=self.copy)
        editmenu.add_command(labe="Paste", compound=LEFT, image=self.pasteicon, accelerator='Ctrl+V', command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="Find", compound=LEFT, image=self.findicon, underline=0, accelerator='Ctrl+F', command=self.on_find)
        editmenu.add_separator()
        editmenu.add_command(label="Select All", accelerator='Ctrl+A', underline=0, command=self.select_all)

        #View menu

        viewmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=viewmenu)
        self.showln = IntVar()
        self.showln.set(1)
        viewmenu.add_checkbutton(label="Show Line Number", variable=self.showln)
        self.showinbar = IntVar()
        self.showinbar.set(1)
        viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=self.showinbar)
        self.hltln = IntVar()
        viewmenu.add_checkbutton(label="Highlight Current Line", variable=self.hltln)
        themesmenu = Menu(viewmenu, tearoff=0)
        viewmenu.add_cascade(label="Themes",compound=LEFT, image=self.eyeicon, menu=themesmenu)

        #we define a color scheme dictionary containg name and color code as key value pair
        self.clrschms = {
        '1. Default White': '000000.FFFFFF',
        '2. Greygarious Grey':'83406A.D1D4D1',
        '3. Lovely Lavender':'202B4B.E1E1FF' , 
        '4. Aquamarine': '5B8340.D1E7E0',
        '5. Bold Beige': '4B4620.FFF0E1',
        '6. Cobalt Blue':'ffffBB.3333aa',
        '7. Olive Green': 'D1E7E0.5B8340',
        }
        self.themechoice= StringVar()
        self.themechoice.set('1. Default White')
        for k in sorted(self.clrschms):
            themesmenu.add_radiobutton(label=k, variable=self.themechoice, command=self.theme)

        #About menu
        aboutmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About" ,menu=aboutmenu)
        aboutmenu.add_command(label="About",compound=LEFT,image=self.abouticon, command=about)
        aboutmenu.add_command(label="Help",compound=LEFT,image=self.helpicon, command=help_box)

        #shortcut bar and line number 
        shortcutbar = Frame(self.root2, height=25,bg=self.pientur)
        icons = ['geometry','compile','run','self.plot','self.new_file','self.open_file',
                'self.save','self.save_as','self.exit_editor', 'self.cut', 'self.copy', 
                'self.paste', 'self.undo', 'self.redo', 'self.on_find', 'about','help_box']
        msg = ['Geometry','Call the F2PY –Fortran to Python interface generator– \
                is to provide a connection between Python and Fortran languages. ',
                'Solve Multi-Group Scheme','Plot Scalar Flux','Create new data file',
                'Open data file','Save data file','Save as data file','Close window', 'Cut', 'Copy', 
                'Paste', 'Undo', 'Redo', 'Search in data file', 'About','Help']
        toolbar = [0]*17
        for i, icon in enumerate(icons):
            tbicon = PhotoImage(file='app/icons/'+icon+'.gif')
            cmd = eval(icon)
            toolbar[i] = Button(shortcutbar, image=tbicon,  command=cmd,bg=self.pientur)
            toolbar[i].image = tbicon  
            toolbar[i].pack(side=LEFT)
            hover = HoverInfo(toolbar[i], msg[i])
        shortcutbar.grid(row=0,column=0,columnspan=4,sticky=NSEW)

        #Text widget and scrollbar widget
        #####################################
        self.textPad = Text(framenotebook2, undo=True)
        self.textPad.pack(expand=YES, fill=BOTH)
        scroll=Scrollbar(self.textPad)
        self.textPad.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.textPad.yview)
        scroll.pack(side=RIGHT, fill=Y)

        #Info Bar
        self.infobar = Label(self.textPad, text='Line: 1 | Column:0')
        self.infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')

        #context popup menu
        self.cmenu = Menu(self.output,tearoff=0)
        for i in ('run','self.plot','self.cut', 'self.copy', 'self.paste', 'self.undo', 'self.redo'):
            cmd = eval(i)
            self.cmenu.add_command(label=i, compound=LEFT, command=cmd)  
        self.cmenu.add_separator()
        self.cmenu.add_command(label='Select All', underline=7, command=self.select_all)
        self.output.bind("<Button-3>", self.popup)
        
        #Binding events
        self.output.bind('<Control-P>', self.plot)
        self.output.bind('<Control-p>', self.plot)
        self.output.bind('<Control-R>', run)
        self.output.bind('<Control-r>', run)
        self.output.bind('<Control-N>', self.new_file)
        self.output.bind('<Control-n>', self.new_file)
        self.output.bind('<Control-O>', self.open_file)
        self.output.bind('<Control-o>', self.open_file)
        self.output.bind('<Control-S>', self.save)
        self.output.bind('<Control-s>', self.save)
        self.output.bind('<Control-A>', self.select_all)
        self.output.bind('<Control-a>', self.select_all)
        self.output.bind('<Control-f>', self.on_find)
        self.output.bind('<Control-F>', self.on_find)
        self.output.bind('<KeyPress-F1>', help_box)

        self.output.bind("<Any-KeyPress>", self.update_line_number)
        self.output.tag_configure("active_line", background="ivory2")

        self.cmenu = Menu(self.textPad,tearoff=0)
        for i in ('run','self.plot','self.cut', 'self.copy', 'self.paste', 'self.undo', 'self.redo'):
            cmd = eval(i)
            self.cmenu.add_command(label=i, compound=LEFT, command=cmd)  
        self.cmenu.add_separator()
        self.cmenu.add_command(label='Select All', underline=7, command=self.select_all)
        self.textPad.bind("<Button-3>", self.popup)
        
        #Binding events
        self.textPad.bind('<Control-P>', self.plot)
        self.textPad.bind('<Control-p>', self.plot)
        self.textPad.bind('<Control-R>', run)
        self.textPad.bind('<Control-r>', run)
        self.textPad.bind('<Control-N>', self.new_file)
        self.textPad.bind('<Control-n>', self.new_file)
        self.textPad.bind('<Control-O>', self.open_file)
        self.textPad.bind('<Control-o>', self.open_file)
        self.textPad.bind('<Control-S>', self.save)
        self.textPad.bind('<Control-s>', self.save)
        self.textPad.bind('<Control-A>', self.select_all)
        self.textPad.bind('<Control-a>', self.select_all)
        self.textPad.bind('<Control-f>', self.on_find)
        self.textPad.bind('<Control-F>', self.on_find)
        self.textPad.bind('<KeyPress-F1>', help_box)

        self.textPad.bind("<Any-KeyPress>", self.update_line_number)
        self.textPad.tag_configure("active_line", background="ivory2")

        Frame08 = Frame(self.root2, width=50, height=40)
        Frame08.grid(row=8, column=0, columnspan=4, sticky=NSEW )
        v1 = "System",":", platform.system(),platform.dist()
        v2 = "Python",":", platform.python_version()
        v3 = "Tkinter",":",tk.TkVersion
        for (n,version) in [(3,v1),(4,v2),(5,v3)]:
            barreEtat = Label(Frame08, text=version, bd=2, anchor=W)
            barreEtat.grid(row=8,column=n)
# Programme principal :
if __name__ == '__main__':
    app = Application() 
    app.root.mainloop()
