from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .tree_printer import TreePrinter
import ply.yacc as yacc


def test_python_lexer():
    lexer = Lexer()
    tokens = lexer.tokens
    return tokens

def run_python_tests(code):
    # Crear instancias del lexer y parser
    lexer = Lexer()
    parser = yacc.yacc(module=Parser)

    # Lista para guardar los resultados
    results = []

    # Parsear el código y obtener el AST
    ast = parser.parse(code, lexer=lexer)
    results.append('===== LEXER OUTPUT =====\n')
    results.append('\n'.join(lexer.tokens)+'\n')
    results.append('===== AST =====\n')
    results.append(str(ast))

    # Ejecutar el programa analizado
    if ast is not None:
        results.append('\n===== PROGRAM EXECUTION =====\n')
        output = ast.accept(Interpreter())
        results.append(str(output))
    else:
        results.append('\nNo valid AST generated.\n')

    # Unir los resultados en una sola cadena y devolverla
    return '\n'.join(results)
