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

    def load_instructions(self, instructions_text):
        self.memory = {}
        instructions = [line.split("#")[0].strip() for line in instructions_text.split("\n") if line.strip() and not line.startswith("#")]
        for i, instruction in enumerate(instructions):
            if len(instruction) == 16:
                self.memory[self.PC + i] = instruction

    def execute_step(self):
        if self.PC not in self.memory:
            print("No hay más instrucciones para ejecutar.")
            return False

        self.current_instruction = self.memory[self.PC]
        opcode = self.current_instruction[:4]

        if opcode in self.instruction_set:
            self.instruction_set[opcode]()
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

    def _execute_trap(self):
        trapvect8 = int(self.current_instruction[8:], 2)
        if trapvect8 == 0x25:  # HALT
            print("HALT instruction encountered. Stopping execution.")
            return False
        print(f"TRAP executed: x{trapvect8:02X}")
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

def run_simulator(instructions):
    simulator = LC3Simulator()
    simulator.load_instructions(instructions)

    print("=== Ejecución Paso a Paso ===")
    while simulator.PC in simulator.memory:
        simulator.show_state()
        if not simulator.execute_step():
            break
    print("=== Ejecución Completa ===")
    simulator.show_state()

# Ejemplo de uso
instructions = """
0001001001100011 # ADD R1, R1, #3
0101011011100111 # AND R3, R3, #7
0010101000000101 # LD R5, #5
1110110000000011 # LEA R6, #3
0110000110111111 # LDR R0, R6, #-1
0111001110000010 # STR R1, R6, #2
0000001000000011 # BRp #3
0000100000000100 # BRz #4
0000010000000101 # BRn #5
0000111000000110 # BRnzp #6
0001010010100001 # ADD R2, R2, #1
0000000111110100 # BR #-12
0001010010111111 # ADD R2, R2, #-1
0000000111110010 # BR #-14
0101010010100000 # AND R2, R2, #0
0000000111110000 # BR #-16
0100100000000001 # JSR #1
1100000111000000 # RET
1011111000000010 # STI R7, #2
1000000000000000 # RTI
0011000000000000 # ST R0, #0
0000000000000000 # BR #0
1111000000100101 # TRAP x25
"""

run_simulator(instructions)
