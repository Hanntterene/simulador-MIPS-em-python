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

tk.Label(root, text="Saída do PRINT:", font=fonte_label).pack()
saida_print = scrolledtext.ScrolledText(root, width=80, height=6, font=fonte_texto)
saida_print.pack(pady=5)

tk.Label(root, text="Resultado do programa:", font=fonte_label).pack()
resultado = scrolledtext.ScrolledText(root, width=80, height=16, font=fonte_texto)
resultado.pack(pady=5)

root.mainloop()
