import ply.yacc as yacc
from .lexer import tokens, lexer
from .semantic import analyze
import json
# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# Diccionario de nombres (para almacenar variables)
names = {}

# Reglas de gramática
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : var_declaration
                 | function_declaration
                 | expression_statement
                 | return_statement'''
    p[0] = p[1]

def p_var_declaration(p):
    '''var_declaration : VAR ID ASSIGN expression SEMICOLON'''
    p[0] = ('var_declaration', p[2], p[4])

def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN parameters RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('function_declaration', p[2], p[4], p[7])

def p_parameters(p):
    '''parameters : ID
                  | parameters COMMA ID
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    p[0] = []

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return_statement', p[2])

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = ('expression_statement', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = ('id', p[1])

# Regla para manejar errores
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
        parser.errok()
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

def test_js_lexer(input_string):
    """Ejecuta el lexer sobre el string de entrada y recopila los valores de los tokens generados."""
    lexer.input(input_string)
    tokens = []
    for tok in lexer:
        tokens.append(tok.value)
    return tokens

def test_js_parser(input_string):
    """ Analiza el string de entrada y retorna el resultado del análisis sintáctico. """
    result = parser.parse(input_string, lexer=lexer)
    return result

def print_js_ast(node, level=0):
    """ Construye y retorna una representación en cadena del AST con sangría para mostrar la estructura. """
    indent = "  " * level
    result = ""
    
    if isinstance(node, dict):
        node_type = node.get('type', 'Unknown')
        node_info = node.get('info', 'None')
        result += f"{indent}{node_type} (Info: {node_info})\n"
        children = node.get('children', [])
        for child in children:
            result += print_js_ast(child, level + 1)
    elif isinstance(node, list):
        for child in node:
            result += print_js_ast(child, level)
    else:
        result += f"{indent}- {node}\n"
    return result

def run_js_tests(input_string):
    """ Ejecuta todas las pruebas: lexing, parsing y la impresión del AST, y retorna los resultados concatenados en un solo string. """
    lexer_results = test_js_lexer(input_string)
    parser_results = test_js_parser(input_string)
    if parser_results:
        ast_representation = print_js_ast(parser_results)
        if ast_representation:
               semantic = analyze(parser_results, names)
    else:
        ast_representation = "No valid AST generated or parser error."
    
    final_results = f"Lexer JavaScript Output:\n{lexer_results}\n\nAST Representation:\n\n{ast_representation}\n\nSemantic Analysis:\n{semantic}"
    return final_results
