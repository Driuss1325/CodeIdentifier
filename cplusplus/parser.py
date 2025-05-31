import ply.yacc as yacc
from .lexer import *
import pprint
from .semantic import *
import json 

precedence = (
    ('left', 'ADDEQ', 'SUBEQ', 'MODEQ', 'MULTEQ', 'DIVEQ', '='),
    ('left', '?', ':'),
    ('left', 'LOGOR'),
    ('left', 'LOGAND'),
    ('left', '^'),
    ('left', 'LOGEQ', 'LOGNEQ'),
    ('left', '<', '>', 'LEQ', 'GEQ'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'LPLUSPLUS', 'LMINUSMINUS', 'LPOS', 'LNEG', 'LNOT', 'LAT'),
    ('left', 'RPLUSPLUS', 'RMINUSMINUS', '.', 'RARROW'),
    ('left', "THEN"),
    ('left', 'ELSE'),
)


class n:
    def __init__(self, type, children=[], info=None) -> None:
        self.type = type
        self.children = children
        self.info = info

    def __repr__(self) -> str:
        # return pprint.pformat({"type": self.type, "info": self.info, "children": self.children}, width=500, sort_dicts=False)
        return repr({"type": self.type, "info": self.info, "children": self.children})
# =========== For the whole program ===========


def p_program(p):
    """
        program : include program
                | external_decl program
    """
    p[0] = n("program", [p[1]] + p[2].children)


def p_program_end(p):
    """
        program : include
                | external_decl
    """
    p[0] = n("program", [p[1]])

# ----------------- program end -------------------

# =================== include =====================


def p_include(p):
    """
        include : INCLUDE
    """
    p[0] = n("include", [], p[1])

# ---------------- include end -------------------


def p_external_declaration(p):
    """
        external_decl   : decl ';'
                        | func_def
    """
    p[0] = n("external_decl", [p[1]])


def p_external_declaration_extra_semicolon(p):
    """
        external_decl : ';'
    """
    pass


def p_decl(p):
    """
        decl    : usual_dec
                | new_type_dec
    """
    p[0] = p[1]


def p_usual_decl(p):
    """
        usual_dec : type declarators
    """
    p[0] = n("usual_decl", [p[2]], p[1])

# ================ declarators ==================


def p_declarators(p):
    """
        declarators : declarator_1 ',' declarators
    """
    p[0] = n("declarators", [p[1]] + p[3].children)


def p_declarator_end(p):
    """
        declarators : declarator_1
    """
    p[0] = n("declarators", [p[1]])


def p_declarator_1(p):
    """
        declarator_1    : declarator_2
    """
    p[0] = p[1]


def p_declarator_1_winit(p):
    """
        declarator_1    : declarator_2 '=' initializer
    """
    p[0] = n("init", [p[1], p[3]])


def p_declarator_2_single(p):
    """
        declarator_2    : ID
    """
    p[0] = n("var", [], p[1])


def p_declarator_2_func(p):
    """
        declarator_2    : ID '(' ')'
    """
    p[0] = n("func_decl", [], info=p[1])


def p_declarator_2_array(p):
    """
        declarator_2    : ID '[' ']'
    """
    p[0] = n("arr_decl", [], info=p[1])


def p_declarator_2_arrray(p):
    """
        declarator_2    : ID '[' expression ']'
    """
    p[0] = n("arr_decl", [p[3]], info=p[1])


def p_initializer(p):
    """
        initializer : expression
                    | '{' expressions '}'
    """
    if (len(p) == 2):
        p[0] = n("initializer", [p[1]])
    else:
        p[0] = n("initializer", [p[2]])


# ---------------- declarators end -----------------

# ================= new_type ======================


def p_new_type_dec(p):
    """
        new_type_dec    : new_type ID '{' new_type_params '}'
    """
    p[0] = n(p[1], [p[4]], p[2])


def p_new_type_dec_winit(p):
    """
        new_type_dec    : new_type ID '{' new_type_params '}' declarators
    """
    p[0] = n(p[1], [p[4], p[6]])


def p_new_type_dec_wodef(p):
    """
        new_type_dec    : new_type ID declarators
    """
    p[0] = n(p[1], [p[3]])


def p_new_type(p):
    """
        new_type    : STRUCT
                    | CLASS
    """
    p[0] = p[1]


def p_new_type_params(p):
    """
        new_type_params : new_type_param new_type_params
    """
    p[0] = n("params", [p[1]] + p[2].children)


def p_new_type_params_end(p):
    """
        new_type_params : new_type_param
    """
    p[0] = n("params", [p[1]])


def p_new_type_param(p):
    """
        new_type_param : type declarators ';'
    """
    p[0] = n("param", [p[2]], p[1])

# ------------------ new types end -------------------


