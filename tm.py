from __future__ import annotations

from typing import Literal, Callable, Any


class declval[T]:
  def __new__(cls) -> T:
    return getattr(T, 'declval')

L = 'L'
R = 'R'
Dir = Literal['L', 'R']

class tape[A]:
  def __new__(cls, read: A, write: A, d: Dir) -> None:
    ...

a = (int, int)

def right[A : list]():
  for x in declval[A]():
    if tape(x, x, 'R'):
      return

def instantiate[**T, R](f: Callable[T, R], **kwargs: Any) -> Callable[T, R]:
  def g(*a, **kw):
    for t in f.__type_params__:
      val = kwargs.get(t.__name__)
      if val:
        setattr(t, 'declval', val)
    return f(*a, **kw)
  return g # type: ignore

def right[As : list]():
  if tape(As, As, R): pass
  elif ...: ...
  return

def shl[As : list, prev]():
  if None: pass
  elif ...(tape(As, prev, L)): shl[As]()

instantiate(right[[1]]())
