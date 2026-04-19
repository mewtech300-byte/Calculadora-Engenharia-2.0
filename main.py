import tkinter as tk
from tkinter import ttk

# Configuração da Janela Principal
root = tk.Tk()
root.title("Calculadora de Engenharia")
root.geometry("400x600")
root.configure(bg="#0c375e") # Cor de fundo elegante

# Display (Onde aparecem os números e fórmulas)
display = tk.Entry(root, font=("Times New Roman", 24), bg="#f0ede9", fg="#0c375e", borderwidth=5, relief="flat", justify="right")
display.pack(fill="both", padx=20, pady=20)

# Container para os botões
frame_botoes = tk.Frame(root, bg="#0c375e")
frame_botoes.pack(fill="both", expand=True, padx=10, pady=10)

# --- Grade de Botões ---
# Lista com os textos dos botões
botoes = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

linha = 0
coluna = 0

for texto in botoes:
    # Criando o botão com o estilo que você escolheu
    btn = tk.Button(frame_botoes, text=texto, width=5, height=2, 
                    bg="#69a9ba", fg="white", 
                    font=("Times New Roman", 14, "bold"),
                    relief="flat")
    
    # Colocando o botão na grade
    btn.grid(row=linha, column=coluna, padx=5, pady=5, sticky="nsew")
    
    coluna += 1
    if coluna > 3: # Quando chegar na 4ª coluna, pula para a próxima linha
        coluna = 0
        linha += 1

# Fazendo os botões crescerem por igual
for i in range(4):
    frame_botoes.grid_columnconfigure(i, weight=1)
for i in range(4):
    frame_botoes.grid_rowconfigure(i, weight=1)
    # Final que me esqueci coloquei de novo e ela rodou.
    root.mainloop()