def p_function_definition(p):
    """
        func_def : type ID '(' params ')' '{' statements '}'
    """
    p[0] = n("func_def", [p[7]], (p[1], p[2], p[3]))


def p_function_defintion_noparam(p):
    """
        func_def : type ID '(' ')' '{' statements '}'
    """
    p[0] = n("func_def", [p[6]], (p[1], p[2]))


def p_function_defintion_nostatement(p):
    """
        func_def : type ID '(' params ')' '{' '}'
    """
    p[0] = n("func_def", [], (p[1], p[2], p[4]))


def p_function_definition_nothing(p):
    """
        func_def : type ID '(' ')' '{' '}'
    """
    p[0] = n("func_def", [], (p[1], p[2]))


def p_params(p):
    """
        params : param ',' params
    """
    p[0] = n("params", [p[1]] + p[3].children)


def p_params_end(p):
    """
        params : param
    """
    p[0] = n("params", [p[1]])


def p_param(p):
    """
        param : type declarator_2
    """
    p[0] = n("param", [p[2]], p[1])

# =================== statement start ======================


def p_statements(p):
    """
        statements : statement statements
    """
    if (p[1] != None):
        p[0] = n("statements", [p[1]] + p[2].children)
    else:
        p[0] = n("statements", p[2].children)


def p_statements_end(p):
    """
        statements : statement
    """
    p[0] = n("statements", [p[1]])


def p_statement(p):
    """
        statement   : expression ';'
                    | decl ';'
                    | block
                    | conditional
                    | iteration
                    | jump ';'
    """
    p[0] = p[1]


def p_statement_extra_semicolon(p):
    """
        statement : ';'
    """
    pass

# ================== conditional statement ==================


def p_conditional(p):
    """
        conditional : IF '(' expression ')' statement %prec THEN
    """
    p[0] = n("conditional", [p[3], p[5]])


def p_conditional_else(p):
    """
        conditional : IF '(' expression ')' statement ELSE statement
    """
    p[0] = n("conditional", [p[3], p[5], p[7]], "else")


# -------------------- conditional end -------------------


def p_block(p):
    """
        block : '{' stats_or_null '}'
    """
    p[0] = n("block", p[2])


def p_statement_or_null(p):
    """
        stats_or_null   : statements
                        | empty
    """
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1]

# ===================== iteration =========================


def p_iteration(p):
    """
        iteration : WHILE '(' expression ')' statement
    """
    p[0] = n("while", [p[3], p[5]])


def p_iteration_do_while(p):
    """
        iteration : DO statement WHILE '(' expression ')' ';'
    """
    p[0] = n("dowhile", [p[2], p[5]])


def p_iteration_for(p):
    """
        iteration : FOR '(' expr_or_null_or_init ';' expr_or_null ';' expr_or_null ')' statement
    """
    p[0] = n("for", [p[3], p[5], p[7], p[9]])


def p_expr_or_null(p):
    """
        expr_or_null    : expressions
                        | empty
    """
    if p[1] == None:
        p[0] = []
    else:
        p[0] = p[1]


def p_expr_or_null_or_init(p):
    """
        expr_or_null_or_init    : expr_or_null
                                | usual_dec
    """
    p[0] = p[1]


def p_jump(p):
    """
        jump    : BREAK
                | CONTINUE
                | RETURN
    """
    p[0] = n(p[1])


def p_jump_wvalue(p):
    """
        jump : RETURN expression
    """
    p[0] = n(p[1], [p[2]])

# -------------------- statement end ------------------------


# ===================== expression =========================

def p_expressions(p):
    """
        expressions : expression ',' expressions
    """
    p[0] = n("expressions", [p[1]] + p[3].children)


def p_expressions_end(p):
    """
        expressions : expression
    """
    p[0] = n("expressions", [p[1]])


def p_expression_to_ternary(p):
    """
        expression : tern_expr
    """
    p[0] = p[1]


def p_ternary_expr(p):
    """
        tern_expr  : tern_expr '?' tern_expr ':' tern_expr
    """
    p[0] = n("ternary_expr", [p[1], p[3], p[5]])


def p_ternary_expr_to_binary(p):
    """
        tern_expr : bin_expr
    """
    p[0] = p[1]


def p_binary_expr(p):
    """
        bin_expr        : bin_expr '+' bin_expr
                        | bin_expr '-' bin_expr
                        | bin_expr '*' bin_expr
                        | bin_expr '/' bin_expr
                        | bin_expr '^' bin_expr
                        | bin_expr '>' bin_expr
                        | bin_expr '<' bin_expr
                        | bin_expr LOGAND bin_expr
                        | bin_expr LOGOR bin_expr
                        | bin_expr LOGEQ bin_expr
                        | bin_expr LOGNEQ bin_expr
                        | bin_expr LEQ bin_expr
                        | bin_expr GEQ bin_expr
                        | bin_expr LSHIFT bin_expr
                        | bin_expr RSHIFT bin_expr
                        | bin_expr '=' bin_expr
                        | bin_expr ADDEQ bin_expr
                        | bin_expr SUBEQ bin_expr
                        | bin_expr MULTEQ bin_expr
                        | bin_expr DIVEQ bin_expr
                        | bin_expr MODEQ bin_expr
    """
    p[0] = n("binary_expression", [p[1], p[3]], p[2])


