import tkinter as tk
from tkinter import messagebox
import sympy as sp
import re

# --- CONFIGURAÇÕES DE TRADUÇÃO ---
MAPA_SOBRE = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
MAPA_NORMAL = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")

def formatar_resultado_visual(resultado_obj):
    if resultado_obj.is_Number and abs(resultado_obj) < 1e-12: return "0"
    texto = str(resultado_obj)
    texto = re.sub(r'\*\*(\d+)', lambda m: m.group(1).translate(MAPA_SOBRE), texto)
    texto = texto.replace('sqrt', '√').replace('exp', 'e').replace('*', '').replace('pi', 'π').replace('.', ',')
    return texto

def limpar_para_calcular(texto):
    texto = texto.replace('X', '*')
    texto = texto.replace(',', '.')
    texto = re.sub(r'(\d)([a-zA-Z\(π])', r'\1*\2', texto)
    texto = re.sub(r'(\))(\d)', r'\1*\2', texto)
    texto = re.sub(r'(\d+)!', r'factorial(\1)', texto)
    texto = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹])√\((.*?)\)', lambda m: f"root({m.group(2)}, {m.group(1).translate(MAPA_NORMAL)})", texto)
    texto = re.sub(r'e([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: f"exp({m.group(1).translate(MAPA_NORMAL)})", texto)
    texto = re.sub(r'10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: f"10**({m.group(1).translate(MAPA_NORMAL)})", texto)
    for sobre, normal in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"):
        texto = texto.replace(sobre, f"**{normal}")
    texto = texto.replace('π', 'pi').replace('ln(', 'log(').replace('√(', 'sqrt(')
    if 'log₁₀' in display.get():
        texto = texto.replace('log₁₀(', 'log(')
        texto = re.sub(r'log\((.*?)\)', r'log(\1, 10)', texto)
    else:
        texto = texto.replace('log₁₀(', 'log(')
    return texto

# --- FUNÇÕES DE COMANDO ---
def calcular():
    try:
        conteudo = display.get()
        while conteudo.count('(') > conteudo.count(')'): conteudo += ')'
        expr_limpa = limpar_para_calcular(conteudo)
        resultado = sp.sympify(expr_limpa)
        display.delete(0, tk.END)
        display.insert(0, formatar_resultado_visual(resultado))
    except: messagebox.showerror("Erro", "Expressão inválida.")

def calcular_simbolico(tipo):
    try:
        x = sp.symbols('x')
        expr_limpa = limpar_para_calcular(display.get())
        expressao = sp.sympify(expr_limpa)
        res = sp.diff(expressao, x) if tipo == 'derivar' else sp.integrate(expressao, x)
        display.delete(0, tk.END)
        display.insert(0, formatar_resultado_visual(res))
    except: messagebox.showerror("Erro de Variável", "Para derivar ou integrar, use a letra 'x'.")

def acao_botao(texto):
    atual = display.get()
    if texto == "=": calcular()
    elif texto == "C": display.delete(0, tk.END)
    elif texto == "Del": display.delete(len(atual)-1, tk.END)
    elif texto == "derivar": calcular_simbolico('derivar')
    elif texto == "integrar": calcular_simbolico('integrar')
    elif texto == "1/x":
        if atual:
            match = re.search(r'(\d+[\,]?\d*)$|(\(.*\))$', atual)
            if match:
                alvo = match.group(); display.delete(len(atual) - len(alvo), tk.END)
                display.insert(tk.END, f"(1/{alvo})")
    elif texto in ["eˣ", "10ˣ", "ʸ√x"]:
        if atual and atual[-1].isdigit():
            num_final = re.search(r'\d+$', atual).group()
            sobre = num_final.translate(MAPA_SOBRE)
            display.delete(len(atual) - len(num_final), tk.END)
            if texto == "eˣ": display.insert(tk.END, f"e{sobre}")
            elif texto == "10ˣ": display.insert(tk.END, f"10{sobre}")
            elif texto == "ʸ√x": display.insert(tk.END, f"{sobre}√(")
        else:
            if texto == "ʸ√x": display.insert(tk.END, "√(")
            elif texto == "eˣ": display.insert(tk.END, "e")
            else: display.insert(tk.END, "10")
    elif texto == "x!":
        if atual and (atual[-1].isdigit() or atual[-1] == ')'): display.insert(tk.END, "!")
    elif texto in ["sin", "cos", "tan", "ln", "log₁₀", "√"]: display.insert(tk.END, f"{texto}(")
    elif texto == "x²": display.insert(tk.END, "²")
    elif texto == "x³": display.insert(tk.END, "³")
    elif texto == "π": display.insert(tk.END, "π")
    elif texto == ",": display.insert(tk.END, ",")
    else: display.insert(tk.END, texto)

# --- GUI E DESIGN  MEIO AMADEIRADO + VERDE MUSGO ---
root = tk.Tk()
root.title("Calculadora de Engenharia 3.0")
root.geometry("600x820")

COR_MADEIRA = "#3d2b1f" 
COR_VERDE_MUSGO = "#4b5320" # Tom de verde exército/musgo

root.configure(bg=COR_MADEIRA)

display = tk.Entry(root, font=("Times New Roman", 28), bg="black", fg="white", 
                  borderwidth=10, relief="sunken", justify="right", insertbackground="white")
display.pack(fill="both", padx=20, pady=25)

frame_botoes = tk.Frame(root, bg=COR_MADEIRA)
frame_botoes.pack(fill="both", expand=True, padx=10, pady=10)

botoes = [
    'C', 'Del', '(', ')', 'sin', 'derivar',
    '7', '8', '9', '/', 'cos', 'integrar',
    '4', '5', '6', 'X', 'tan', 'π',
    '1', '2', '3', '-', 'eˣ', 'x',
    '%', '0', ',', '+', '10ˣ', 'x!',
    'ʸ√x', '√', '1/x', '=', 'x²', 'x³',
    'log₁₀', 'ln'
]

l, c = 0, 0
for t in botoes:
    # LÓGICA DAS CORES
    if t in ['C', 'Del']:
        cor_bg, cor_fg = "yellow", "black"
    elif t == '=':
        cor_bg, cor_fg = "red", "white"
        fonte_btn = ("Times New Roman", 12, "bold")
    elif t.isdigit() or t in [',', 'derivar', 'integrar', '%']:
        cor_bg, cor_fg = "#d3d3d3", "black" # Cinza claro
    elif t in ['+', '-', 'X', '/']:
        cor_bg, cor_fg = "#ff8c00", "white" # Laranja Mecânica
        fonte_btn = ("Times New Roman", 12, "bold")

    else:
        #  VERDE MUSGO
        cor_bg, cor_fg = COR_VERDE_MUSGO, "white"

    if t != '=': fonte_btn = ("Times New Roman", 11, "bold")

    tk.Button(frame_botoes, text=t, bg=cor_bg, fg=cor_fg, font=fonte_btn, 
              relief="raised", borderwidth=2, command=lambda x=t: acao_botao(x)).grid(row=l, column=c, padx=3, pady=3, sticky="nsew")
    
    c += 1
    if c > 5: c = 0; l += 1

for i in range(6): frame_botoes.grid_columnconfigure(i, weight=1)
for i in range(7): frame_botoes.grid_rowconfigure(i, weight=1)

root.mainloop()
