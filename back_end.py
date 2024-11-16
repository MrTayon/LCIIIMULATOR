
class Conversor:
    def __init__(self):
        
        self.keys = {"ADD":"0001" , "AND":"0101" ,"BR":"0000" , "JMP":"1100", "JSR":"0100" ,
                     "LD":"0010", "LDI":"1010", "LDR":"0110" , "LEA":"1110" , "NOT":"1001" ,
                     "RET":"1100" , "RTI":"1000" , "ST":"0011" , "STI":"1011" ,"STR":"0111" ,
                     "TRAP":"1111" , "reserved":"1101"}


        self.registers = {f"R{i}": f"{i:03b}" for i in range(8)}  # R0-R7 in binary

    def assambly_to_binary(self, textAssambly: str) -> str:
        """Converts LC-3 assembly instructions to binary (supports multiple lines)."""
        try:
            lines = textAssambly.strip().split("\n")
            binary_lines = []
            for line in lines:
                parts = line.split()
                opcode = parts[0].upper()
                args = parts[1:]

                # Find binary opcode
                opcode_bin = self.keys.get(opcode)
                if not opcode_bin:
                    raise ValueError(f"Unknown opcode: {opcode}")

                # Process arguments (registers or immediate values)
                binary_parts = [opcode_bin]
                for arg in args:
                    if arg in self.registers:  # It's a register
                        binary_parts.append(self.registers[arg])
                    elif arg.isdigit():  # It's an immediate value
                        imm_value = int(arg)
                        binary_parts.append(format(imm_value & 0x1F, "05b"))  # Handle 5-bit immediates
                    else:
                        raise ValueError(f"Invalid argument: {arg}")

                # Join binary parts
                binary_lines.append("".join(binary_parts))
            return "\n".join(binary_lines)

        except Exception as e:
            return f"Error: {str(e)}"

    def binary_to_assambly(self, textBinary: str) -> str:
        """Converts LC-3 binary instructions to assembly (supports multiple lines)."""
        try:
            lines = textBinary.strip().split("\n")
            assembly_lines = []
            for binary in lines:
                opcode_bin = binary[:4]
                opcode = next(
                    (key for key, value in self.keys.items() if value == opcode_bin), None
                )
                if not opcode:
                    raise ValueError(f"Unknown binary opcode: {opcode_bin}")

                binary_args = binary[4:]
                args = []
                while binary_args:
                    if len(binary_args) >= 3 and binary_args[:3] in self.registers.values():
                        reg_bin = binary_args[:3]
                        reg = next(key for key, value in self.registers.items() if value == reg_bin)
                        args.append(reg)
                        binary_args = binary_args[3:]
                    elif len(binary_args) >= 5:
                        imm_bin = binary_args[:5]
                        imm_value = int(imm_bin, 2)
                        args.append(str(imm_value))
                        binary_args = binary_args[5:]
                    else:
                        break

                assembly_lines.append(f"{opcode} {' '.join(args)}")

            return "\n".join(assembly_lines)

        except Exception as e:
            return f"Error: {str(e)}"


# Crear una instancia del Conversor para pruebas
conversor = Conversor()

# Pruebas con múltiples líneas de ensamblador a binario y viceversa
assembly_block = """
ADD R1 R2 3
AND R3 R4 7
NOT R5 R6
"""

binary_block = """
000100101000011
010111000110011
100111101110000
"""

binary_output_block = conversor.assambly_to_binary(assembly_block)
assembly_output_block = conversor.binary_to_assambly(binary_block)

binary_output_block, assembly_output_block


print(binary_output_block)
print(assembly_output_block)
