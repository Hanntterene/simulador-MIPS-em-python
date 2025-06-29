# simulador-MIPS-em-python
# Autores: Luís Guilherme Amorim Dessia e Lohanna da Silva Monteiro

# Interface gráfica do simulador MIPS utilizando tkinter


import tkinter as tk
from tkinter import scrolledtext, messagebox
from main import MIPSSimulator
import io
import sys

# Estado global do simulador para execução passo a passo
sim_passo = None      # O simulador atual para passo a passo
codigo_passo = []     # Lista de linhas de código assembly para passo a passo

def executar():
    # Função chamada ao clicar no botão "OK" para executar o programa inteiro
    codigo = caixa_texto.get("1.0", tk.END).strip().splitlines()
    sim = MIPSSimulator()
    saida_print.delete("1.0", tk.END)
    resultado.delete("1.0", tk.END)
    saida_binario.delete("1.0", tk.END)  # Limpa a saída binária
    try:
        buffer = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer
        sim.load_assembly(codigo)
        sim.run()
        sys.stdout = sys_stdout_original
        # Mostra saída do PRINT primeiro
        saida_print.insert(tk.END, buffer.getvalue())
        # Mostra resultado do programa
        resultado.insert(tk.END, "Registradores:\n")
        resultado.insert(tk.END, str(sim.registers) + "\n")
        resultado.insert(tk.END, "Memória:\n")
        resultado.insert(tk.END, str(sim.memory) + "\n")
        # Mostra código binário executado
        saida_binario.delete("1.0", tk.END)
        if hasattr(sim, "executed_binaries"):
            for linha in sim.executed_binaries:
                saida_binario.insert(tk.END, linha + "\n")
    except Exception as e:
        sys.stdout = sys_stdout_original
        messagebox.showerror("Erro", str(e))

#Função para executar uma instrução por vez
def executar_passo():
    global sim_passo, codigo_passo
    if sim_passo is None or not hasattr(sim_passo, "instructions") or not sim_passo.instructions:
        # Inicializa o simulador e carrega o código na primeira vez
        codigo_passo = caixa_texto.get("1.0", tk.END).strip().splitlines()
        sim_passo = MIPSSimulator()
        sim_passo.load_assembly(codigo_passo)
    if sim_passo.pc >= len(sim_passo.instructions):
        messagebox.showinfo("Fim", "Fim do programa.")
        limpar_destaque()
        return

    # Destaca a linha que VAI SER executada agora (próxima)
    destacar_linha(sim_passo.pc)
    try:
        buffer = io.StringIO()
        sys_stdout_original = sys.stdout
        sys.stdout = buffer
        sim_passo.step()  # Executa a instrução destacada
        sys.stdout = sys_stdout_original

        # Após executar, já destaca a próxima linha (se houver)
        if sim_passo.pc < len(sim_passo.instructions):
            destacar_linha(sim_passo.pc)
        else:
            limpar_destaque()

        # Atualiza os campos normalmente
        saida_print.delete("1.0", tk.END)
        if hasattr(sim_passo, "output"):
            for linha in sim_passo.output:
                saida_print.insert(tk.END, linha + "\n")
        resultado.delete("1.0", tk.END)
        resultado.insert(tk.END, "Registradores:\n")
        resultado.insert(tk.END, str(sim_passo.registers) + "\n")
        resultado.insert(tk.END, "Memória:\n")
        resultado.insert(tk.END, str(sim_passo.memory) + "\n")
        saida_binario.delete("1.0", tk.END)
        if hasattr(sim_passo, "executed_binaries"):
            for linha in sim_passo.executed_binaries:
                saida_binario.insert(tk.END, linha + "\n")
    except Exception as e:
        sys.stdout = sys_stdout_original
        messagebox.showerror("Erro", str(e))
        limpar_destaque()
        
#Função para reiniciar o passo a passo
def reiniciar_passo():
    global sim_passo, codigo_passo
    sim_passo = None
    codigo_passo = []
    saida_print.delete("1.0", tk.END)
    resultado.delete("1.0", tk.END)
    saida_binario.delete("1.0", tk.END)
    limpar_destaque()

#Funções auxiliares para destacar linha a linha por instrução
def limpar_destaque():
    caixa_texto.tag_remove("destaque", "1.0", tk.END)

def destacar_linha(linha):
    limpar_destaque()
    index1 = f"{linha+1}.0"
    index2 = f"{linha+1}.end"
    caixa_texto.tag_add("destaque", index1, index2)
    caixa_texto.tag_config("destaque", background="#FFFF99")


root = tk.Tk()
root.title("Simulador MIPS")
root.geometry("900x700")  # Aumenta o tamanho da janela

fonte_label = ("Arial", 14, "bold")
fonte_texto = ("Consolas", 13)

tk.Label(root, text="Digite o código MIPS:", font=fonte_label).pack()
caixa_texto = scrolledtext.ScrolledText(root, width=80, height=12, font=fonte_texto)
caixa_texto.pack(pady=5)

#Botões para passo a passo
frame_botoes = tk.Frame(root)
frame_botoes.pack()
btn = tk.Button(frame_botoes, text="OK", command=executar, font=fonte_label, width=10)
btn.pack(side=tk.LEFT, padx=6)
btn_passo = tk.Button(frame_botoes, text="Executar Passo", command=executar_passo, font=fonte_label, width=15)
btn_passo.pack(side=tk.LEFT, padx=6)
btn_reset = tk.Button(frame_botoes, text="Reiniciar Passo", command=reiniciar_passo, font=fonte_label, width=15)
btn_reset.pack(side=tk.LEFT, padx=6)


# Cria um frame para os três campos de saída lado a lado
frame_saidas = tk.Frame(root)
frame_saidas.pack(fill=tk.BOTH, expand=True, pady=5)

# Saída do PRINT
frame_print = tk.Frame(frame_saidas)
frame_print.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
tk.Label(frame_print, text="Saída do PRINT:", font=fonte_label).pack()
saida_print = scrolledtext.ScrolledText(frame_print, width=30, height=18, font=fonte_texto)
saida_print.pack(fill=tk.BOTH, expand=True, pady=5)

# Resultado do programa
frame_resultado = tk.Frame(frame_saidas)
frame_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
tk.Label(frame_resultado, text="Resultado do programa:", font=fonte_label).pack()
resultado = scrolledtext.ScrolledText(frame_resultado, width=30, height=18, font=fonte_texto)
resultado.pack(fill=tk.BOTH, expand=True, pady=5)

# Código binário executado
frame_binario = tk.Frame(frame_saidas)
frame_binario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
tk.Label(frame_binario, text="Código binário executado:", font=fonte_label).pack()
saida_binario = scrolledtext.ScrolledText(frame_binario, width=30, height=18, font=fonte_texto)
saida_binario.pack(fill=tk.BOTH, expand=True, pady=5)

root.mainloop()