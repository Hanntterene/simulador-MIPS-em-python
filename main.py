import re

# ===============================
# Núcleo Simulador MIPS - main.py
# ===============================

# Lista dos nomes dos registradores
REG_NAMES = [
    "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
    "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
    "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
    "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
]

class Registers:
    def __init__(self):
        self.reg = {name: 0 for name in REG_NAMES}
        self.reg["$zero"] = 0  # $zero é sempre 0

    def __getitem__(self, reg):
        return self.reg[reg]

    def __setitem__(self, reg, value):
        if reg != "$zero":
            self.reg[reg] = value

    def as_dict(self):
        return dict(self.reg)

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.reg.items())

class Memory:
    def __init__(self):
        self.mem = {}  # Endereço (int) -> valor (int)

    def load(self, addr):
        return self.mem.get(addr, 0)

    def store(self, addr, value):
        self.mem[addr] = value

    def as_dict(self):
        return dict(self.mem)

    def __str__(self):
        result = []
        for addr in sorted(self.mem.keys()):
            result.append(f"[0x{addr:08x}]: {self.mem[addr]}")
        return "\n".join(result)

class MIPSSimulator:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()
        self.instructions = []
        self.labels = {}
        self.pc = 0  # índice da próxima instrução a executar

    def reset(self):
        self.__init__()

    def load_assembly(self, lines):
        """Carrega e faz o parse das linhas do programa Assembly."""
        self.instructions = []
        self.labels = {}
        for idx, line in enumerate(lines):
            line = line.strip()
            if "#" in line:
                line = line.split("#")[0].strip()
            if not line:
                continue
            # Marca label
            if ':' in line:
                label, rest = line.split(':', 1)
                self.labels[label.strip()] = len(self.instructions)
                if rest.strip():
                    self.instructions.append(rest.strip())
            else:
                self.instructions.append(line)
        self.pc = 0

    def step(self):
        """Executa uma única instrução."""
        if self.pc >= len(self.instructions):
            return False  # Fim do programa

        instr = self.instructions[self.pc].strip()
        self.execute_instruction(instr)
        self.pc += 1
        return True

    def run(self, step_by_step=False):
        """Executa o programa até o fim."""
        while self.pc < len(self.instructions):
            self.step()
            if step_by_step:
                input(f"Pressione Enter para executar a próxima instrução ({self.instructions[self.pc-1]})...")

    def execute_instruction(self, instr):
        """Executa uma única instrução em formato Assembly."""
        if not instr:
            return
        tokens = re.split(r'[,\s()]+', instr)
        opcode = tokens[0].upper()

        # Instruções do tipo R
        if opcode == "ADD":
            rd, rs, rt = tokens[1:4]
            self.registers[rd] = self.registers[rs] + self.registers[rt]
        elif opcode == "SUB":
            rd, rs, rt = tokens[1:4]
            self.registers[rd] = self.registers[rs] - self.registers[rt]
        elif opcode == "AND":
            rd, rs, rt = tokens[1:4]
            self.registers[rd] = self.registers[rs] & self.registers[rt]
        elif opcode == "OR":
            rd, rs, rt = tokens[1:4]
            self.registers[rd] = self.registers[rs] | self.registers[rt]
        elif opcode == "SLL":
            rd, rt, shamt = tokens[1:4]
            self.registers[rd] = self.registers[rt] << int(shamt)

        # Instruções do tipo I
        elif opcode == "ADDI":
            rt, rs, imm = tokens[1:4]
            self.registers[rt] = self.registers[rs] + int(imm)
        elif opcode == "LW":
            rt, offset, base = tokens[1], tokens[2], tokens[3]
            addr = self.registers[base] + int(offset)
            self.registers[rt] = self.memory.load(addr)
        elif opcode == "SW":
            rt, offset, base = tokens[1], tokens[2], tokens[3]
            addr = self.registers[base] + int(offset)
            self.memory.store(addr, self.registers[rt])
        elif opcode == "SLT":
            rd, rs, rt = tokens[1:4]
            self.registers[rd] = int(self.registers[rs] < self.registers[rt])

        # Saltos condicionais (simples, usando labels)
        elif opcode == "BEQ":
            rs, rt, label = tokens[1:4]
            if self.registers[rs] == self.registers[rt]:
                self.pc = self.labels[label]
                return  # Importante: não incrementa PC depois de salto
        elif opcode == "BNE":
            rs, rt, label = tokens[1:4]
            if self.registers[rs] != self.registers[rt]:
                self.pc = self.labels[label]
                return

        # Saída (imprimir inteiro)
        elif opcode == "PRINT":
            reg = tokens[1]
            print(self.registers[reg])

        # Fim do programa
        elif opcode == "HALT":
            self.pc = len(self.instructions)  # Força parada

        else:
            raise ValueError(f"Instrução não reconhecida: {opcode}")

    def get_registers(self):
        return self.registers.as_dict()

    def get_memory(self):
        return self.memory.as_dict()

    def show_state(self):
        print("Registradores:")
        print(self.registers)
        print("\nMemória:")
        print(self.memory)

# ===============================
# Exemplo de uso
# ===============================
if __name__ == "__main__":
    sim = MIPSSimulator()
    # Exemplo de programa em Assembly (pode ser substituído por leitura de arquivo)
    programa = [
        "ADD $t0, $zero, $zero",
        "ADDI $t0, $t0, 5",
        "ADDI $t1, $zero, 10",
        "ADD $t2, $t0, $t1",
        "SW $t2, 0, $zero",
        "LW $t3, 0, $zero",
        "PRINT $t3",
        "HALT"

# add $t0, $t0, $zero
# addi $t0, $zero, 5
# print $t0

    ]
    sim.load_assembly(programa)
    sim.run()
    sim.show_state()