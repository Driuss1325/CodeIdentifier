import ply.lex as lex

# Lista de tokens
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE', 'SEMICOLON', 'ASSIGN', 'VAR', 'FUNCTION', 'RETURN',
    'COMMA'  # Agregado el token COMMA
]

# Palabras reservadas
reserved = {
    'var': 'VAR',
    'function': 'FUNCTION',
    'return': 'RETURN'
}

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_COMMA = r','  # Agregada la regla regular para el token COMMA

# Regla para identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es una palabra reservada
    return t

# Regla para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para ignorar espacios y tabs
t_ignore = ' \t'

# Regla para ignorar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    print(f"Illegal javascript character '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
