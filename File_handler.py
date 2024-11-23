from tkinter import filedialog
import os

class FileHandler:
    @staticmethod
    def find_assembly(self):
        """Load assembly code from a file"""
        filetypes = [('Assembly files', '*.asm'), ('Text files', '*.txt'), ('All files', '*.*')]
        filename = filedialog.askopenfilename(
            title='Open Assembly File',
            filetypes=filetypes,
            initialdir=os.getcwd()
        )
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    self.assembly_text.delete('1.0', 'end')
                    self.assembly_text.insert('1.0', content)
                    self.update_console(f"Loaded assembly from: {filename}")
            except Exception as e:
                self.update_console(f"Error loading file: {str(e)}")

    @staticmethod
    def save_assembly(self):
        """Save assembly code to a file"""
        content = self.assembly_text.get('1.0', 'end').strip()
        if not content:
            self.update_console("No assembly code to save")
            return
            
        filetypes = [('Assembly files', '*.asm'), ('Text files', '*.txt'), ('All files', '*.*')]
        filename = filedialog.asksaveasfilename(
            title='Save Assembly File',
            filetypes=filetypes,
            defaultextension=".asm",
            initialdir=os.getcwd()
        )
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(content)
                    self.update_console(f"Saved assembly to: {filename}")
            except Exception as e:
                self.update_console(f"Error saving file: {str(e)}")

    @staticmethod
    def find_binary(self):
        """Load binary code from a file"""
        filetypes = [('Binary files', '*.bin'), ('Text files', '*.txt'), ('All files', '*.*')]
        filename = filedialog.askopenfilename(
            title='Open Binary File',
            filetypes=filetypes,
            initialdir=os.getcwd()
        )
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    self.binary_text.delete('1.0', 'end')
                    self.binary_text.insert('1.0', content)
                    self.update_console(f"Loaded binary from: {filename}")
            except Exception as e:
                self.update_console(f"Error loading file: {str(e)}")

    @staticmethod
    def save_binary(self):
        """Save binary code to a file"""
        content = self.binary_text.get('1.0', 'end').strip()
        if not content:
            self.update_console("No binary code to save")
            return
            
        filetypes = [('Binary files', '*.bin'), ('Text files', '*.txt'), ('All files', '*.*')]
        filename = filedialog.asksaveasfilename(
            title='Save Binary File',
            filetypes=filetypes,
            defaultextension=".bin",
            initialdir=os.getcwd()
        )
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(content)
                    self.update_console(f"Saved binary to: {filename}")
            except Exception as e:
                self.update_console(f"Error saving file: {str(e)}")

