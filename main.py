import tkinter as tk
from tkinter import messagebox
import math

#--- Lógica Básica dia 02 --- #
def clicar_botao(valor):
    # Insere o texto do botão no final do que já está no display
    atual=display.get()
    display.delete(0, tk.END)
    display.insert(0, atual + str(valor))

def limpar_tela():
    display.delete( 0, tk.END)

def calcular():
    try:
        expressao = display.get()
        # O eval resolve a string. Ex: "2**3" vira 8
        resultado = eval(expressao)
        display.delete(0, tk.END)
        display.insert(0, resultado)
    except Exception:
        messagebox.showerror("Erro", "Conta inválida!")
        limpar_tela()

def calcular_raiz():
    try:
        # Pega o número atual, calcula a raiz e substitui no visor
        valor = float(display.get())
        resultado = math.sqrt(valor)
        display.delete(0, tk.END)
        display.insert(0, resultado)
    except Exception:
        messagebox.showerror("Erro", "Impossível calcular raiz deste valor")

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
# Acrescentei '**' (Potência) e '√' (Raiz)
# Lista com os textos dos botões
botoes = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+',
    '**','√' #  botões científicos
]

linha = 0
coluna = 0

for texto in botoes:
    # Lógica de conexão dos comandos
    if texto == "=":
        comando = calcular
    elif texto == "C":
        comando = limpar_tela
    elif texto == "√":
        comando = calcular_raiz
    else:
        # O lambda é essencial aqui para passar o número/operador como texto
        comando = lambda t=texto: clicar_botao(t)

    # Criando o botão com o estilo 
    btn = tk.Button(frame_botoes, text=texto, width=5, height=2, 
                    bg="#69a9ba", fg="white", 
                    font=("Times New Roman", 14, "bold"),
                    relief="flat",
                    command=comando) # Adicionamos essa linha para o clique funcionar!
    # Colocando o botão na grade
    btn.grid(row=linha, column=coluna, padx=5, pady=5, sticky="nsew")
    
    coluna += 1
    if coluna > 3: # Quando chegar na 4ª coluna, pula para a próxima linha
        coluna = 0
        linha += 1

# Fazendo os botões crescerem por igual
# Fazendo os botões crescerem por igual nas colunas (0 a 3)
for i in range(4):
    frame_botoes.grid_columnconfigure(i, weight=1)

# Fazendo os botões crescerem por igual nas linhas (agora são 5 linhas, de 0 a 4)
for i in range(5): 
    frame_botoes.grid_rowconfigure(i, weight=1)

# O mainloop deve ficar SEMPRE por último
root.mainloop()
