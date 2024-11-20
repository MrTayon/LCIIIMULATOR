class LC3Simulator:
    def __init__(self):
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.PSR = 32768  # Initialize in supervisor mode (decimal equivalent of 0x8000)
        self.MSR = 0
        self.memory = {}
        self.PC = 0  # Initialize PC to 0
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
        self.halted = False
        self.console_buffer = []
        self.input_buffer = []

    def load_instructions(self, binary_instructions):
        self.memory = {}
        instructions = [line.strip() for line in binary_instructions.split('\n') if line.strip()]
        if instructions:
            first_instruction = int(instructions[0], 2)
            if first_instruction == 0x3000:  # Check if the first instruction specifies starting at 0x3000
                self.PC = 0x3000
                instructions = instructions[1:]  # Remove the first instruction
            else:
                self.PC = 0  # Start at 0 if not specified
        for i, instruction in enumerate(instructions):
            if len(instruction) == 16:
                self.memory[self.PC + i] = int(instruction, 2)  # Store as integer

    def step(self):
        if self.halted or self.PC not in self.memory:
            return False

        self.current_instruction = f"{self.memory[self.PC]:016b}"
        opcode = self.current_instruction[:4]

        if self.current_instruction == "0000000000000000":
            self.console_write("NOP instruction encountered.")
            self.PC = (self.PC + 1) & 0xFFFF
            return True

        if opcode in self.instruction_set:
            result = self.instruction_set[opcode]()
            if result is False:  # For TRAP instructions that need input
                return None
            if result is not True:  # If the instruction didn't handle PC update
                self.PC = (self.PC + 1) & 0xFFFF
        else:
            self.console_write(f"Opcode desconocido: {opcode}")
            self.PC = (self.PC + 1) & 0xFFFF

        return True

    def _update_flags(self, result):
        result = result & 0xFFFF  # Ensure 16-bit value
        self.flags = {"N": 0, "Z": 0, "P": 0}
        if result == 0:
            self.flags["Z"] = 1
        elif result & 0x8000:  # Check if negative (bit 15 is set)
            self.flags["N"] = 1
        else:
            self.flags["P"] = 1
        self.PSR = (self.PSR & 0xFFF8) | (self.flags["N"] << 2 | self.flags["Z"] << 1 | self.flags["P"])

    def _sign_extend(self, value, bit_count):
        if value & (1 << (bit_count - 1)):
            value |= (0xFFFF << bit_count)
        return value & 0xFFFF

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
        self.registers[f"R{dr}"] = int(self.memory.get(address, 0))
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_ldr(self):
        dr = int(self.current_instruction[4:7], 2)
        base_r = int(self.current_instruction[7:10], 2)
        offset = self._sign_extend(int(self.current_instruction[10:], 2), 6)
        address = (self.registers[f"R{base_r}"] + offset) & 0xFFFF
        self.registers[f"R{dr}"] = int(self.memory.get(address, 0))
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_lea(self):
        dr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        self.registers[f"R{dr}"] = (self.PC + 1 + pc_offset) & 0xFFFF
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_not(self):
        dr = int(self.current_instruction[4:7], 2)
        sr = int(self.current_instruction[7:10], 2)
        self.registers[f"R{dr}"] = (~self.registers[f"R{sr}"]) & 0xFFFF
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_st(self):
        sr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        self.memory[address] = self.registers[f"R{sr}"]

    def _execute_jsr(self):
        self.registers["R7"] = self.PC + 1
        if self.current_instruction[4] == "1":
            pc_offset = self._sign_extend(int(self.current_instruction[5:], 2), 11)
            self.PC = (self.PC + pc_offset) & 0xFFFF
        else:
            base_r = int(self.current_instruction[7:10], 2)
            self.PC = self.registers[f"R{base_r}"]
        return True

    def _execute_rti(self):
        if self.PSR & 0x8000:  # Check if in supervisor mode
            self.PC = self.registers["R6"]
            self.PSR = self.memory.get(self.registers["R6"] + 1, 0)
            self.registers["R6"] += 2
        else:
            self.console_write("Privilege mode exception: RTI called in user mode")
        return True

    def _execute_str(self):
        sr = int(self.current_instruction[4:7], 2)
        base_r = int(self.current_instruction[7:10], 2)
        offset = self._sign_extend(int(self.current_instruction[10:], 2), 6)
        address = (self.registers[f"R{base_r}"] + offset) & 0xFFFF
        self.memory[address] = self.registers[f"R{sr}"]

    def _execute_ldi(self):
        dr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        indirect_address = self.memory.get(address, 0)
        self.registers[f"R{dr}"] = self.memory.get(indirect_address, 0)
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_sti(self):
        sr = int(self.current_instruction[4:7], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        address = (self.PC + 1 + pc_offset) & 0xFFFF
        indirect_address = self.memory.get(address, 0)
        self.memory[indirect_address] = self.registers[f"R{sr}"]

    def _execute_jmp(self):
        base_r = int(self.current_instruction[7:10], 2)
        self.PC = self.registers[f"R{base_r}"]
        return True

    def _execute_trap(self):
        trapvect8 = int(self.current_instruction[8:], 2)
        if trapvect8 == 0x20:  # GETC
            if not self.input_buffer:
                self.console_write("Input required: ")
                return False
            self.registers["R0"] = ord(self.input_buffer.pop(0))
        elif trapvect8 == 0x21:  # OUT
            self.console_write(chr(self.registers["R0"]))
        elif trapvect8 == 0x22:  # PUTS
            address = self.registers["R0"]
            string = ""
            while True:
                char = chr(self.memory.get(address, 0))
                if char == "\0":
                    break
                string += char
                address += 1
            self.console_write(string)
        elif trapvect8 == 0x23:  # IN
            self.console_write("Input a character: ")
            if not self.input_buffer:
                return False
            char = self.input_buffer.pop(0)
            self.registers["R0"] = ord(char)
            self.console_write(char)
        elif trapvect8 == 0x25:  # HALT
            self.console_write("HALT instruction encountered. Stopping execution.")
            self.halted = True
            return False
        else:
            self.console_write(f"Unimplemented TRAP: x{trapvect8:02X}")
        return True

    def _execute_br(self):
        n = int(self.current_instruction[4], 2)
        z = int(self.current_instruction[5], 2)
        p = int(self.current_instruction[6], 2)
        pc_offset = self._sign_extend(int(self.current_instruction[7:], 2), 9)
        if (n and self.flags["N"]) or (z and self.flags["Z"]) or (p and self.flags["P"]):
            self.PC = (self.PC + pc_offset) & 0xFFFF
            return True
        return False

    def get_state(self):
        return {
            "PC": self.PC,
            "registers": {reg: value & 0xFFFF for reg, value in self.registers.items()},
            "PSR": self.PSR,
            "MSR": self.MSR,
            "flags": self.flags.copy(),
            "halted": self.halted,
            "console_output": self.get_console_output(),
            "current_instruction": f"{self.memory.get(self.PC, 0):016b}"
        }

    def get_console_output(self):
        output = "".join(self.console_buffer)
        self.console_buffer = []
        return output

    def console_write(self, text):
        self.console_buffer.append(text)

    def console_input(self, text):
        self.input_buffer.extend(list(text))

# test
def run_simulator(binary_instructions):
    simulator = LC3Simulator()
    simulator.load_instructions(binary_instructions)

    print("=== Ejecución Paso a Paso ===")
    step_count = 0
    while True:
        state = simulator.get_state()
        print(f"Paso {step_count}:")
        print(f"PC: 0x{state['PC']:04X}")
        print(f"Instrucción actual: {state['current_instruction']}")
        print("Registros:", " ".join(f"{reg}:{value}" for reg, value in state['registers'].items()))
        print(f"PSR: {state['PSR']}")
        print(f"MSR: {state['MSR']}")
        print(f"Flags: N={state['flags']['N']} Z={state['flags']['Z']} P={state['flags']['P']}")
        
        result = simulator.step()
        
        if result is None:
            user_input = input("Entrada requerida: ")
            simulator.console_input(user_input)
        elif not result:
            break
        
        console_output = simulator.get_console_output()
        if console_output:
            print("Salida de consola:", console_output)
        
        print("-" * 40)
        step_count += 1

    print("=== Ejecución Completa ===")
    final_state = simulator.get_state()
    print(f"PC final: 0x{final_state['PC']:04X}")
    print("Registros finales:", " ".join(f"{reg}:{value}" for reg, value in final_state['registers'].items()))
    print(f"PSR final: {final_state['PSR']}")
    print(f"MSR final: {final_state['MSR']}")
    print(f"Flags finales: N={final_state['flags']['N']} Z={final_state['flags']['Z']} P={final_state['flags']['P']}")
    print("Salida final de consola:", final_state['console_output'])

# Instrucciones de ejemplo
binary_instructions = """
0011000000000000
0001001001100011
0101011011100111
0010101000000101
1110110000000011
0110000110111111
0111001110000010
0000001000000011
0000100000000100
0000010000000101
0000111000000110
0001010010100001
0000000111110100
0001010010111111
0000000111110010
0101010010100000
0000000111110000
0100100000000001
1100000111000000
1011111000000010
1000000000000000
0011000000000000
0000000000000000
1111000000100101
"""

run_simulator(binary_instructions)
