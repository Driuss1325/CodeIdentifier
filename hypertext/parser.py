import ply.yacc as yacc
import json
from .lexer import tokens, lexer
# Parser rules
def p_html(p):
    '''html : elements'''
    p[0] = ('html', p[1])

def p_elements(p):
    '''elements : elements element
                | element'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_element(p):
    '''element : text
               | comment
               | conditional_comment
               | xml
               | cdata
               | dtd
               | script
               | style
               | tag'''
    p[0] = p[1]

def p_text(p):
    '''text : HTML_TEXT'''
    p[0] = ('text', p[1])

def p_comment(p):
    '''comment : HTML_COMMENT'''
    p[0] = ('comment', p[1])

def p_conditional_comment(p):
    '''conditional_comment : HTML_CONDITIONAL_COMMENT'''
    p[0] = ('conditional_comment', p[1])

def p_xml(p):
    '''xml : XML'''
    p[0] = ('xml', p[1])

def p_cdata(p):
    '''cdata : CDATA'''
    p[0] = ('cdata', p[1])

def p_dtd(p):
    '''dtd : DTD'''
    p[0] = ('dtd', p[1])

# Add a parser rule to handle SCRIPTLET tokens
def p_scriptlet(p):
    '''element : SCRIPTLET'''
    p[0] = ('scriptlet', p[1])  # Capture scriptlet content

# Add a parser rule to handle SEA_WS tokens
def p_sea_ws(p):
    '''element : SEA_WS'''
    p[0] = ('sea_ws', p[1]) # Capture SEA_WS content
    
def p_script(p):
    '''script : SCRIPT_OPEN script_body SCRIPT_CLOSE'''
    p[0] = ('script', p[2])

def p_script_body(p):
    '''script_body : SCRIPT_BODY'''
    p[0] = p[1]

def p_script_close(p):
    '''SCRIPT_CLOSE : TAG_OPEN TAG_SLASH TAG_NAME TAG_CLOSE'''
    p[0] = ('/script',)

def p_style(p):
    '''style : STYLE_OPEN style_body STYLE_CLOSE'''
    p[0] = ('style', p[2])

def p_style_body(p):
    '''style_body : STYLE_BODY'''
    p[0] = p[1]

def p_style_close(p):
    '''STYLE_CLOSE : TAG_OPEN TAG_SLASH TAG_NAME TAG_CLOSE'''
    p[0] = ('/style',)

def p_tag(p):
    '''tag : TAG_OPEN tag_name tag_attributes TAG_CLOSE
           | TAG_OPEN tag_name tag_attributes TAG_SLASH_CLOSE
           | TAG_OPEN TAG_SLASH tag_name TAG_CLOSE '''
    if len(p) == 5:  
        p[0] = ('tag', p[2], p[3])  
    else:
        p[0] = ('/', p[3])  

def p_tag_name(p):
    '''tag_name : TAG_NAME'''
    p[0] = p[1]

def p_tag_attributes(p):
    '''tag_attributes : tag_attributes tag_attribute
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_tag_attribute(p):
    '''tag_attribute : TAG_NAME TAG_EQUALS attribute_value'''
    p[0] = (p[1], p[3])

def p_attribute_value(p):
    '''attribute_value : ATTVALUE_VALUE'''
    p[0] = p[1]

# ... (lexer definitions remain the same)

# Parser Enhancements
def p_tag_close(p):
    '''tag_close : TAG_CLOSE
                 | TAG_SLASH_CLOSE'''
    if len(p) == 2:
        p[0] = ('/',)  # Indicate self-closing tag
    else:
        p[0] = ()      # Regular closing tag

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' in line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

def test_html_lexer(input_string):
    """Ejecuta el lexer sobre el string de entrada y recopila los valores de los tokens generados."""
    lexer.input(input_string)
    tokens = []
    for tok in lexer:
        tokens.append(tok.value)
    return tokens

def test_html_parser(input_data):
    """ Analiza el string de entrada HTML y retorna el resultado del análisis sintáctico como string. """
    result = parser.parse(input_data, lexer=lexer)
    return str(result)

def print_html_ast(node, level=0):
    """ Construye una representación en cadena del AST con sangría para mostrar la estructura. """
    result = ""
    indent = "  " * level
    if hasattr(node, 'type'):
        result += f"{indent}{node.type}\n"
        if hasattr(node, 'children'):
            for child in node.children:
                result += print_html_ast(child, level + 1)
    elif isinstance(node, list):
        for child in node:
            result += print_html_ast(child, level)
    else:
        result += f"{indent}- {node}\n"
    return result

def run_html_tests(input_data):
    """ Ejecuta todas las pruebas para HTML: lexing, parsing y la visualización del AST, y concatena los resultados en un solo string. """
    lexer_results = test_html_lexer(input_data)
    parser_result = test_html_parser(input_data)
    if parser_result:
        ast_representation = print_html_ast(parser_result)
    else:
        ast_representation = "No valid AST generated or parser error."
    
    final_results = f"Lexer HTML Output:\n{lexer_results}\n\nAST Representation:\n{ast_representation}"
    return final_results