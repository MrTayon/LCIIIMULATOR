class Conversor:
    def __init__(self):
        # Mapa de opcodes e instrucciones
        self.keys = {
            "ADD": "0001", "AND": "0101", "BR": "0000", "JMP": "1100",
            "JSR": "0100", "LD": "0010", "LDI": "1010", "LDR": "0110",
            "LEA": "1110", "NOT": "1001", "RET": "1100", "RTI": "1000",
            "ST": "0011", "STI": "1011", "STR": "0111", "TRAP": "1111",
            "reserved": "1101"
        }

        self.registers = {f"R{i}": f"{i:03b}" for i in range(8)}  # R0-R7 en binario

    def assembly_to_binary(self, assembly_code, label_addresses=None):
        lines = assembly_code.strip().split('\n')
        result = []
        for line in lines:
            if not line.strip():  # Ignorar líneas vacías
                continue
            parts = line.replace(',', '').split()
            opcode = parts[0]
            bin_instr = ""

            if opcode not in self.keys:
                raise ValueError(f"Opcode no soportado: {opcode}")

            # Instrucciones tipo R o inmediato
            if opcode in ["ADD", "AND"]: 
                DR = self.registers[parts[1]]
                SR1 = self.registers[parts[2]]
                if "#" in parts[3]:  # Modo inmediato
                    imm5 = int(parts[3][1:])
                    if imm5 < 0:
                        imm5 = (1 << 5) + imm5  # Complemento a 2 para negativos
                    imm5 = f"{imm5:05b}"
                    bin_instr = f"{self.keys[opcode]}{DR}{SR1}1{imm5}"
                else:  # Modo registro
                    SR2 = self.registers[parts[3]]
                    bin_instr = f"{self.keys[opcode]}{DR}{SR1}0{SR2}"

            # Instrucciones de tipo PC-offset
            elif opcode in ["LD", "LDR", "LEA"]:  
                DR = self.registers[parts[1]]
                label = parts[2]

                if label_addresses and label in label_addresses:
                    offset = label_addresses[label] - (len(result) + 1)  # Calcula el desplazamiento relativo al PC
                else:
                    raise ValueError(f"Etiqueta no encontrada: {label}")

                if offset < 0:
                    offset = (1 << 9) + offset  # Complemento a 2 para números negativos
                offset = f"{offset:09b}"
                bin_instr = f"{self.keys[opcode]}{DR}{offset}"

            # Instrucción tipo J (salto)
            elif opcode in ["JMP", "JSR"]:
                if opcode == "JMP":
                    baseR = self.registers[parts[1]]
                    bin_instr = f"{self.keys[opcode]}{baseR}000000000"
                else:  # JSR
                    bin_instr = f"{self.keys[opcode]}000{baseR}000000000"

            # Instrucción tipo TRAP
            elif opcode == "TRAP":
                trap_vector = f"{int(parts[1]):08b}"  # Convertir el número a binario de 8 bits
                bin_instr = f"{self.keys[opcode]}{trap_vector}"

            # Instrucciones tipo R
            elif opcode == "NOT":  # Instrucción tipo R
                DR = self.registers[parts[1]]
                SR = self.registers[parts[2]]
                bin_instr = f"{self.keys[opcode]}{DR}{SR}111111"

            # Instrucción tipo BR (condicional de salto)
            elif opcode == "BR":
                condition = parts[1]  # Puede ser "n", "z", "p", o combinaciones
                label = parts[2]
                condition_bits = {
                    "n": "100", "z": "010", "p": "001", "nz": "110",
                    "np": "101", "zp": "011", "nzp": "111"
                }
                if label_addresses and label in label_addresses:
                    offset = label_addresses[label] - (len(result) + 1)
                else:
                    raise ValueError(f"Etiqueta no encontrada: {label}")
                if offset < 0:
                    offset = (1 << 9) + offset  # Complemento a 2 para números negativos
                offset = f"{offset:09b}"
                bin_instr = f"{self.keys[opcode]}{condition_bits[condition]}{offset}"

            # Instrucción tipo STI, STR (almacenamiento)
            elif opcode in ["ST", "STI", "STR"]:
                DR = self.registers[parts[1]]
                label = parts[2]

                if label_addresses and label in label_addresses:
                    offset = label_addresses[label] - (len(result) + 1)
                else:
                    raise ValueError(f"Etiqueta no encontrada: {label}")
                if opcode == "ST":
                    bin_instr = f"{self.keys[opcode]}{DR}{offset}"
                else:
                    SR = self.registers[parts[3]]
                    bin_instr = f"{self.keys[opcode]}{DR}{SR}{offset}"

            # Instrucción tipo RTI (restaurar contexto)
            elif opcode == "RTI":
                bin_instr = f"{self.keys[opcode]}0000000000"

            # Instrucción tipo RET (retorno de llamada)
            elif opcode == "RET":
                bin_instr = f"{self.keys[opcode]}0000000000"

            else:
                raise ValueError(f"Estructura no implementada para el opcode: {opcode}")

            # Asegurar 16 bits de longitud
            bin_instr = bin_instr.ljust(16, '0')
            result.append(bin_instr)
        return "\n".join(result)

    def binary_to_assembly(self, binary_code):
        lines = binary_code.strip().split('\n')
        result = []
        for line in lines:
            if not line.strip():  # Ignorar líneas vacías
                continue
            line = line.ljust(16, '0')  # Asegurar que tiene 16 bits
            opcode_bin = line[:4]
            opcode = next((key for key, value in self.keys.items() if value == opcode_bin), None)

            if not opcode:
                raise ValueError(f"Binario no reconocido: {line}")

            if opcode in ["ADD", "AND"]:  # Instrucciones tipo R o inmediato
                DR = f"R{int(line[4:7], 2)}"
                SR1 = f"R{int(line[7:10], 2)}"
                mode = line[10]
                if mode == "1":  # Modo inmediato
                    imm5 = int(line[11:], 2)
                    if imm5 >= 16:  # Convertir negativos
                        imm5 -= (1 << 5)
                    result.append(f"{opcode} {DR}, {SR1}, #{imm5}")
                else:  # Modo registro
                    SR2 = f"R{int(line[13:], 2)}"
                    result.append(f"{opcode} {DR}, {SR1}, {SR2}")

            elif opcode in ["LD", "LDR", "LEA"]:  # Instrucciones tipo PC-offset
                DR = f"R{int(line[4:7], 2)}"
                offset = int(line[7:], 2)
                if offset >= 256:  # Convertir negativos
                    offset -= (1 << 9)
                result.append(f"{opcode} {DR}, {offset}")

            elif opcode in ["JMP", "JSR"]:  # Instrucciones tipo J (salto)
                baseR = f"R{int(line[4:7], 2)}"
                result.append(f"{opcode} {baseR}")

            elif opcode == "TRAP":  # Instrucción TRAP
                trap_vector = int(line[4:], 2)
                result.append(f"{opcode} #{trap_vector}")

            elif opcode == "NOT":  # Instrucción tipo R
                DR = f"R{int(line[4:7], 2)}"
                SR = f"R{int(line[7:10], 2)}"
                result.append(f"{opcode} {DR}, {SR}")

            elif opcode == "BR":  # Instrucción BR (condicional de salto)
                condition = line[4:7]
                label = "Etiqueta no resuelta"  # Este campo depende del offset, se resuelve luego.
                condition_bits = {
                    "100": "n", "010": "z", "001": "p", "110": "nz",
                    "101": "np", "011": "zp", "111": "nzp"
                }
                result.append(f"{opcode} {condition_bits[condition]}, {label}")

            elif opcode in ["ST", "STI", "STR"]:  # Instrucciones de almacenamiento
                DR = f"R{int(line[4:7], 2)}"
                offset = int(line[7:], 2)
                result.append(f"{opcode} {DR}, {offset}")

            elif opcode == "RTI":  # Instrucción RTI
                result.append(f"{opcode}")

            elif opcode == "RET":  # Instrucción RET
                result.append(f"{opcode}")

        return "\n".join(result)

# Uso del código
conv = Conversor()

assembly_code = """ADD R1, R2, #3
AND R3, R4, #7
LD R5, A
LEA R6, B
JMP R7
TRAP #2
"""

binary_code = conv.assembly_to_binary(assembly_code)
print("Ensamblador a Binario:\n", binary_code)

# Convertir binario a ensamblador (simulado)
binary_input = binary_code.strip()
assembly_output = conv.binary_to_assembly(binary_input)
print("\nBinario a Ensamblador:\n", assembly_output)
