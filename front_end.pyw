from tkinter import *
from tkinter import ttk
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
        self.simulator.set_input_callback(self.get_char_input)
        self.simulator.set_output_callback(self.console_output)
        self.input_mode = False
        self.input_buffer = ""


    def create_layout(self):
        #icono en binario
        gif_data = b'GIF89a \x00 \x00\x84\x00\x00\xb4\xc6\xc3\xae\xc1\xbeFfw\xfd\xfd\xfd\xa9\xbd\xbc\x8d\xa4\xaa9\\n\xc2\xd2\xcfXu\x84y\x94\x9c\x86\x9b\xa6\xe6\xec\xed\xc0\xca\xd0l\x88\x93\xbe\xd0\xcd=crb}\x8c\x13:Q^\x83\x8c~\x97\xa1\n/H\x1dDW F[*OcUs\x7f\x9e\xb5\xb5\xae\xbd\xc5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x1b\x00,\x00\x00\x00\x00 \x00 \x00@\x08\xff\x00\x01\x08\x0c\x10@\xa0\xc1\x83\x08\x13*\\(P\x80\x02\x05\x03"&H\xf0\xe0@\x03\x08\x08\x18j\x14h`\xc1\x00\x00\x08\x04$p\xb0\x11\x00\x01\x93\x00\n\x0e\x14x\x80%\x00\x92\nU\xae<(saK\x84\x04\n\x94L\xc9\x93\xa3G\x00\x06\x0e\x1c\x10\x00@@\x81\x9b%e&\x10\xc0`\x01\x80\x8f\x08\x11 \x80\xb9\x90`\xcf\xab;\xaf\x9e\xb4\xaa\xb2&\xc3\xae\x06\x0b\x82\x15k\xb0\x81\x80\xb3\x02B\nh`\xf0,\xd5\xac\x04\x04D\xd0\x00\xa0@\x04\x0cK\x17L0p\xe1\xe4\xcc\x9d\x1d?\x06\x15``d\xd6\xb0\x07;.x\x10@h\xd5\x84[g.e@\xb92e\x00\x0c0"\x1c{x\xa7\xd7\xceIQ\xae\xfcL\xf3/V\xb0X;\x7f&]\xa0\xb5k\x9da\x05dP\xe8W\xacL\x03\x0f#\x0eH\xa0\xc0\x00\x80\x03\x12*\xc0\xde\\\xfa\xa0\x00\x08F\x1f\x1a\x90:\xa1A\x01\xb6\xa0\r>\x88\x08\xd4\xa2\x81\x06\x0b\x8cF\xf7)\xd8A\x01\xa9\t\x90\xd2N&\xcd\x1dh\x01\n\x86\xb7\x1b\x0c\xac@B\x81\xb7\x0c\xfd\xa6. \xc0\xc2\x80\x02\n\xd4\xa2u8\xb3\xa0|\xff+%\xd0\x80n\x04\xea\xf6]q\x02\x9d\x14\x19O\xf4\xed\xe7\xe0Y\n\x1cT\x1bJ\n"\xa6\x9e\x85\xa6]\xd8\x93|\xdbYePd\xffu\x08@@\x00;'
  
        tk_icon = PhotoImage(data=gif_data)
        self.master.iconphoto(False, tk_icon)

        space0 = self.create_space0()
        space1 = self.create_space1(space0)
        space2_and_memory = self.create_space2_and_memory(space1)
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
        button0.grid(row=0, column=4, padx=2, pady=2, sticky='wnse')
        button1 = Button(self.space1, text="Load assembly", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.find_assembly(self))
        button1.grid(row=0, column=0, padx=2, pady=2, sticky='wnse')
        button2 = Button(self.space1, text="Save assembly", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.save_assembly(self))
        button2.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')
        button3 = Button(self.space1, text="Load binary", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.find_binary(self))
        button3.grid(row=0, column=2, padx=2, pady=2, sticky='wnse')
        button4 = Button(self.space1, text="Save binary", foreground="white", background="#4B4B4B", command=lambda: self.file_handler.save_binary(self))
        button4.grid(row=0, column=3, padx=2, pady=2, sticky='wnse')
        button5 = Button(self.space1, text="CLEAR ALL", foreground="white", background="#4B4B4B", command=self.clear_all)
        button5.grid(row=0, column=5, padx=2, pady=2, sticky='wnse')
        button6 = Button(self.space1, text="More", foreground="white", background="#4B4B4B", command=self.more)
        button6.grid(row=0, column=6, padx=2, pady=2, sticky='wnse')


        space1 = Frame(self, bg="#3E3E3E")
        space1.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        space1.grid_rowconfigure(0, weight=1)
        space1.grid_columnconfigure(0, weight=1)

        return space1
    
    def more(self):
        messagebox.showinfo(
            "Acerca del Programa",
            "*****************************************************\n"
            "      LICENCIA GNU GENERAL PUBLIC LICENSE (GPL)\n"
            "*****************************************************\n"
            "Este software está licenciado bajo la GPLv3 (2024).\n\n"
            "Desarrollado por: Taeeon, Nicolas, Magno.\n"
            "Testeado a fondo por: Nicolas.\n\n"
            "Eres libre de usar, compartir y modificar este programa\n"
            "mientras respetes los términos de la licencia GPLv3.\n\n"
            "Para más información, consulta nuestra página de GitHub:\n"
            "https://github.com/MrTayon/LCIIIMULATOR"
        )
    
    def create_space2_and_memory(self, space1):
        container = Frame(space1, bg="grey")
        container.pack(side='right', expand=True, fill='both', padx=2, pady=2)

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
        self.console_text.bind("<Key>", self.on_key_press)
        self._input_done = StringVar()

        entry96 = Button(space2_2_1, text=" CLEAR CONSOLE ", foreground="white", background="#4B4B4B",command=self.clear_console)
        entry96.grid(row=0, column=1, padx=22, pady=2, sticky='wnse')


        # MEMORY VIEWER
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#3E3E3E", foreground="white", fieldbackground="#3E3E3E")
        style.map("Treeview", background=[("selected", "#4B4B4B")])

        memory_frame = Frame(container, bg="grey", width=200)
        memory_frame.pack(side='right', expand=True, fill='both', padx=2, pady=2)

        memory_label = Label(memory_frame, text="MEMORY VIEWER", foreground="white", background="#4B4B4B")
        memory_label.pack(side='top', fill='x')

        self.memory_tree = ttk.Treeview(memory_frame, columns=('Address', 'Value'), show='headings', height=20, style="Custom.Treeview")
        self.memory_tree.heading('Address', text='Address')
        self.memory_tree.heading('Value', text='Value')
        self.memory_tree.column('Address', width=80)
        self.memory_tree.column('Value', width=120)
        self.memory_tree.pack(side='left', expand=True, fill='both')

        scrollbar = ttk.Scrollbar(memory_frame, orient="vertical", command=self.memory_tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.memory_tree.configure(yscrollcommand=scrollbar.set)

        return container
    
    def update_memory_viewer(self):
        self.memory_tree.delete(*self.memory_tree.get_children())
        for address, value in sorted(self.simulator.memory.items()):
            self.memory_tree.insert('', 'end', values=(f'x{address:04X}', value))


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
        clear_binary_button = Button(space3_1_1, text=" CLEAR ", foreground="white", background="#4B4B4B", command=self.clear_binary_text)
        clear_binary_button.grid(row=0, column=3, padx=2, pady=2, sticky='wnse')
        entry2 = Button(space3_1_1, text="TO ASSEMBLY", foreground="white", background="#4B4B4B", command=self.binary_to_assembly)
        entry2.grid(row=0, column=4, padx=2, pady=2, sticky='wnse')

        spacer = Label(space3_1_1, text="               ", foreground="grey", background="grey")
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
        clear_assembly_button = Button(space3_2_1, text=" CLEAR ", foreground="white", background="#4B4B4B", command=self.clear_assembly_text)
        clear_assembly_button.grid(row=0, column=3, padx=2, pady=2, sticky='wnse')
        entry4 = Button(space3_2_1, text="TO BINARY", foreground="white", background="#4B4B4B", command=self.assembly_to_binary)
        entry4.grid(row=0, column=4, padx=2, pady=2, sticky='wnse')

        spacer = Label(space3_2_1, text="         ", foreground="grey", background="grey")
        spacer.grid(row=0, column=1, padx=2, pady=2, sticky='wnse')

        space3_2_2 = Frame(space3, bg="grey")
        space3_2_2.pack(side='bottom', expand=True, fill='both', padx=0, pady=0, ipadx=0, ipady=0)

        self.binary_text = Text(space3_2_2, width=20, height=20, font=("Arial", 10), fg="white", bg="#3E3E3E", insertbackground="white")
        self.binary_text.pack(side='bottom', expand=True, fill='both', padx=2, pady=2, ipadx=20)

        return space3

    def on_key_press(self, event):
        if self.input_mode:
            if event.char:
                self.input_buffer = event.char
                self.console_output(event.char + "\n")
                self._input_done.set(True)
            return "break"  # Prevents default key behavior

    def step_execution(self):
        if self.simulator.execute_step():
            self.update_registers()
            self.update_memory_viewer()
            self.update_console(f"Executed instruction at PC: {self.simulator.PC-1:04X}")
        else:
            self.update_console("No more instructions to execute.")
            self.display_instruction_count()
        self.master.update()  # Force update of the GUI

    def run_all(self):
        while self.simulator.execute_step():
            self.update_registers()
            self.update_memory_viewer()
            self.master.update()  # Force update of the GUI after each step
            if not self.simulator.execute_step():
                break
        self.update_console("Execution complete.")
        self.display_instruction_count()

    def display_instruction_count(self):
        count = self.simulator.instruction_count
        message = f"Total instructions executed: {count}"
        self.update_console(message)


    def update_console(self, message):
        self.console_text.config(state="normal")
        self.console_text.insert(END, message + "\n")
        self.console_text.see(END)
        self.console_text.config(state="normal")  # Keep it normal to allow input

    def get_char_input(self, prompt):
        self.input_mode = True
        self.console_output(prompt)
        self.master.wait_variable(self._input_done)
        self.input_mode = False
        char = self.input_buffer
        self.input_buffer = ""
        return char

    def console_output(self, text):
        self.console_text.config(state="normal")
        self.console_text.insert(END, text)
        self.console_text.see(END)
        self.console_text.config(state="normal")  # Keep it normal to allow input
        if text.endswith('\n'):
            self.console_text.insert(END, "\n")  # Add an extra newline for better readability
        self.master.update()  # Force update of the GUI

    def clear_memory_viewer(self):
        # Clear all items from the memory_tree
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)
        
        # Update the console to inform the user
        self.update_console("Memory viewer cleared.")

    def clear_binary_text(self):
        self.binary_text.delete("1.0", END)
        self.update_console("Binary text area cleared.")

    def clear_assembly_text(self):
        self.assembly_text.delete("1.0", END)
        self.update_console("Assembly text area cleared.")

    def clear_all(self):
        self.clear_binary_text()
        self.clear_assembly_text()
        self.reset_registers()
        self.clear_console()

    def reset_registers(self):
        self.simulator.reset_registers()
        self.clear_memory_viewer()
        self.update_registers()
        self.update_memory_viewer()
        self.update_console("Registers and memory reset.")
        self.update_console("Instruction count reset to 0.")

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
        self.clear_memory_viewer()
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
        self.clear_memory_viewer()
        binary_code = self.binary_text.get("1.0", END).strip()
        self.update_console(f"Código Binario recibido:\n{binary_code}")
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

    def clear_console(self):
        self.console_text.config(state="normal")
        self.console_text.delete("1.0", END)
        self.console_text.config(state="disabled")


root = Tk()
root.geometry("800x600")
root.wm_title("LCIIIMULATOR")
app = Application(root)
app.mainloop()
