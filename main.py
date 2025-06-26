import re

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
        self.executed_binaries = []  # Armazena as instruções convertidas para binário

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
        self._pc_modified = False
        self.execute_instruction(instr)
        if not self._pc_modified:
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

        # Saltos condicionais (BEQ/BNE) com fix para não pular instrução da label
        elif opcode == "BEQ":
            rs, rt, label = tokens[1:4]
            if self.registers[rs] == self.registers[rt]:
                self.pc = self.labels[label]
                self._pc_modified = True
                # Parte binária: o offset real não é calculado, só exemplo!
        elif opcode == "BNE":
            rs, rt, label = tokens[1:4]
            if self.registers[rs] != self.registers[rt]:
                self.pc = self.labels[label]
                self._pc_modified = True
                # Parte binária: o offset real não é calculado, só exemplo!

        # Saída (imprimir inteiro)
        elif opcode == "PRINT":
            reg = tokens[1]
            print(self.registers[reg])

        # Fim do programa
        elif opcode == "HALT":
            self.pc = len(self.instructions)  # Força parada
            self._pc_modified = True

        else:
            raise ValueError(f"Instrução não reconhecida: {opcode}")

        # ==============================
        # BLOCO DA CONVERSÃO PARA BINÁRIO
        # ==============================
        bin_instr = self.assembly_to_binary(instr)
        if bin_instr:
            self.executed_binaries.append(bin_instr)
        # ==============================
        # FIM DO BLOCO BINÁRIO
        # ==============================

    # =========================================
    # MÉTODO DE CONVERSÃO SIMPLIFICADO PARA BINÁRIO
    # =========================================
    def assembly_to_binary(self, instr):
        """
        Converte uma instrução Assembly MIPS simples para uma string binária (exemplo).
        Este método cobre apenas o subconjunto básico e serve como demonstração didática.
        """
        tokens = re.split(r'[,\s()]+', instr)
        if not tokens or not tokens[0]:
            return ""
        opcode = tokens[0].upper()
        # Mapas de opcode/funct (parcial, para fins didáticos)
        opcode_map = {
            "ADD":  "000000",
            "SUB":  "000000",
            "AND":  "000000",
            "OR":   "000000",
            "SLL":  "000000",
            "ADDI": "001000",
            "LW":   "100011",
            "SW":   "101011",
            "BEQ":  "000100",
            "BNE":  "000101",
            "SLT":  "000000",
            "PRINT":"111111",  # Não existe em MIPS real, só para visualização
            "HALT": "111110"   # Não existe em MIPS real, só para visualização
        }
        funct_map = {
            "ADD": "100000",
            "SUB": "100010",
            "AND": "100100",
            "OR":  "100101",
            "SLL": "000000",
            "SLT": "101010"
        }
        reg_bin = {name: format(i, '05b') for i, name in enumerate(REG_NAMES)}
        if opcode in ["ADD", "SUB", "AND", "OR", "SLT"]:
            # Exemplo: ADD rd, rs, rt
            rd, rs, rt = tokens[1:4]
            return f"{opcode_map[opcode]}{reg_bin[rs]}{reg_bin[rt]}{reg_bin[rd]}00000{funct_map[opcode]}"
        elif opcode == "SLL":
            rd, rt, shamt = tokens[1:4]
            return f"{opcode_map[opcode]}00000{reg_bin[rt]}{reg_bin[rd]}{format(int(shamt),'05b')}{funct_map[opcode]}"
        elif opcode == "ADDI":
            rt, rs, imm = tokens[1:4]
            return f"{opcode_map[opcode]}{reg_bin[rs]}{reg_bin[rt]}{format(int(imm)&0xFFFF,'016b')}"
        elif opcode in ["LW", "SW"]:
            rt, offset, base = tokens[1], tokens[2], tokens[3]
            return f"{opcode_map[opcode]}{reg_bin[base]}{reg_bin[rt]}{format(int(offset)&0xFFFF,'016b')}"
        elif opcode in ["BEQ", "BNE"]:
            rs, rt, label = tokens[1:4]
            # Offset real não é calculado aqui, só exemplo:
            return f"{opcode_map[opcode]}{reg_bin[rs]}{reg_bin[rt]}{'0'*16}"
        elif opcode == "PRINT":
            reg = tokens[1]
            return f"{opcode_map[opcode]}{'0'*21}{reg_bin[reg]}{'0'*5}"
        elif opcode == "HALT":
            return f"{opcode_map[opcode]}{'0'*26}"
        else:
            return ""
    # =========================================
    # FIM DO BLOCO DE CONVERSÃO PARA BINÁRIO
    # =========================================

    def get_registers(self):
        return self.registers.as_dict()

    def get_memory(self):
        return self.memory.as_dict()

    def show_state(self):
        print("Registradores:")
        print(self.registers)
        print("\nMemória:")
        print(self.memory)