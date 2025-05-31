class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}  # Almacena las variables y sus tipos
        self.errors = []  # Lista para almacenar mensajes de error

    def analyze(self, node):
        """ Recorre el árbol de análisis sintáctico y verifica las reglas semánticas. """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, dict):
            children = node.get('children', [])
            for child in children:
                self.analyze(child)

    def visit_program(self, node):
        self.generic_visit(node)

    def visit_func_def(self, node):
        func_name = node.info[1]
        func_type = node.info[0]
        self.symbols[func_name] = func_type
        self.generic_visit(node)

    def visit_var(self, node):
        var_name = node.info
        if var_name in self.symbols:
            self.errors.append(f"Error: Variable '{var_name}' ya declarada.")
        else:
            self.symbols[var_name] = None  # Aquí podrías manejar el tipo si es necesario

    def visit_init(self, node):
        var_node = node.children[0]
        var_name = var_node.info
        # Verificar que la variable no ha sido declarada previamente
        if var_name in self.symbols:
            self.errors.append(f"Error: Variable '{var_name}' redeclarada.")
        else:
            self.symbols[var_name] = None  # Aquí manejar el tipo

    def visit_binary_expression(self, node):
        left_expr = node.children[0]
        right_expr = node.children[1]
        # Aquí podrías añadir verificaciones de tipo, como asegurar que ambos lados del operador son del mismo tipo, etc.
        self.analyze(left_expr)
        self.analyze(right_expr)

    def get_results(self):
        if not self.errors:
            return "Análisis Semántico completado sin errores."
        else:
            return "\n".join(self.errors)
