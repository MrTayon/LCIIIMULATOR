class Conversor:
    def __init__(self):
        self.keys = {
            "ADD": "0001", "AND": "0101", "BR": "0000", "JMP": "1100",
            "JSR": "0100", "LD": "0010", "LDI": "1010", "LDR": "0110",
            "LEA": "1110", "NOT": "1001", "RET": "1100", "RTI": "1000",
            "ST": "0011", "STI": "1011", "STR": "0111", "TRAP": "1111",
            "reserved": "1101"
        }
        self.registers = {f"R{i}": f"{i:03b}" for i in range(8)}  # R0-R7 en binario
        self.reverse_registers = {f"{i:03b}": f"R{i}" for i in range(8)}  # Binario a R0-R7
        self.condition_bits = {
            "": "000", "n": "100", "z": "010", "p": "001",
            "nz": "110", "np": "101", "zp": "011", "nzp": "111"
        }

    def parse_labels(self, assembly_code):
        lines = assembly_code.strip().split('\n')
        label_addresses = {}
        instruction_index = 0

        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if ":" in line:
                label, instruction = line.split(":", 1)
                label_addresses[label.strip()] = instruction_index
                if instruction.strip():
                    instruction_index += 1
            else:
                instruction_index += 1

        return label_addresses

    def assembly_to_binary(self, assembly_code):
        label_addresses = self.parse_labels(assembly_code)
        lines = assembly_code.strip().split('\n')
        result = []

        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith(';') or ":" in line:
                continue

            parts = line.replace(',', '').split()
            opcode = parts[0]
            bin_instr = ""

            if opcode.startswith("BR"):
                conditions = opcode[2:].lower()
                if conditions not in self.condition_bits:
                    raise ValueError(f"Condiciones no soportadas en BR: {conditions}")
                cond_bits = self.condition_bits[conditions]

                label = parts[1]
                if label not in label_addresses:
                    raise ValueError(f"Etiqueta no encontrada: {label}")
                offset = label_addresses[label] - len(result) - 1
                if offset < -256 or offset > 255:
                    raise ValueError(f"Offset fuera de rango para BR: {offset}")
                if offset < 0:
                    offset = (1 << 9) + offset
                offset = f"{offset:09b}"
                bin_instr = f"{self.keys['BR']}{cond_bits}{offset}"

            elif opcode in ["ADD", "AND"]:
                DR = self.registers[parts[1]]
                SR1 = self.registers[parts[2]]
                if "#" in parts[3]:
                    imm5 = int(parts[3][1:])
                    if imm5 < 0:
                        imm5 = (1 << 5) + imm5
                    imm5 = f"{imm5:05b}"
                    bin_instr = f"{self.keys[opcode]}{DR}{SR1}1{imm5}"
                else:
                    SR2 = self.registers[parts[3]]
                    bin_instr = f"{self.keys[opcode]}{DR}{SR1}000{SR2}"

            elif opcode in ["LD", "ST", "LEA", "LDI", "STI"]:
                DR = self.registers[parts[1]]
                label = parts[2]
                if label not in label_addresses:
                    raise ValueError(f"Etiqueta no encontrada: {label}")
                offset = label_addresses[label] - len(result) - 1
                if offset < -256 or offset > 255:
                    raise ValueError(f"Offset fuera de rango para {opcode}: {offset}")
                if offset < 0:
                    offset = (1 << 9) + offset
                offset = f"{offset:09b}"
                bin_instr = f"{self.keys[opcode]}{DR}{offset}"

            elif opcode in ["LDR", "STR"]:
                DR = self.registers[parts[1]]
                BaseR = self.registers[parts[2]]
                offset = int(parts[3][1:]) if parts[3].startswith('#') else int(parts[3])
                if offset < -32 or offset > 31:
                    raise ValueError(f"Offset fuera de rango para {opcode}: {offset}")
                if offset < 0:
                    offset = (1 << 6) + offset
                offset = f"{offset:06b}"
                bin_instr = f"{self.keys[opcode]}{DR}{BaseR}{offset}"

            elif opcode == "JMP":
                baseR = self.registers[parts[1]]
                bin_instr = f"{self.keys[opcode]}000{baseR}000000"

            elif opcode == "JSR":
                if parts[1] in self.registers:  # JSRR
                    baseR = self.registers[parts[1]]
                    bin_instr = f"{self.keys[opcode]}000{baseR}000000"
                else:  # JSR
                    label = parts[1]
                    if label not in label_addresses:
                        raise ValueError(f"Etiqueta no encontrada: {label}")
                    offset = label_addresses[label] - len(result) - 1
                    if offset < -1024 or offset > 1023:
                        raise ValueError(f"Offset fuera de rango para JSR: {offset}")
                    if offset < 0:
                        offset = (1 << 11) + offset
                    offset = f"{offset:011b}"
                    bin_instr = f"{self.keys[opcode]}1{offset}"

            elif opcode == "TRAP":
                trap_vector = int(parts[1][1:], 16) if parts[1].startswith("x") else int(parts[1])
                if trap_vector < 0 or trap_vector > 255:
                    raise ValueError("El vector TRAP debe estar en el rango [0, 255].")
                bin_instr = f"{self.keys['TRAP']}0000{trap_vector:08b}"

            elif opcode == "NOT":
                DR = self.registers[parts[1]]
                SR = self.registers[parts[2]]
                bin_instr = f"{self.keys[opcode]}{DR}{SR}111111"

            elif opcode in ["RET", "RTI"]:
                bin_instr = f"{self.keys[opcode]}000000000000"

            else:
                raise ValueError(f"Opcode no soportado: {opcode}")

            bin_instr = bin_instr.ljust(16, '0')
            result.append(bin_instr)
        return "\n".join(result)

    def binary_to_assembly(self, binary_code):
        lines = binary_code.strip().split('\n')
        result = []
        for line_num, line in enumerate(lines):
            if not line.strip():
                continue
            
            line = line.ljust(16, '0')
            opcode_bin = line[:4]
            opcode = next((key for key, value in self.keys.items() if value == opcode_bin), None)

            if not opcode:
                raise ValueError(f"Binario no reconocido: {line}")

            if opcode == "BR":
                condition_bits = line[4:7]
                condition = next((key for key, value in self.condition_bits.items() if value == condition_bits), "")
                offset = int(line[7:], 2)
                if offset & 0b100000000:
                    offset -= 512
                result.append(f"BR{condition} LABEL_{line_num + offset + 1}")

            elif opcode == "TRAP":
                trap_vector = int(line[8:], 2)
                result.append(f"TRAP x{trap_vector:02X}")

            elif opcode == "NOT":
                DR = self.reverse_registers[line[4:7]]
                SR = self.reverse_registers[line[7:10]]
                result.append(f"NOT {DR}, {SR}")

            elif opcode in ["ADD", "AND"]:
                DR = self.reverse_registers[line[4:7]]
                SR1 = self.reverse_registers[line[7:10]]
                if line[10] == "1":
                    imm5 = int(line[11:], 2)
                    if imm5 & 0b10000:
                        imm5 -= 32
                    result.append(f"{opcode} {DR}, {SR1}, #{imm5}")
                else:
                    SR2 = self.reverse_registers[line[13:]]
                    result.append(f"{opcode} {DR}, {SR1}, {SR2}")

            elif opcode in ["LD", "ST", "LEA", "LDI", "STI"]:
                DR = self.reverse_registers[line[4:7]]
                offset = int(line[7:], 2)
                if offset & 0b100000000:
                    offset -= 512
                result.append(f"{opcode} {DR}, LABEL_{line_num + offset + 1}")

            elif opcode in ["LDR", "STR"]:
                DR = self.reverse_registers[line[4:7]]
                BaseR = self.reverse_registers[line[7:10]]
                offset = int(line[10:], 2)
                if offset & 0b100000:
                    offset -= 64
                result.append(f"{opcode} {DR}, {BaseR}, #{offset}")

            elif opcode == "JMP":
                baseR = self.reverse_registers[line[7:10]]
                result.append(f"JMP {baseR}")

            elif opcode == "JSR":
                if line[4] == "0":  # JSRR
                    baseR = self.reverse_registers[line[7:10]]
                    result.append(f"JSRR {baseR}")
                else:  # JSR
                    offset = int(line[5:], 2)
                    if offset & 0b10000000000:
                        offset -= 2048
                    result.append(f"JSR LABEL_{line_num + offset + 1}")

            elif opcode in ["RET", "RTI"]:
                result.append(opcode)

            else:
                raise ValueError(f"Opcode no implementado: {opcode}")

        return "\n".join(result)

# Prueba del código
conv = Conversor()

assembly_code = """
START: ADD R1, R2, #3
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
          BR START
NEGATIVE: ADD R2, R2, #-1
          BR START
ZERO:    AND R2, R2, #0
         BR START
DONE:   JSR SUBRUTINA
        RET
SUBRUTINA: STI R7, SAVE_R7
           LDI R7, RESTORE_R7
           RTI
DATA:  .FILL x3000
SAVE_R7: .BLKW 1
RESTORE_R7: .FILL x0000
END:   TRAP x25
"""

binary_code = conv.assembly_to_binary(assembly_code)
print("Ensamblador a Binario:\n", binary_code)

binary_input = binary_code.strip()
assembly_output = conv.binary_to_assembly(binary_input)
print("\nBinario a Ensamblador:\n", assembly_output)