def p_binary_to_unary(p):
    """
        bin_expr    : pre_unary_expr
    """
    p[0] = p[1]


def p_pre_unary_expr(p):
    """
        pre_unary_expr  : PLUSPLUS pre_unary_expr %prec LPLUSPLUS
                        | MINUSMINUS pre_unary_expr %prec LMINUSMINUS
                        | '+' pre_unary_expr %prec LPOS
                        | '-' pre_unary_expr %prec LNEG
                        | '!' pre_unary_expr %prec LNOT
                        | '&' pre_unary_expr %prec LAT
    """
    p[0] = n("pre_unary", [p[2]], p[1])


def p_pre_unary_to_post(p):
    """
        pre_unary_expr : post_unary_expr
    """
    p[0] = p[1]


def p_post_unary_expr_array(p):
    """
        post_unary_expr : post_unary_expr '[' expression ']'
    """
    p[0] = n("post_unary", [p[1], p[3]], "array_access")


def p_post_unary_fncall_empty(p):
    """
        post_unary_expr : post_unary_expr '(' ')'
    """
    p[0] = n("post_unary", [p[1]], "fncall")


def p_post_unary_fncall(p):
    """
        post_unary_expr : post_unary_expr '(' expressions ')'
    """
    p[0] = n("post_unary", [p[1], p[3]], "fncall")


def p_post_unary_ppmm(p):
    """
        post_unary_expr : post_unary_expr PLUSPLUS %prec RPLUSPLUS
                        | post_unary_expr MINUSMINUS %prec RMINUSMINUS
    """
    p[0] = n("post_unary", [p[1]], p[2])


def p_post_unary_access_member(p):
    """
        post_unary_expr : post_unary_expr '.' ID
                        | post_unary_expr RARROW ID
    """
    p[0] = n("post_unary", [p[1], p[3]], p[2])


def p_post_unary_to_parenthesis(p):
    """
        post_unary_expr : element
    """
    p[0] = p[1]


def p_element(p):
    """
        element : ID
    """
    p[0] = n("var", [], p[1])


def p_element_const(p):
    """
        element : NUMBER
                | CHR
                | STR
    """
    p[0] = n("const", [], p[1])


def p_element_paren_expr(p):
    """
        element : '(' expression ')'
    """
    p[0] = p[2]

# ------------------- expression end -----------------------


def p_type(p):
    """
        type    : VOID
                | CHAR
                | SHORT
                | INT
                | LONG
                | FLOAT
                | DOUBLE
    """
    p[0] = p[1]


def p_empty(p):
    """
        empty :
    """
    pass

# Construye el parser global
parser = yacc.yacc()

def test_cpp_lexer(input_string):
    """Ejecuta el lexer sobre el string de entrada y recopila los valores de los tokens generados."""
    lexer.input(input_string)
    tokens = []
    for tok in lexer:
        tokens.append(tok.value)
    return tokens

def test_cpp_parser(input_string):
    """Parsea el string de entrada y retorna el resultado del análisis sintáctico como string."""
    result = parser.parse(input_string, lexer=lexer)
    return str(result)  # Asegúrate de que el resultado pueda ser convertido a string, o modifica según la necesidad

def print_cpp_ast(node, level=0):
    """Construye y retorna una representación en cadena del AST con sangría para mostrar la estructura."""
    result = ""
    indent = "  " * level
    
    if isinstance(node, n):  # Asegurándonos de que node es de la clase n
        result += f"{indent}+ {node.type}\n"  # Modificado para usar .type directamente
        for child in node.children:
            result += print_ast(child, level + 1)
    elif isinstance(node, list):
        for child in node:
            result += print_ast(child, level)
    else:
        result += f"{indent}- {node}\n"
    return result


def run_cpp_tests(input_string):
    """Ejecuta todas las pruebas: lexing, parsing y la impresión del AST, y retorna los resultados concatenados."""
    lexer_results = test_cpp_lexer(input_string)
    parser_result = test_cpp_parser(input_string)
    if parser_result:
        ast_representation = print_cpp_ast(parser_result)
        semantic = SemanticAnalyzer() 
        semantic.analyze(ast_representation) 
    else:
        ast_representation = "No valid AST generated or parser error."
    
    final_results = f"Lexer C++ Output:\n{lexer_results}\n\nAST Representation:\n{ast_representation}\n\nSemantic Analysis:\n{semantic.get_results()}"
    return final_results