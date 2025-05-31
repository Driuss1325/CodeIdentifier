from symtab import *
listaf = []
pilavalores = []

def generate(file, top):
    emit_program(file, top)
    anexo_get_expr(top)

def get_tipo(top, tipo):
    funciones = top.children
    global listaf
    for f in funciones:
        if f.name == tipo:
            listaf.append(f)
        get_tipo(f, tipo)

def anexo_get_tipo(rea, tipo):
    global listaf
    listaf = []
    get_tipo(rea, tipo)
    return listaf

def anexo_get_expr(top):
    global listaf
    expr = "numero id + - * / < > <= >= = != and or".split()
    listaf = []
    for i in expr:
        get_tipo(top, i)
    return listaf

def eval_expressions(out, lista):
    for s in lista:
        eval_expression(out, s)

def eval_expression(out, expr):
    if expr.name == 'numero':
        print(f"! push {expr.value}", file=out)
    elif expr.name == 'id':
        print(f"! push {expr.value}", file=out)
    elif expr.name == '+':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! add", file=out)
    elif expr.name == '-':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! sub", file=out)
    elif expr.name == '*':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! multiplicacion", file=out)
    elif expr.name == '/':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! division", file=out)
    elif expr.name == '<':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! mayor", file=out)
    elif expr.name == '>':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! menor", file=out)
    elif expr.name == '<=':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! mayor_igual", file=out)
    elif expr.name == '>=':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! menor_igual", file=out)
    elif expr.name == '=':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! igual", file=out)
    elif expr.name == '!=':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! no_igual", file=out)
    elif expr.name == 'or':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! or", file=out)
    elif expr.name == 'and':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out, left)
        eval_expression(out, right)
        print("! and", file=out)

#------------------- EMITS ----------------------------

def emit_program(out, top):
    print("\n! program", file=out)
    funclist = anexo_get_tipo(top, "funcion")
    for f in funclist:
        emit_function(out, f)

def emit_function(out, func):
    print(f"\n! function: {func.leaf} (start)", file=out)
    emit_statementsinter(out, func)
    print(f"! function: {func.leaf} (end)", file=out)

def emit_statementsinter(out, statements):
    statements = anexo_get_tipo(statements, "lineas")
    if len(statements) > 0:
        statements = statements[0].children
        emit_statements(out, statements)

def emit_statements(out, statements):
    for s in statements:
        emit_statement(out, s)

def emit_statement(out, s):
    if s.name == 'print':
        emit_print(out, s)
    elif s.name == 'read':
        emit_read(out, s)
    elif s.name == 'write':
        emit_write(out, s)
    elif s.name == 'while':
        emit_while(out, s)
    elif s.name == 'skip':
        emit_skip(out, s)
    elif s.name == 'break':
        emit_break(out, s)
    elif s.name == 'if':
        emit_if(out, s)
    elif s.name == 'return':
        emit_return(out, s)
    elif s.name == ':=':
        emit_asig(out, s)
    elif s.name == 'else':
        emit_else(out, s)
    else:
        pass

def emit_print(out, s):
    print("\n! print (start)", file=out)
    print("! print (end)", file=out)

def emit_read(out, s):
    print("\n! read (start)", file=out)
    print("! read (end)", file=out)

def emit_write(out, s):
    print("\n! write (start)", file=out)
    expr = anexo_get_expr(s)
    eval_expressions(out, expr)
    print("! expr := pop", file=out)
    print("! write(expr)", file=out)
    print("! write (end)", file=out)

def emit_while(out, s):
    print("\n! while (start)", file=out)
    expr = anexo_get_expr(s)
    eval_expressions(out, expr)
    emit_statementsinter(out, s)
    print("! while (end)", file=out)

def emit_skip(out, s):
    print("\n! skip (start)", file=out)
    print("! skip (end)", file=out)

def emit_break(out, s):
    print("\n! break (start)", file=out)
    print("! break (end)", file=out)

def emit_if(out, s):
    print("\n! if (start)", file=out)
    expr = anexo_get_expr(s)
    eval_expressions(out, expr)
    emit_statements(out, s.children)
    print("! if (end)", file=out)

def emit_return(out, s):
    print("\n! return (start)", file=out)
    expr = anexo_get_expr(s)
    eval_expressions(out, expr)
    print("! return (end)", file=out)

def emit_asig(out, s):
    print("\n! asig (start)", file=out)
    expr = anexo_get_expr(s)
    eval_expressions(out, expr)
    print("! expr := pop", file=out)
    print("! asig (end)", file=out)

def emit_else(out, s):
    print("\n! else (start)", file=out)
    if len(s.children) > 0:
        expr = anexo_get_expr(s)
        eval_expressions(out, expr)
        emit_statements(out, s.children)
    print("! else (end)", file=out)
