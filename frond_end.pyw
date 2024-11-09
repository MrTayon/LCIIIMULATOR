from tkinter import *
from tkinter import messagebox

class Application(Frame):
    def __init__(self, master=None):

        super().__init__(master, bg="#4B4B4B")
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_layout()

    def create_layout(self):
         
        icon_image_path = 'image_icon.gif'

        try:
            tk_icon = PhotoImage(file=icon_image_path)
            self.master.iconphoto(False, tk_icon)

        except Exception :
            messagebox.showerror("Error", f"Error al cargar el ícono:")


        space0 = self.create_space0()
        space1 = self.create_space1(space0)
        space2 = self.create_space2(space1)
        space3 = self.create_space3(space1)

        #entry = Entry(self.space2, width=16, high = 16, textvariable="entry_var1", font=("Consolas", 9), fg="white", bg="#3E3E3E", insertbackground="white")
        #entry.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')

        #entry = Entry(self.space3, width=16, textvariable="entry_var1", font=("Consolas", 9), fg="white", bg="#3E3E3E", insertbackground="white")
        #entry.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
   

        #space3 = Frame(space0, bg="lightgray")
        #space3.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        
    def create_space0(self):
        space0 = Frame(self, bg="#3E3E3E")
        space0.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        space0.grid_rowconfigure(1, weight=1)
        space0.grid_columnconfigure(0, weight=1)

        return space0
    
    def create_space1(self,space0):

        self.space1 = Frame(space0, bg="grey")
        self.space1.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        entry = Label(self.space1, text="reset", foreground="white", background="#4B4B4B")
        entry.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
        entry = Label(self.space1, text="run", foreground="white", background="#4B4B4B")
        entry.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')
        entry = Label(self.space1, text="more", foreground="white", background="#4B4B4B")
        entry.grid(row=0, column=2, padx=2, pady=2, sticky='wnse')

        space1 = Frame(self, bg="#3E3E3E")
        space1.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        space1.grid_rowconfigure(0, weight=1)
        space1.grid_columnconfigure(0, weight=1)

        return space1
    
    def create_space2(self,space1):
        #space 2 in to space1
        space2 = Frame(space1, bg="grey")
        space2.pack(side = 'right',expand = True,fill='both',padx = 2, pady = 2,ipadx = 0)
        #text entry space
        text_widget3 = Text(space2, width=0, height=20, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        text_widget3.pack(side = 'top',expand = True,fill='both',padx = 2, pady = 2,ipadx = 10)

        return space2

    def create_space3(self,space1):
        
        #space 3 in to space1
        space3 = Frame(space1, bg="grey")
        space3.pack(side = 'left',expand = True,fill='both',padx = 2, pady = 2,ipadx = 0)
        #text entry space
        text_widget = Text(space3, width=10, height=20, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        text_widget.pack(side = 'top',expand = True,fill='both',padx = 2, pady = 2,ipadx = 20)
        text_widget1 = Text(space3, width=20, height=20, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        text_widget1.pack(side = 'bottom',expand = True,fill='both',padx = 2, pady = 2,ipadx = 20)

        return space3


root = Tk()
root.geometry("490x560")
root.wm_title("LCMULATOR")
app = Application(root)
app.mainloop()
