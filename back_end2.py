class LC3Simulator:
    def __init__(self):
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.PSR = 0
        self.MSR = 0
        self.memory = {}
        self.PC = 0x3000
        self.flags = {"N": 0, "Z": 1, "P": 0}
        self.instruction_set = {
            "0001": self._execute_add,
            "0101": self._execute_and,
            "1111": self._execute_trap,
            "0000": self._execute_br,
            "0010": self._execute_ld,
            "0110": self._execute_ldr,
            "0011": self._execute_st,
            "0100": self._execute_jsr,
            "1000": self._execute_rti,
            "0111": self._execute_str,
            "1010": self._execute_ldi,
            "1011": self._execute_sti,
            "1100": self._execute_jmp,
            "1110": self._execute_lea,
            "1001": self._execute_not
        }
        self.input_callback = None
        self.output_callback = None
        self.instruction_count = 0

    def reset_registers(self):
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.PSR = 0
        self.MSR = 0
        self.PC = 0x3000
        self.memory = {}
        self.flags = {"N": 0, "Z": 1, "P": 0}
        self.instruction_count = 0
        

    def load_instructions(self, instructions_text):
        self.memory = {}
        self.reset_registers()
        instructions = [line.split("#")[0].strip() for line in instructions_text.split("\n") if line.strip() and not line.startswith("#")]
        
        for i, instruction in enumerate(instructions):
            if instruction.upper().startswith(".ORIG"):
                try:
                    self.PC = int(instruction.split()[1], 16)
                    continue
                except (ValueError, IndexError):
                    print("Invalid .ORIG instruction")
                    return
            
            if len(instruction) == 16 and all(c in '01' for c in instruction):
                self.memory[self.PC + i] = instruction

    def execute_step(self):
        if self.PC not in self.memory:
            print("No hay más instrucciones para ejecutar.")
            return False

        self.current_instruction = self.memory[self.PC]
        opcode = self.current_instruction[:4]

        if opcode in self.instruction_set:
            self.instruction_set[opcode]()
            self.instruction_count += 1
        else:
            print(f"Opcode desconocido: {opcode}")

        self.PC += 1
        return True

    def _update_flags(self, result):
        self.flags = {"N": 0, "Z": 0, "P": 0}
        if result == 0:
            self.flags["Z"] = 1
        elif result > 0:
            self.flags["P"] = 1
        else:
            self.flags["N"] = 1

    def _sign_extend(self, value, bit_count):
        if value & (1 << (bit_count - 1)):
            value -= (1 << bit_count)
        return value

    def _execute_add(self):
        dr = int(self.current_instruction[4:7], 2)
        sr1 = int(self.current_instruction[7:10], 2)
        if self.current_instruction[10] == "0":
            sr2 = int(self.current_instruction[13:], 2)
            result = self.registers[f"R{sr1}"] + self.registers[f"R{sr2}"]
        else:
            imm5 = self._sign_extend(int(self.current_instruction[11:], 2), 5)
            result = self.registers[f"R{sr1}"] + imm5
        self.registers[f"R{dr}"] = result & 0xFFFF
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_and(self):
        dr = int(self.current_instruction[4:7], 2)
        sr1 = int(self.current_instruction[7:10], 2)
        if self.current_instruction[10] == "0":
            sr2 = int(self.current_instruction[13:], 2)
            result = self.registers[f"R{sr1}"] & self.registers[f"R{sr2}"]
        else:
            imm5 = self._sign_extend(int(self.current_instruction[11:], 2), 5)
            result = self.registers[f"R{sr1}"] & imm5
        self.registers[f"R{dr}"] = result & 0xFFFF
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_ld(self):
        dr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        self.registers[f"R{dr}"] = int(self.memory.get(address, "0" * 16), 2)
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_st(self):
        sr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        self.memory[address] = f"{self.registers[f'R{sr}']:016b}"

    def _execute_jsr(self):
        self.registers["R7"] = self.PC + 1
        if self.current_instruction[4] == "1":
            pc_offset = self._sign_extend(int(self.current_instruction[5:], 2), 11)
            self.PC = (self.PC + pc_offset) & 0xFFFF
        else:
            base_r = int(self.current_instruction[7:10], 2)
            self.PC = self.registers[f"R{base_r}"]

    def _execute_ldr(self):
        dr = int(self.current_instruction[4:7], 2)
        base_r = int(self.current_instruction[7:10], 2)
        offset = self._sign_extend(int(self.current_instruction[10:], 2), 6)
        address = (self.registers[f"R{base_r}"] + offset) & 0xFFFF
        self.registers[f"R{dr}"] = int(self.memory.get(address, "0" * 16), 2)
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_str(self):
        sr = int(self.current_instruction[4:7], 2)
        base_r = int(self.current_instruction[7:10], 2)
        offset = self._sign_extend(int(self.current_instruction[10:], 2), 6)
        address = (self.registers[f"R{base_r}"] + offset) & 0xFFFF
        self.memory[address] = f"{self.registers[f'R{sr}']:016b}"

    def _execute_rti(self):
        if self.PSR & 0x8000:  # Check if in supervisor mode
            self.PC = self.registers["R6"]
            self.PSR = self.memory[self.registers["R6"] + 1]
            self.registers["R6"] += 2
        else:
            print("Privilege mode exception: RTI called in user mode")

    def _execute_ldi(self):
        dr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        indirect_address = int(self.memory.get(address, "0" * 16), 2)
        self.registers[f"R{dr}"] = int(self.memory.get(indirect_address, "0" * 16), 2)
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_sti(self):
        sr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        indirect_address = int(self.memory.get(address, "0" * 16), 2)
        self.memory[indirect_address] = f"{self.registers[f'R{sr}']:016b}"

    def _execute_jmp(self):
        base_r = int(self.current_instruction[7:10], 2)
        self.PC = self.registers[f"R{base_r}"]

    def _execute_lea(self):
        dr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        self.registers[f"R{dr}"] = (self.PC + 1 + pc_offset) & 0xFFFF
        self._update_flags(self.registers[f"R{dr}"])

    def set_input_callback(self, callback):
        self.input_callback = callback

    def set_output_callback(self, callback):
        self.output_callback = callback

    def _execute_trap(self):
        trapvect8 = int(self.current_instruction[8:], 2)
        if trapvect8 == 0x20:  # GETC
            if self.input_callback:
                char = self.input_callback("Enter a single character: ")
            else:
                char = input("Enter a single character: ")
            self.registers["R0"] = ord(char[0]) if char else 0
        elif trapvect8 == 0x21:  # OUT
            char = chr(self.registers["R0"] & 0xFF)
            if self.output_callback:
                self.output_callback(char + "\n")
            else:
                print(char, end='\n', flush=True)
        elif trapvect8 == 0x22:  # PUTS
            address = self.registers["R0"]
            string = ""
            while True:
                char_value = self.memory.get(address, 0)
                if char_value == 0:
                    break
                string += chr(char_value & 0xFF)
                address += 1
            print(string, end='', flush=True)
        elif trapvect8 == 0x23:  # IN
            char = input("Enter a single character: ")
            self.registers["R0"] = ord(char[0]) if char else 0
            print(f"Character read: {char[0] if char else ''}")
        elif trapvect8 == 0x24:  # PUTSP
            address = self.registers["R0"]
            string = ""
            while True:
                char_value = self.memory.get(address, 0)
                if char_value == 0:
                    break
                string += chr(char_value & 0xFF)
                char_value >>= 8
                if char_value != 0:
                    string += chr(char_value & 0xFF)
                address += 1
            print(string, end='', flush=True)
        elif trapvect8 == 0x25:  # HALT
            print("HALT instruction encountered. Stopping execution.")
            return False
        else:
            print(f"Unknown TRAP vector: x{trapvect8:02X}")
        
        return True

    def _execute_br(self):
        n = int(self.current_instruction[4], 2)
        z = int(self.current_instruction[5], 2)
        p = int(self.current_instruction[6], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        if (n and self.flags["N"]) or (z and self.flags["Z"]) or (p and self.flags["P"]):
            self.PC = (self.PC + pc_offset) & 0xFFFF

    def _execute_not(self):
        dr = int(self.current_instruction[4:7], 2)
        sr = int(self.current_instruction[7:10], 2)
        self.registers[f"R{dr}"] = (~self.registers[f"R{sr}"]) & 0xFFFF
        self._update_flags(self.registers[f"R{dr}"])

    def show_state(self):
        print(f"PC: {self.PC:04X}")
        print("Registros:")
        for reg, value in self.registers.items():
            print(f"  {reg}: {value:04X}")
        print(f"PSR: {self.PSR:04X}")
        print(f"MSR: {self.MSR:04X}")
        print(f"Flags: N={self.flags['N']} Z={self.flags['Z']} P={self.flags['P']}")
        print("-" * 40)
