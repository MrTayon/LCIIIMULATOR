class Conversor:
    def __init__(self):
        self.keys = {
            "ADD": "0001", "AND": "0101", "BR": "0000", "JMP": "1100",
            "JSR": "0100", "LD": "0010", "LDI": "1010", "LDR": "0110",
            "LEA": "1110", "NOT": "1001", "RET": "1100", "RTI": "1000",
            "ST": "0011", "STI": "1011", "STR": "0111", "TRAP": "1111",
            "MUL": "1101"
        }
        self.registers = {f"R{i}": f"{i:03b}" for i in range(8)}
        self.reverse_registers = {v: k for k, v in self.registers.items()}
        self.condition_bits = {
            "": "000", "n": "100", "z": "010", "p": "001",
            "nz": "110", "np": "101", "zp": "011", "nzp": "111"
        }
        self.pseudo_ops = [".ORIG", ".END", ".FILL", ".BLKW", ".HALT", "HALT"]
        self.trap_vectors = {
            0x20: ".GETC", 0x21: ".OUT", 0x22: ".PUTS",
            0x23: ".IN", 0x24: ".PUTSP", 0x25: ".HALT"
        }
        self.reverse_trap_vectors = {v: k for k, v in self.trap_vectors.items()}
        self.orig_labels = {}
        self.orig_instructions = []

    def assembly_to_binary(self, assembly_code):
        self.orig_labels.clear()
        self.orig_instructions.clear()
        lines = assembly_code.strip().split('\n')
        result = []
        label_addresses = {}
        current_address = 0

        # First pass: collect label addresses
        for line in lines:
            line = line.strip()
            if ';' in line:
                line = line.split(';')[0]
            if not line or line.startswith(';') or line.upper().startswith('.ORIG') or line.upper().startswith('.END'):
                continue
            if ':' in line:
                label, instruction = line.split(':', 1)
                label_addresses[label.strip()] = current_address
                line = instruction.strip()
            if line:
                if '.FILL' in line:
                    parts = line.split()
                    value_str = parts[-1]
                    if value_str.startswith('#'):
                        value = int(value_str[1:])
                    elif value_str.startswith('x'):
                        value = int(value_str[1:], 16)
                    else:
                        value = int(value_str)
                    if value < 0:
                        value = (1 << 16) + value  # Convert to two's complement
                    self.orig_instructions.append((current_address, f"{value:016b}"))
                elif '.BLKW' in line:
                    self.orig_instructions.append((current_address, '0'*16))
                else:
                    self.orig_instructions.append((current_address, line))
                current_address += 1

        # Second pass: convert to binary
        for address, line in self.orig_instructions:
            parts = line.replace(',', '').split()
            opcode = parts[0].upper()

            if opcode in ["ADD", "AND"]:
                DR, SR1 = self.registers[parts[1]], self.registers[parts[2]]
                if parts[3].startswith("#"):
                    imm5 = int(parts[3][1:])
                    result.append(f"{self.keys[opcode]}{DR}{SR1}1{imm5 & 0x1F:05b}")
                else:
                    SR2 = self.registers[parts[3]]
                    result.append(f"{self.keys[opcode]}{DR}{SR1}000{SR2}")
            elif opcode == "MUL":
                DR, SR1 = self.registers[parts[1]], self.registers[parts[2]]
                if parts[3].startswith("#"):
                    imm5 = int(parts[3][1:])
                    result.append(f"1101{DR}{SR1}1{imm5 & 0x1F:05b}")
                else:
                    SR2 = self.registers[parts[3]]
                    result.append(f"1101{DR}{SR1}000{SR2}")
            elif opcode.startswith("BR"):
                conditions = opcode[2:].lower()
                cond_bits = self.condition_bits.get(conditions, "000")
                offset = self.calculate_offset(parts[1], label_addresses, address, 9)
                result.append(f"{self.keys['BR']}{cond_bits}{offset:09b}")
            elif opcode in ["LD", "ST", "LEA", "LDI", "STI"]:
                DR = self.registers[parts[1]]
                offset = self.calculate_offset(parts[2], label_addresses, address, 9)
                result.append(f"{self.keys[opcode]}{DR}{offset:09b}")
            elif opcode in ["LDR", "STR"]:
                DR = self.registers[parts[1]]
                BaseR = self.registers[parts[2]]
                offset6 = int(parts[3][1:])
                result.append(f"{self.keys[opcode]}{DR}{BaseR}{offset6 & 0x3F:06b}")
            elif opcode in ["JMP", "RET"]:
                if opcode == "RET":
                    BaseR = "111"  # R7 for RET
                else:
                    BaseR = self.registers[parts[1]]
                result.append(f"{self.keys['JMP']}000{BaseR}000000")
            elif opcode == "JSR":
                if len(parts) > 1 and parts[1] in self.registers:  # JSRR
                    BaseR = self.registers[parts[1]]
                    result.append(f"{self.keys['JSR']}000{BaseR}000000")
                else:  # JSR
                    offset = self.calculate_offset(parts[1], label_addresses, address, 11)
                    result.append(f"{self.keys['JSR']}1{offset:011b}")
            elif opcode == "TRAP" or opcode in self.reverse_trap_vectors:
                if opcode == "TRAP":
                    trapvect8 = int(parts[1].replace('x', '0x'), 16)
                else:
                    trapvect8 = self.reverse_trap_vectors[opcode]
                result.append(f"{self.keys['TRAP']}0000{trapvect8:08b}")
            elif opcode == "NOT":
                DR, SR = self.registers[parts[1]], self.registers[parts[2]]
                result.append(f"{self.keys[opcode]}{DR}{SR}111111")
            elif opcode == "RTI":
                result.append(f"{self.keys[opcode]}000000000000")
            else:
                result.append(line)

        return "\n".join(result)

    def binary_to_assembly(self, binary_code):
        lines = binary_code.strip().split('\n')
        result = []
        label_addresses = {}
        fill_addresses = set()
        blkw_addresses = set()
        current_address = 0x3000  # Inicializamos con la dirección por defecto

        # First pass: collect label addresses and identify .BLKW
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            
            instruction = int(line, 2)
            opcode = (instruction >> 12) & 0xF
            
            if opcode in [2, 3, 6, 7, 10, 11, 14]:  # LD, ST, LDR, STR, LDI, STI, LEA
                offset = self.sign_extend(instruction & 0x1FF, 9)
                target = current_address + 1 + offset
                if target not in label_addresses:
                    label_addresses[target] = f"LABEL_{len(label_addresses)}"
                    if opcode in [2, 6, 10, 14]:
                        fill_addresses.add(target)
                    elif opcode in [3, 7, 11]:
                        blkw_addresses.add(target)
            elif opcode == 0 and current_address not in fill_addresses and current_address not in blkw_addresses:  # BR
                offset = self.sign_extend(instruction & 0x1FF, 9)
                target = current_address + 1 + offset
                if target not in label_addresses:
                    label_addresses[target] = f"LABEL_{len(label_addresses)}"
            elif opcode == 4 and instruction & 0x800:  # JSR
                offset = self.sign_extend(instruction & 0x7FF, 11)
                target = current_address + 1 + offset
                if target not in label_addresses:
                    label_addresses[target] = f"LABEL_{len(label_addresses)}"
            elif instruction == 0:  # Potential .BLKW
                blkw_addresses.add(current_address)
            
            current_address += 1

        # Second pass: convert to assembly
        current_address = 0x3000  # Reiniciamos la dirección
        result.append(f".ORIG x{current_address:04X}")

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            instruction = int(line, 2)
            opcode = (instruction >> 12) & 0xF

            if current_address in label_addresses:
                label = f"{label_addresses[current_address]}:"
                if current_address in fill_addresses:
                    num = instruction & 0xFFFF
                    if num > 0x7FFF:
                        num -= 0x10000
                    label += f" .FILL #{num}"
                elif current_address in blkw_addresses:
                    label += f" .BLKW 1"
                result.append(label)

            if current_address not in fill_addresses and current_address not in blkw_addresses:
                if opcode == 1:  # ADD
                    dr = (instruction >> 9) & 0x7
                    sr1 = (instruction >> 6) & 0x7
                    if instruction & 0x20:
                        imm5 = self.sign_extend(instruction & 0x1F, 5)
                        result.append(f"\tADD R{dr}, R{sr1}, #{imm5}")
                    else:
                        sr2 = instruction & 0x7
                        result.append(f"\tADD R{dr}, R{sr1}, R{sr2}")
                elif opcode == 5:  # AND
                    dr = (instruction >> 9) & 0x7
                    sr1 = (instruction >> 6) & 0x7
                    if instruction & 0x20:
                        imm5 = self.sign_extend(instruction & 0x1F, 5)
                        result.append(f"\tAND R{dr}, R{sr1}, #{imm5}")
                    else:
                        sr2 = instruction & 0x7
                        result.append(f"\tAND R{dr}, R{sr1}, R{sr2}")
                elif opcode == 13:
                    dr = (instruction >> 9) & 0x7
                    sr1 = (instruction >> 6) & 0x7
                    if instruction & 0x20:
                        imm5 = self.sign_extend(instruction & 0x1F, 5)
                        result.append(f"\tMUL R{dr}, R{sr1}, #{imm5}")
                    else:
                        sr2 = instruction & 0x7
                        result.append(f"\tMUL R{dr}, R{sr1}, R{sr2}")
                elif opcode == 0:  # BR
                    n = (instruction >> 11) & 1
                    z = (instruction >> 10) & 1
                    p = (instruction >> 9) & 1
                    offset = self.sign_extend(instruction & 0x1FF, 9)
                    target = current_address + 1 + offset
                    cond = "".join(['n' if n else '', 'z' if z else '', 'p' if p else ''])
                    label = label_addresses.get(target, f"x{target:04X}")
                    result.append(f"\tBR{cond.upper()} {label}")
                elif opcode in [2, 3, 10, 11, 14]:  # LD, ST, LDI, STI, LEA
                    dr = (instruction >> 9) & 0x7
                    offset = self.sign_extend(instruction & 0x1FF, 9)
                    target = current_address + 1 + offset
                    op_name = {2: "LD", 3: "ST", 10: "LDI", 11: "STI", 14: "LEA"}[opcode]
                    label = label_addresses.get(target, f"x{target:04X}")
                    result.append(f"\t{op_name} R{dr}, {label}")
                elif opcode in [6, 7]:  # LDR, STR
                    dr = (instruction >> 9) & 0x7
                    base_r = (instruction >> 6) & 0x7
                    offset6 = self.sign_extend(instruction & 0x3F, 6)
                    op_name = "LDR" if opcode == 6 else "STR"
                    result.append(f"\t{op_name} R{dr}, R{base_r}, #{offset6}")
                elif opcode == 12:  # JMP or RET
                    base_r = (instruction >> 6) & 0x7
                    if base_r == 7:
                        result.append("\tRET")
                    else:
                        result.append(f"\tJMP R{base_r}")
                elif opcode == 4:  # JSR or JSRR
                    if instruction & 0x800:
                        offset = self.sign_extend(instruction & 0x7FF, 11)
                        target = current_address + 1 + offset
                        label = label_addresses.get(target, f"x{target:04X}")
                        result.append(f"\tJSR {label}")
                    else:
                        base_r = (instruction >> 6) & 0x7
                        result.append(f"\tJSRR R{base_r}")
                elif opcode == 15:  # TRAP
                    trapvect8 = instruction & 0xFF
                    if trapvect8 == 0x25:
                        result.append("\tTRAP x25")
                    else:
                        result.append(f"\tTRAP x{trapvect8:02X}")
                elif opcode == 9:  # NOT
                    dr = (instruction >> 9) & 0x7
                    sr = (instruction >> 6) & 0x7
                    result.append(f"\tNOT R{dr}, R{sr}")
                elif opcode == 8:  # RTI
                    result.append("\tRTI")

            current_address += 1

        result.append(".END")
        return "\n".join(result)
    
    def calculate_offset(self, label_or_value, label_addresses, current_address, bits):
        if label_or_value.startswith("#"):
            return int(label_or_value[1:]) & ((1 << bits) - 1)
        if label_or_value.startswith("x"):
            return int(label_or_value.replace('x', '0x'), 16) & ((1 << bits) - 1)
        if label_or_value not in label_addresses:
            raise ValueError(f"Label no encontrada: {label_or_value}")
        offset = label_addresses[label_or_value] - (current_address + 1)
        if offset < -(1 << (bits - 1)) or offset >= (1 << (bits - 1)):
            raise ValueError(f"Offset fuera de rango: {offset}")
        return offset & ((1 << bits) - 1)

    def sign_extend(self, value, bits):
        if value & (1 << (bits - 1)):
            return value - (1 << bits)
        return value
