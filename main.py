import tkinter as tk
from tkinter import messagebox
import sympy as sp
import re

# --- CONFIGURAÇÕES DE TRADUÇÃO E MEMÓRIA ---
MAPA_SOBRE = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
MAPA_NORMAL = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
memoria = 0 

def formatar_resultado_visual(resultado_obj):
    try:
        if resultado_obj.is_Number:
            if abs(resultado_obj) < 1e-12: return "0"
            res_formatado = f"{float(resultado_obj):.6f}".rstrip('0').rstrip('.')
            return res_formatado.replace('.', ',')
        texto = str(resultado_obj)
        texto = re.sub(r'\*\*(\d+)', lambda m: m.group(1).translate(MAPA_SOBRE), texto)
        texto = texto.replace('sqrt', '√').replace('exp', 'e').replace('*', '').replace('pi', 'π').replace('.', ',')
        return texto
    except: return str(resultado_obj)

def limpar_para_calcular(texto):
    texto = texto.replace('X', '*').replace('÷', '/')
    texto = texto.replace(',', '.')
    texto = re.sub(r'(\d+)!', r'factorial(\1)', texto)
    texto = re.sub(r'e([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: f"exp({m.group(1).translate(MAPA_NORMAL)})", texto)
    texto = re.sub(r'10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: f"10**({m.group(1).translate(MAPA_NORMAL)})", texto)
    texto = re.sub(r'([0-9x])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: f"{m.group(1)}**{m.group(2).translate(MAPA_NORMAL)}", texto)
    texto = re.sub(r'(\d)([a-zA-Zπ])', r'\1*\2', texto)
    texto = re.sub(r'(\))(\d)', r'\1*\2', texto)
    for sobre, normal in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"):
        texto = texto.replace(sobre, f"**{normal}")
    texto = texto.replace('π', 'pi').replace('ln(', 'log(').replace('√(', 'sqrt(').replace('%', '/100')
    return texto

def obter_valor_atual():
    try:
        conteudo = display.get()
        if not conteudo: return 0
        expr_limpa = limpar_para_calcular(conteudo)
        return float(sp.sympify(expr_limpa).evalf())
    except: return None

def calcular_simbolico(tipo):
    try:
        x = sp.symbols('x')
        expr_limpa = limpar_para_calcular(display.get())
        expressao = sp.sympify(expr_limpa)
        res = sp.diff(expressao, x) if tipo == 'derivar' else sp.integrate(expressao, x)
        display.delete(0, tk.END)
        display.insert(0, formatar_resultado_visual(res))
    except: messagebox.showerror("Erro", "Use 'x' para derivar/integrar.")

def acao_botao(texto):
    global modo_expoente, memoria
    atual = display.get()

    if texto == "=":
        try:
            parenteses_abertos = atual.count('(') - atual.count(')')
            if parenteses_abertos > 0: atual += ')' * parenteses_abertos
            expr_limpa = limpar_para_calcular(atual)
            resultado = sp.sympify(expr_limpa).evalf()
            display.delete(0, tk.END)
            display.insert(0, formatar_resultado_visual(resultado))
        except: messagebox.showerror("Erro", "Expressão inválida.")
        modo_expoente = False

    elif texto == "C": 
        display.delete(0, tk.END)
        modo_expoente = False

    elif texto == "⌫": 
        display.delete(len(atual)-1, tk.END)

    elif texto == "MC": 
        memoria = 0
        display.delete(0, tk.END)
    
    elif texto == "MR":
        display.delete(0, tk.END)
        display.insert(0, formatar_resultado_visual(sp.Float(memoria)))

    elif texto == "M+":
        v = obter_valor_atual()
        if v is not None: 
            memoria += v
            display.delete(0, tk.END)
    
    elif texto == "M-":
        v = obter_valor_atual()
        if v is not None: 
            memoria -= v
            display.delete(0, tk.END)

    elif texto == "derivar": calcular_simbolico('derivar')
    elif texto == "integrar": calcular_simbolico('integrar')

    elif texto == "EXP":
        display.insert(tk.END, "X10" if atual else "10")
        modo_expoente = True

    elif texto == "+/-":
        match = re.search(r'(\d+[\,]?\d*)$|x$', atual)
        if match:
            alvo = match.group()
            if atual.endswith(f"(-{alvo})"):
                display.delete(len(atual) - (len(alvo) + 3), tk.END)
                display.insert(tk.END, alvo)
            else:
                display.delete(len(atual) - len(alvo), tk.END)
                display.insert(tk.END, f"(-{alvo})")

    elif texto.isdigit():
        display.insert(tk.END, texto.translate(MAPA_SOBRE) if modo_expoente else texto)
    
    elif texto in ["sin", "cos", "tan", "log₁₀", "ln", "√"]:
        display.insert(tk.END, f"{texto}(")
    
    elif texto in ["+", "-", "X", "÷", "(", ")", "%"]:
        modo_expoente = False
        display.insert(tk.END, texto)

    elif texto == "x²": display.insert(tk.END, "²")
    elif texto == "x³": display.insert(tk.END, "³")
    elif texto == "xʸ": modo_expoente = True
    elif texto == "π": display.insert(tk.END, "π")
    elif texto == ",": display.insert(tk.END, ",")
    elif texto == "x!": display.insert(tk.END, "!")
    elif texto == "1/x":
        match = re.search(r'(\d+[\,]?\d*)$|x$', atual)
        if match:
            alvo = match.group()
            display.delete(len(atual) - len(alvo), tk.END)
            display.insert(tk.END, f"(1/{alvo})")
        else: display.insert(tk.END, "(1/")
    elif texto in ["eˣ", "10ˣ", "ʸ√x"]:
        match = re.search(r'\d+$', atual)
        if match:
            num = match.group(); sobre = num.translate(MAPA_SOBRE)
            display.delete(len(atual) - len(num), tk.END)
            if texto == "eˣ": display.insert(tk.END, f"e{sobre}")
            elif texto == "10ˣ": display.insert(tk.END, f"10{sobre}")
            elif texto == "ʸ√x": display.insert(tk.END, f"{sobre}√(")
        else: display.insert(tk.END, "√(" if texto == "ʸ√x" else ("e" if texto == "eˣ" else "10"))

# --- GUI ---
root = tk.Tk()
root.title("Calculadora de Engenharia 3.0")
root.geometry("700x850") 
COR_MADEIRA, COR_VERDE_MUSGO = "#3d2b1f", "#4b5320"
root.configure(bg=COR_MADEIRA)

display = tk.Entry(root, font=("Times New Roman", 28), bg="black", fg="white", 
                  borderwidth=10, relief="sunken", justify="right", insertbackground="white")
display.pack(fill="both", padx=20, pady=25)

frame_botoes = tk.Frame(root, bg=COR_MADEIRA)
frame_botoes.pack(fill="both", expand=True, padx=10, pady=10)

modo_expoente = False

# Organizado para 6 linhas completas de 7 colunas antes do botão '='
botoes = [
    'MC', 'MR', 'M+', 'M-', '(', ')', 'derivar',
    'C', '⌫', '%', '+/-', '÷', 'EXP', 'integrar',
    'sin', '7', '8', '9', 'X', 'x²', 'ʸ√x',
    'cos', '4', '5', '6', '-', 'x³', '1/x',
    'tan', '1', '2', '3', '+', 'xʸ', 'eˣ',
    'π', '√', '0', ',', 'ln', 'x', '10ˣ',
    'log₁₀',
]

l, c = 0, 0
for t in botoes:
    fonte_botao = ("Times New Roman", 11, "bold")
    
    # Lógica de Cores
    if t in ['MC', 'MR', 'M+', 'M-', 'derivar', 'integrar', 'EXP']:
        cor_bg, cor_fg = COR_VERDE_MUSGO, "white"
    elif t == 'C': 
        cor_bg, cor_fg = "#ceca0a", "black"
    elif t.isdigit() or t in [',', '⌫', '+/-', '%']: # % aqui com cor de número
        cor_bg, cor_fg = "#d3d3d3", "black"
    elif t in ['+', '-', 'X', '÷']: 
        cor_bg, cor_fg = "#d27c13", "white"
        fonte_botao = ("Times New Roman", 16, "bold")
    else: 
        cor_bg, cor_fg = COR_VERDE_MUSGO, "white"

    btn = tk.Button(frame_botoes, text=t, bg=cor_bg, fg=cor_fg, font=fonte_botao, 
                   relief="raised", borderwidth=2, command=lambda x=t: acao_botao(x))
    btn.grid(row=l, column=c, padx=3, pady=3, ipady=12, sticky="nsew")
    
    c += 1
    if c > 6: 
        c = 0
        l += 1

# CRIAR O BOTÃO '=' FORA DO LOOP PARA GARANTIR QUE APAREÇA NO FINAL
btn_igual = tk.Button(frame_botoes, text='=', bg="#831D1B", fg="white", font=("Times New Roman", 14, "bold"), 
                     relief="raised", borderwidth=2, command=lambda: acao_botao('='))
btn_igual.grid(row=l+1, column=0, columnspan=7, padx=3, pady=3, ipady=12, sticky="nsew")

# --- SIMETRIA ---
for i in range(7):
    frame_botoes.grid_columnconfigure(i, weight=1, uniform="equal")
for i in range(l + 2): # Ajustado para incluir a linha do '='
    frame_botoes.grid_rowconfigure(i, weight=1, uniform="equal")

root.mainloop()
