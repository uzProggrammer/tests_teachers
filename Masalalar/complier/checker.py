import ast
a = input()
a=ast.literal_eval(a)
if 'a' not in a['code'] and a['out']:
    print(1)
else:
    print(0)