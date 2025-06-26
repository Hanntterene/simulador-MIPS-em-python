import tkinter as tk
from tkinter import scrolledtext, messagebox
from main import MIPSSimulator
import io
import sys

def executar():
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

root = tk.Tk()
root.title("Simulador MIPS")
root.geometry("900x700")  # Aumenta o tamanho da janela

fonte_label = ("Arial", 14, "bold")
fonte_texto = ("Consolas", 13)

tk.Label(root, text="Digite o código MIPS:", font=fonte_label).pack()
caixa_texto = scrolledtext.ScrolledText(root, width=80, height=12, font=fonte_texto)
caixa_texto.pack(pady=5)

btn = tk.Button(root, text="OK", command=executar, font=fonte_label, width=10)
btn.pack(pady=5)

# Remove o canvas e o scrollbar
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
