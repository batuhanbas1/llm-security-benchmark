import ast

def safe_calculate(expression):
    node = ast.parse(expression, mode='eval')
    return eval(compile(node, "<string>", "eval"), {"__builtins__": {}})