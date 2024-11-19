class LC3Simulator:
    def __init__(self):
        # Inicializar registros, flags y memoria
        self.registers = {f"R{i}": 0 for i in range(8)}  # R0 a R7
        self.flags = {"N": 0, "Z": 1, "P": 0}  # Solo uno de los flags puede estar activo
        self.PC = 0  # Program Counter
        self.memory = {}  # Memoria (dirección -> instrucción)
        self.current_instruction = None  # Instrucción actual

    def load_instructions(self, instructions_text):
        """Carga las instrucciones en memoria desde un texto."""
        self.memory = {}
        instructions = [line.strip() for line in instructions_text.split("\n") if line.strip()]
        for i, instruction in enumerate(instructions):
            self.memory[self.PC + i] = instruction
        self.PC = 0  # Reiniciar el PC a la primera instrucción

    def execute_step(self):
        """Ejecuta una sola instrucción."""
        if self.PC not in self.memory:
            print("No hay más instrucciones para ejecutar.")
            return

        self.current_instruction = self.memory[self.PC]
        opcode = self.current_instruction[:4]

        # Decodificar y ejecutar la instrucción
        if opcode == "0001":  # ADD
            self._execute_add()
        elif opcode == "0101":  # AND
            self._execute_and()
        elif opcode == "1111":  # TRAP
            self._execute_trap()
        # ... Otros opcodes a implementar
        else:
            print(f"Opcode desconocido: {opcode}")

        self.PC += 1  # Avanzar el PC

    def execute_all(self):
        """Ejecuta todas las instrucciones automáticamente."""
        while self.PC in self.memory:
            self.execute_step()

    def _update_flags(self, result):
        """Actualiza las banderas NZP basado en el resultado."""
        if result == 0:
            self.flags = {"N": 0, "Z": 1, "P": 0}
        elif result > 0:
            self.flags = {"N": 0, "Z": 0, "P": 1}
        else:
            self.flags = {"N": 1, "Z": 0, "P": 0}

    def _execute_add(self):
        """Ejecuta una instrucción ADD."""
        dr = int(self.current_instruction[4:7], 2)  # Destino
        sr1 = int(self.current_instruction[7:10], 2)  # Fuente 1
        if self.current_instruction[10] == "0":  # Modo registro
            sr2 = int(self.current_instruction[13:], 2)
            self.registers[f"R{dr}"] = self.registers[f"R{sr1}"] + self.registers[f"R{sr2}"]
        else:  # Inmediato
            imm5 = int(self.current_instruction[11:], 2)
            self.registers[f"R{dr}"] = self.registers[f"R{sr1}"] + imm5
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_and(self):
        """Ejecuta una instrucción AND."""
        dr = int(self.current_instruction[4:7], 2)  # Destino
        sr1 = int(self.current_instruction[7:10], 2)  # Fuente 1
        if self.current_instruction[10] == "0":  # Modo registro
            sr2 = int(self.current_instruction[13:], 2)
            self.registers[f"R{dr}"] = self.registers[f"R{sr1}"] & self.registers[f"R{sr2}"]
        else:  # Inmediato
            imm5 = int(self.current_instruction[11:], 2)
            self.registers[f"R{dr}"] = self.registers[f"R{sr1}"] & imm5
        self._update_flags(self.registers[f"R{dr}"])

    def _execute_trap(self):
        """Ejecuta una instrucción TRAP (simulación básica)."""
        trap_vector = int(self.current_instruction[8:], 2)
        print(f"TRAP ejecutado: x{trap_vector:02X}")

    def show_state(self):
        """Muestra el estado actual del simulador."""
        print(f"PC: {self.PC:04X} <- Instrucción actual")
        print("Registros:")
        for reg, value in self.registers.items():
            print(f"  {reg}: {value:04X}")
        print("Flags: N={} Z={} P={}".format(self.flags["N"], self.flags["Z"], self.flags["P"]))
        print("-" * 40)


# Prueba
instructions = """
0001000000100011
0101010010100111
0001001111000101
0001001111111110
1111000000100101
"""

simulator = LC3Simulator()
simulator.load_instructions(instructions)

print("=== Ejecución Paso a Paso ===")
while simulator.PC in simulator.memory:
    simulator.show_state()
    simulator.execute_step()
print("=== Ejecución Completa ===")
simulator.show_state()