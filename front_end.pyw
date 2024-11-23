from tkinter import *
from tkinter import messagebox
from back_end import Conversor
from back_end2 import LC3Simulator
from back_end3 import FileHandler

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#4B4B4B")
        self.master = master
        self.pack(expand=True, fill="both")
        self.conversor = Conversor()
        self.simulator = LC3Simulator()
        self.file_handler = FileHandler()
        self.create_layout()

    def create_layout(self):
        icon_image_path = 'image_icon.gif'

        try:
            tk_icon = PhotoImage(file=icon_image_path)
            self.master.iconphoto(False, tk_icon)
        except Exception:
            messagebox.showerror("Error", "Error al cargar el ícono")

        space0 = self.create_space0()
        space1 = self.create_space1(space0)
        space2 = self.create_space2(space1)
        space3 = self.create_space3(space1)

    def create_space0(self):
        space0 = Frame(self, bg="#3E3E3E")
        space0.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        space0.grid_rowconfigure(1, weight=1)
        space0.grid_columnconfigure(0, weight=1)

        return space0
    
    def create_space1(self, space0):
        self.space1 = Frame(space0, bg="grey")
        self.space1.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        button0 = Button(self.space1, text="RESET REGISTER", foreground="white", background="#4B4B4B", command=self.reset_registers)
        button0.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
        button1 = Button(self.space1, text="Find assembly", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.find_assembly(self))
        button1.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')
        button2 = Button(self.space1, text="Save assembly", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.save_assembly(self))
        button2.grid(row=0, column=2, padx=2, pady=2, sticky='wnse')
        button3 = Button(self.space1, text="Find binary", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.find_binary(self))
        button3.grid(row=0, column=3, padx=2, pady=2, sticky='wnse')
        button4 = Button(self.space1, text="Save binary", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.save_binary(self))
        button4.grid(row=0, column=4, padx=2, pady=2, sticky='wnse')
        button5 = Button(self.space1, text="More", foreground="white", background="#4B4B4B", command=self.more)
        button5.grid(row=0, column=5, padx=2, pady=2, sticky='wnse')

        space1 = Frame(self, bg="#3E3E3E")
        space1.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        space1.grid_rowconfigure(0, weight=1)
        space1.grid_columnconfigure(0, weight=1)

        return space1
    
    def more(self):
        messagebox.showerror("information","license by GNU \n developed in 2024")
    
    def create_space2(self, space1):
        space2 = Frame(space1, bg="grey")
        space2.pack(side='right', expand=True, fill='both', padx=2, pady=2, ipadx=0)
        space2_1 = Frame(space2, bg="grey")
        space2_1.pack(side='top', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)
        space2_1_1 = Frame(space2_1, bg="grey")
        space2_1_1.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')

        label = Label(space2_1_1, text=" REGISTERS ", foreground="white", background="#4B4B4B")
        label.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
        entry67 = Button(space2_1_1, text="STEP TO STEP", foreground="white", background="#4B4B4B", command=self.step_execution)
        entry67.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')
        entry68 = Button(space2_1_1, text="RUN ALL", foreground="white", background="#4B4B4B", command=self.run_all)
        entry68.grid(row=0, column=2, padx=2, pady=2, sticky='wnse')

        space2_1_2 = Frame(space2, bg="grey")
        space2_1_2.pack(side='bottom', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)

        self.registers_text = Text(space2, width=15, height=15, font=("Consolas", 10), fg="white", 
            bg="#3E3E3E", insertbackground="white",wrap="word")
        
        self.registers_text.pack(side='top', expand=True, fill='both', padx=2, pady=2, ipadx=10)
        self.registers_text.insert("end", "R0: 0000\nR1: 0000\nR2: 0000\nR3: 0000\nR4: 0000\nR5: 0000\nR6: 0000\nR7: 0000")
        self.registers_text.config(state="disabled")

        space2_2 = Frame(space2, bg="grey")
        space2_2.pack(side='top', expand=True, fill='both', padx=0, pady=0, ipadx=0)
        space2_2_1 = Frame(space2_2, bg="grey")
        space2_2_1.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')

        entry69 = Label(space2_2_1, text=" CONSOLE ", foreground="white", background="#4B4B4B")
        entry69.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')

        space2_2_2 = Frame(space2, bg="grey")
        space2_2_2.pack(side='bottom', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)

        self.console_text = Text(space2_2_2, width=15, height=20, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        self.console_text.pack(side='bottom', expand=True, fill='both', padx=2, pady=2, ipadx=20)

        entry96 = Button(space2_2_1, text=" CLEAR CONSOLE ", foreground="white", background="#4B4B4B",command=self.clear_console)
        entry96.grid(row=0, column=1, padx=22, pady=2, sticky='wnse')

        return space2

    def create_space3(self, space1):
        space3 = Frame(space1, bg="grey")
        space3.pack(side='left', expand=True, fill='both', padx=2, pady=2, ipadx=0)

        # Assembly section
        space3_1 = Frame(space3, bg="grey")
        space3_1.pack(side='top', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)
        space3_1_1 = Frame(space3_1, bg="grey")
        space3_1_1.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')

        entry1 = Label(space3_1_1, text=" BINARY ", foreground="white", background="#4B4B4B")
        entry1.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
        entry2 = Button(space3_1_1, text="TO ASSEMBLY", foreground="white", background="#4B4B4B", command=self.binary_to_assembly)
        entry2.grid(row=0, column=2, padx=2, pady=2, sticky='wnse')

        spacer = Label(space3_1_1, text="                          ", foreground="grey", background="grey")
        spacer.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')

        space3_1_2 = Frame(space3, bg="grey")
        space3_1_2.pack(side='bottom', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)

        self.assembly_text = Text(space3_1_2, width=10, height=15, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        self.assembly_text.pack(side='bottom', expand=True, fill='both', padx=2, pady=2, ipadx=20)

        # Binary section
        space3_2 = Frame(space3, bg="grey")
        space3_2.pack(side='bottom', expand=True, fill='both', padx=0, pady=0, ipadx=0)
        space3_2_1 = Frame(space3_2, bg="grey")
        space3_2_1.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')

        entry3 = Label(space3_2_1, text=" ASSEMBLY ", foreground="white", background="#4B4B4B")
        entry3.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
        entry4 = Button(space3_2_1, text="TO BINARY", foreground="white", background="#4B4B4B", command=self.assembly_to_binary)
        entry4.grid(row=0, column=2, padx=2, pady=2, sticky='wnse')

        spacer = Label(space3_2_1, text="                             ", foreground="grey", background="grey")
        spacer.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')

        space3_2_2 = Frame(space3, bg="grey")
        space3_2_2.pack(side='bottom', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)

        self.binary_text = Text(space3_2_2, width=20, height=20, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        self.binary_text.pack(side='bottom', expand=True, fill='both', padx=2, pady=2, ipadx=20)

        return space3

    def step_execution(self):
        if self.simulator.PC not in self.simulator.memory:
            self.update_console("No hay más instrucciones para ejecutar.")
            return
        
        self.simulator.execute_step()
        self.update_registers()
        self.update_console(f"Ejecutada instrucción en PC: {self.simulator.PC-1:04X}")

    def run_all(self):
        while self.simulator.PC in self.simulator.memory:
            if not self.simulator.execute_step():
                break
        self.update_registers()
        self.update_console("Ejecución completa.")

    def reset_registers(self):
        self.simulator.reset_registers()
        self.update_registers()
        self.update_console("Registros reseteados.")
    def update_registers(self):
        registers_text = "\n".join([f"R{i}: {value:04X}" for i, value in self.simulator.registers.items()])
        registers_text += f"\nPC: {self.simulator.PC:04X}"
        registers_text += f"\nPSR: {self.simulator.PSR:04X}"
        registers_text += f"\nMSR: {self.simulator.MSR:04X}"
        registers_text += f"\nFlags: N={self.simulator.flags['N']} Z={self.simulator.flags['Z']} P={self.simulator.flags['P']}"
        
        self.registers_text.config(state="normal")
        self.registers_text.delete("1.0", END)
        self.registers_text.insert("1.0", registers_text)
        self.registers_text.config(state="disabled")

    def assembly_to_binary(self):
        assembly_code = self.assembly_text.get("1.0", END).strip()
        self.update_console(f"Código Assembly recibido: {assembly_code}")
        if not assembly_code:
            self.update_console("Error: El área de texto de Assembly está vacía.")
            return
        try:
            if any(opcode in assembly_code for opcode in self.conversor.keys):
                binary_code = self.conversor.assembly_to_binary(assembly_code)
                self.binary_text.delete("1.0", END)
                self.binary_text.insert(END, binary_code)
                self.update_console("Conversión de Assembly a Binario completada.")
                
                # Load instructions into the simulator
                self.simulator.load_instructions(binary_code)
                self.update_registers()
            else:
                raise ValueError("El input no parece ser código Assembly válido.")
        except Exception as e:
            self.update_console(f"Error en la conversión de Assembly a Binario: {str(e)}")
            import traceback
            self.update_console(traceback.format_exc())

    def binary_to_assembly(self):
        binary_code = self.binary_text.get("1.0", END).strip()
        self.update_console(f"Código Binario recibido: {binary_code}")
        if not binary_code:
            self.update_console("Error: El área de texto de Binario está vacía.")
            return
        try:
            if all(c in '01' for c in binary_code.replace('\n', '')):
                assembly_code = self.conversor.binary_to_assembly(binary_code)
                self.assembly_text.delete("1.0", END)
                self.assembly_text.insert(END, assembly_code)
                self.update_console("Conversión de Binario a Assembly completada.")
                
                # Load instructions into the simulator
                self.simulator.load_instructions(binary_code)
                self.update_registers()
            else:
                raise ValueError("El input no parece ser código binario válido.")
        except Exception as e:
            self.update_console(f"Error en la conversión de Binario a Assembly: {str(e)}")
            import traceback
            self.update_console(traceback.format_exc())

    def update_console(self, message):
        self.console_text.config(state="normal")
        self.console_text.insert(END, message + "\n")
        self.console_text.see(END)
        self.console_text.config(state="disabled")

    def clear_console(self):
        self.console_text.config(state="normal")
        self.console_text.delete("1.0", END)
        self.console_text.config(state="disabled")


root = Tk()
root.geometry("490x560")
root.wm_title("LCIIIMULATOR")
app = Application(root)
app.mainloop()
