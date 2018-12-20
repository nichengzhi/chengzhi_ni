#encoding=utf-8
#在Python中，如果一个对象的引用数为0，Python虚拟机就会回收这个对象的内存。
class ClassA():
    def __init__(self):
        print 'object born,id:%s'%str(hex(id(self)))
    def __del__(self):
        print 'object del,id:%s'%str(hex(id(self)))

def f1():
    while True:
        c1=ClassA()
        del c1

f1()
#c1 = classA()创建一个对象，放在0x35af348L内存中，c1指向这个内存，这个内存的引用计数加一。 删除后
#内存的引用计数减1.由于引用计数为0对象销毁
#引用计数减一也可以是c1被赋予其他变量，比如c1 = 25