from .visit import *
from .node import *

class Interpreter(object):

    def __init__(self):
        self.variables = {}

    @on('node')
    def visit(self, node):
        pass

    @when(Module)
    def visit(self, node):
        return node.body.accept(self)

    @when(StatementList)
    def visit(self, node):
        result = []
        for statement in node.statement_list:
            result.append(statement.accept(self))
        return result

    @when(Print)
    def visit(self, node):
        value = node.value.accept(self)
        return value  # ahora también retornas el valor


    @when(While)
    def visit(self, node):
        if node.test.accept(self):
            while node.test.accept(self):
                node.body.accept(self)
        else:
            if node.orelse != []:
                return node.orelse.accept(self)
            else:
                pass

    @when(If)
    def visit(self, node):
        if node.test.accept(self):
            return node.body.accept(self)
        else:
            if node.orelse != []:
                return node.orelse.accept(self)
            else:
                pass

    @when(BoolOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return bool(eval("a " + node.op + " b", {"a": r1, "b": r2}))

    @when(Compare)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return bool(eval("a" + node.op + "b", {"a": r1, "b": r2}))

    @when(Assign)
    def visit(self, node):
        expr_accept = node.expression.accept(self)
        self.variables[node.id] = expr_accept
        return self.variables[node.id]

    @when(BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        r1Str = str(r1)
        r2Str = str(r2)
        pos1 = r1Str.find('.')
        pos2 = r2Str.find('.')

        if pos1 != -1 or pos2 != -1:
            return float(eval("a" + node.op + "b", {"a": r1, "b": r2}))
        else:
            return int(eval("a" + node.op + "b", {"a": r1, "b": r2}))

    @when(List)
    def visit(self, node):
        return list(node.values.accept(self))

    @when(Tuple)
    def visit(self, node):
        return tuple(node.values.accept(self))

    @when(ExprList)
    def visit(self, node):
        result = []
        for expr in node.expression_list:
            result.append(expr.accept(self))
        return result

    @when(Name)
    def visit(self, node):
        return self.variables[node.id]

    @when(Const)
    def visit(self, node):
        return node.value

    @when(Number)
    def visit(self, node):
        numStr = str(node.value)
        pos = numStr.find('.')

        if pos != -1:
            return float(node.value)
        else:
            return int(node.value)

    @when(Str)
    def visit(self, node):
        return node.value
