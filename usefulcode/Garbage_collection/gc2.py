import sys
class ClassA():
    def __init__(self):
        print 'object born,id:%s'%str(hex(id(self)))
    def __del__(self):
        print 'object del,id:%s'%str(hex(id(self)))

def f1():
    while True:
        c1=ClassA()
        del c1


def func(c):
    print 'in func function', sys.getrefcount(c) - 1

#The count returned is generally one higher than you might expect,
# because it includes the (temporary) reference as an argument to  getrefcount().
#可以查看a对象的引用计数，但是比正常计数大1，因为调用函数的时候传入a，这会让a的引用计数+1
print 'init', sys.getrefcount(11) - 1
a = 11
print 'after a=11', sys.getrefcount(11) - 1
b = a
print 'after b=a', sys.getrefcount(11) - 1
func(11)
print 'after func(a)', sys.getrefcount(11) - 1
list1 = [a, 12, 14]
print 'after list1=[a,12,14]', sys.getrefcount(11) - 1
a = 12
print 'after a=12', sys.getrefcount(11) - 1
del a
print 'after del a', sys.getrefcount(11) - 1
del b
print 'after del b', sys.getrefcount(11) - 1
# list1.pop(0)
# print 'after pop list1',sys.getrefcount(11)-1
del list1
print 'after del list1', sys.getrefcount(11) - 1