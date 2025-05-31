def analyze(tree, names):
    if tree[0] == 'program':
        for statement in tree[1]:
            analyze(statement, names)
    elif tree[0] == 'var_declaration':
        name = tree[1]
        value = analyze(tree[2], names)
        names[name] = value
    elif tree[0] == 'function_declaration':
        pass
    elif tree[0] == 'return_statement':
        return analyze(tree[1], names)
    elif tree[0] == 'expression_statement':
        analyze(tree[1], names)
    elif tree[0] == 'binop':
        left = analyze(tree[2], names)
        right = analyze(tree[3], names)
        if tree[1] == '+':
            return left + right
        elif tree[1] == '-':
            return left - right
        elif tree[1] == '*':
            return left * right
        elif tree[1] == '/':
            return left / right
    elif tree[0] == 'number':
        return tree[1]
    elif tree[0] == 'id':
        return names.get(tree[1], 0)
