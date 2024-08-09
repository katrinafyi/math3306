from ast import *
from typing import Any
import builtins
from copy import deepcopy
import typing
import ast
import sys
import string

def safe(s):
  o = ''
  for c in s:
    if c in string.ascii_letters or c in string.digits or c == '_':
      o += c
    else:
      o += f'x{ord(c):02x}'
  return o

class Subst(ast.NodeTransformer):
  def __init__(self, name: str, val: Any):
    self.name = name
    self.val = val

  def visit_Name(self, node):
    match node:
      case Name(x, Load()) if x == self.name:
        return Constant(self.val) 
    return node

  def visit(self, node):
    # print(node, list(ast.iter_fields(node)))
    return super().visit(node)

class Inst(ast.NodeTransformer):
  def __init__(self, base: ast.FunctionDef):
    self.base = base

  def go(self, name, targs):
    self.targs = targs
    self.name = name
    self.base.name += safe(f'_{name}{''.join(map(str, targs))}')
    self.base.type_params = \
      [t for t in self.base.type_params if t.name != name]
    return self.visit(self.base)


  def visit_If(self, node):
    # print(ast.dump(node, indent=2))
    match node:
      case If(test, body, [
        If(Constant(builtins.Ellipsis),
        [Expr(Constant(builtins.Ellipsis))],
        rest)
      ]):
        result = rest
        for x in reversed(self.targs):
          def subst(y):
            return Subst(self.name, x).visit(deepcopy(self.visit(y)))

          result: list[stmt] = \
            [If(subst(test), list(map(subst, body)), result)]

        return result[0] if len(result) == 1 else If(Constant(True), result, [])
    return self.generic_visit(node)


# class Trans(ast.NodeTransformer):
#   def __init__(self, mod: ast.Module):
#     self.mod = mod
#   def visit_Call(self, node):
#     print(ast.dump(node))
#     match node:
#       case Call(Name('instantiate', Load()), [Subscript(
#         Name('right', Load()),
#         targs
#       )]): print(targs)

def go(text):
  a = ast.parse(text)
  print(a)
  # print(ast.dump(a, indent=2))
  # Trans(a).visit(a)
  f = [x for x in a.body if isinstance(x, FunctionDef) and x.name == 'right']
  assert f
  print(ast.unparse(Inst(f[0]).go('As', [1,2, '#', '\n'])))

if __name__ == '__main__':
  go(open(sys.argv[1]).read())



