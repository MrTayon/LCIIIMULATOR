class Conversor:
    def __init__(self):
        self.keys = {
            "ADD": "0001", "AND": "0101", "BR": "0000", "JMP": "1100",
            "JSR": "0100", "LD": "0010", "LDI": "1010", "LDR": "0110",
            "LEA": "1110", "NOT": "1001", "RET": "1100", "RTI": "1000",
            "ST": "0011", "STI": "1011", "STR": "0111", "TRAP": "1111"
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

    def assembly_to_binary(self, assembly_code):
        lines = assembly_code.strip().split('\n')
        result = []
        label_addresses = {}
        current_address = 0
        orig_address = None

        # First pass: collect label addresses
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if ':' in line:
                label, instruction = line.split(':', 1)
                self.orig_labels[current_address] = label.strip()
                label_addresses[label.strip()] = current_address
                line = instruction.strip()
            parts = line.replace(',', '').split()
            opcode = parts[0].upper()

            if opcode == '.ORIG':
                orig_address = int(parts[1][1:], 16)
                current_address = orig_address
            elif opcode == '.END':
                break
            elif opcode == '.FILL':
                current_address += 1
            elif opcode == '.BLKW':
                current_address += int(parts[1])
            elif opcode not in self.pseudo_ops:
                current_address += 1

        # Second pass: convert to binary
        current_address = orig_address if orig_address is not None else 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if ':' in line:
                _, instruction = line.split(':', 1)
                line = instruction.strip()
            if not line:
                continue

            parts = line.replace(',', '').split()
            opcode = parts[0].upper()

            if opcode == '.ORIG':
                result.append(f"{int(parts[1][1:], 16):016b}")
            elif opcode == '.END':
                break
            elif opcode == '.FILL':
                value = int(parts[1][1:], 16) if parts[1].startswith('x') else int(parts[1])
                result.append(f"{value & 0xFFFF:016b}")
            elif opcode == '.BLKW':
                count = int(parts[1])
                result.extend(["0" * 16] * count)
            elif opcode in ['.HALT', 'HALT']:
                result.append(f"{self.keys['TRAP']}0000{0x25:08b}")
            elif opcode.startswith("BR"):
                conditions = opcode[2:].lower()
                cond_bits = self.condition_bits.get(conditions, "000")
                offset = self.calculate_offset(parts[1], label_addresses, current_address, 9)
                result.append(f"{self.keys['BR']}{cond_bits}{offset:09b}")
            elif opcode in ["ADD", "AND"]:
                DR, SR1 = self.registers[parts[1]], self.registers[parts[2]]
                if parts[3].startswith("#"):
                    imm5 = int(parts[3][1:])
                    result.append(f"{self.keys[opcode]}{DR}{SR1}1{imm5 & 0x1F:05b}")
                else:
                    SR2 = self.registers[parts[3]]
                    result.append(f"{self.keys[opcode]}{DR}{SR1}000{SR2}")
            elif opcode in ["LD", "ST", "LEA", "LDI", "STI"]:
                DR = self.registers[parts[1]]
                offset = self.calculate_offset(parts[2], label_addresses, current_address, 9)
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
                    offset = self.calculate_offset(parts[1], label_addresses, current_address, 11)
                    result.append(f"{self.keys['JSR']}1{offset:011b}")
            elif opcode == "TRAP" or opcode in self.reverse_trap_vectors:
                if opcode == "TRAP":
                    trapvect8 = int(parts[1][1:], 16)
                else:
                    trapvect8 = self.reverse_trap_vectors[opcode]
                result.append(f"{self.keys['TRAP']}0000{trapvect8:08b}")
            elif opcode == "NOT":
                DR, SR = self.registers[parts[1]], self.registers[parts[2]]
                result.append(f"{self.keys[opcode]}{DR}{SR}111111")
            elif opcode == "RTI":
                result.append(f"{self.keys[opcode]}000000000000")
            else:
                raise ValueError(f"Opcode no soportado: {opcode}")

            if opcode not in self.pseudo_ops or opcode in ['.HALT', 'HALT']:
                current_address += 1

        return "\n".join(result)

    def binary_to_assembly(self, binary_code):
        lines = binary_code.strip().split('\n')
        result = []
        address_to_label = {}
        current_address = None

        # First pass: identify potential labels
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            if current_address is None:
                current_address = int(line, 2)
                continue
            
            if current_address in self.orig_labels:
                address_to_label[current_address] = self.orig_labels[current_address]
            
            opcode_bin = line[:4]
            if opcode_bin == self.keys['BR']:
                offset = self.sign_extend(int(line[7:], 2), 9)
                target_address = current_address + 1 + offset
                if target_address not in address_to_label:
                    address_to_label[target_address] = f"LABEL_{target_address:X}"
            elif opcode_bin == self.keys['JSR'] and line[4] == '1':
                offset = self.sign_extend(int(line[5:], 2), 11)
                target_address = current_address + 1 + offset
                if target_address not in address_to_label:
                    address_to_label[target_address] = f"LABEL_{target_address:X}"
            current_address += 1

        # Second pass: convert to assembly
        current_address = None
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            
            line = line.ljust(16, '0')
            if current_address is None:
                current_address = int(line, 2)
                result.append(f".ORIG x{current_address:04X}")
                continue

            if current_address in address_to_label:
                result.append(f"{address_to_label[current_address]}:")

            opcode_bin = line[:4]
            opcode = next((key for key, value in self.keys.items() if value == opcode_bin), None)

            instruction = ""
            if not opcode:
                value = int(line, 2)
                instruction = f".FILL x{value:04X}"
            elif opcode == "BR":
                condition_bits = line[4:7]
                condition = next((key for key, value in self.condition_bits.items() if value == condition_bits), "")
                offset = self.sign_extend(int(line[7:], 2), 9)
                target_address = current_address + 1 + offset
                instruction = f"BR{condition.upper()} {address_to_label.get(target_address, f'x{target_address:04X}')}"
            elif opcode in ["ADD", "AND"]:
                DR = self.reverse_registers[line[4:7]]
                SR1 = self.reverse_registers[line[7:10]]
                if line[10] == "1":
                    imm5 = self.sign_extend(int(line[11:], 2), 5)
                    instruction = f"{opcode} {DR}, {SR1}, #{imm5}"
                else:
                    SR2 = self.reverse_registers[line[13:]]
                    instruction = f"{opcode} {DR}, {SR1}, {SR2}"
            elif opcode in ["LD", "ST", "LEA", "LDI", "STI"]:
                DR = self.reverse_registers[line[4:7]]
                offset = self.sign_extend(int(line[7:], 2), 9)
                target_address = current_address + 1 + offset
                if target_address in address_to_label:
                    instruction = f"{opcode} {DR}, {address_to_label[target_address]}"
                else:
                    instruction = f"{opcode} {DR}, x{target_address:04X}"
            elif opcode in ["LDR", "STR"]:
                DR = self.reverse_registers[line[4:7]]
                BaseR = self.reverse_registers[line[7:10]]
                offset6 = self.sign_extend(int(line[10:], 2), 6)
                instruction = f"{opcode} {DR}, {BaseR}, #{offset6}"
            elif opcode == "JMP":
                if line[7:10] == "111":
                    instruction = "RET"
                else:
                    BaseR = self.reverse_registers[line[7:10]]
                    instruction = f"JMP {BaseR}"
            elif opcode == "JSR":
                if line[4] == "0":  # JSRR
                    BaseR = self.reverse_registers[line[7:10]]
                    instruction = f"JSRR {BaseR}"
                else:  # JSR
                    offset = self.sign_extend(int(line[5:], 2), 11)
                    target_address = current_address + 1 + offset
                    if target_address in address_to_label:
                        instruction = f"JSR {address_to_label[target_address]}"
                    else:
                        instruction = f"JSR x{target_address:04X}"
            elif opcode == "TRAP":
                trapvect8 = int(line[8:], 2)
                if trapvect8 in self.trap_vectors:
                    instruction = f"{self.trap_vectors[trapvect8]}"
                else:
                    instruction = f"TRAP x{trapvect8:02X}"
            elif opcode == "NOT":
                DR = self.reverse_registers[line[4:7]]
                SR = self.reverse_registers[line[7:10]]
                instruction = f"NOT {DR}, {SR}"
            elif opcode == "RTI":
                instruction = "RTI"
            else:
                raise ValueError(f"Opcode no implementado: {opcode}")

            if instruction:
                result.append(f"\t{instruction}")

            current_address += 1

        return "\n".join(result)

    def calculate_offset(self, label_or_value, label_addresses, current_address, bits):
        if label_or_value.startswith("#"):
            return int(label_or_value[1:]) & ((1 << bits) - 1)
        if label_or_value.startswith("x"):
            return int(label_or_value[1:], 16) - (current_address + 1) & ((1 << bits) - 1)
        if label_or_value not in label_addresses:
            return 0
        offset = label_addresses[label_or_value] - current_address - 1
        if offset < -(1 << (bits - 1)) or offset >= (1 << (bits - 1)):
            raise ValueError(f"Offset fuera de rango: {offset}")
        return offset & ((1 << bits) - 1)

    def sign_extend(self, value, bits):
        if value & (1 << (bits - 1)):
            return value - (1 << bits)
        return value

# Ejemplo de uso
conv = Conversor()

assembly_code = """
.ORIG x3000
STARTS: ADD R1, R2, #3
       AND R3, R4, #7
       LD R5, DATA
       LEA R6, END
       LDR R0, R6, #-1
       STR R1, R6, #2
       BRp POSITIVE
       BRn NEGATIVE
       BRz ZERO
       BRnzp DONE
POSITIVE: ADD R2, R2, #1
          BR STARTS
NEGATIVE: ADD R2, R2, #-1
          BR STARTS
ZERO:    AND R2, R2, #0
         BR STARTS
DONE:   JSR SUBRUTINA
        RET
SUBRUTINA: STI R7, SAVE_R7
           RTI
DATA:  .FILL x3000
SAVE_R7: .BLKW 1
.HALT
"""

binary_code = conv.assembly_to_binary(assembly_code)
print("Ensamblador a Binario:\n", binary_code)

binary_input = binary_code.strip()
assembly_output = conv.binary_to_assembly(binary_input)
print("\nBinario a Ensamblador:\n", assembly_output)
