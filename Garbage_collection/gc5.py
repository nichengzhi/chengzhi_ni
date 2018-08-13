import gc

gc.set_debug(gc.DEBUG_STATS|gc.DEBUG_LEAK)
class A:
    def __del__(self):
        pass


class B:
    def __del__(self):
        pass


a = A()
b = B()
print a.__dict__
a.h = 123
print a.h
print a.__dict__
print hex(id(a))
print hex(id(a.__dict__))
a.b = b
b.a = a
del a
del b

print gc.collect()
print gc.garbage