import gc
import time
#gc模块的一个主要功能就是解决循环引用的问题。
class ClassA(object):
    def __init__(self):
        print 'object born,id:%s'%str(hex(id(self)))
    def __del__(self):
        print 'object del,id:%s'%str(hex(id(self)))

def f3():
    # print gc.collect()
    c1=ClassA()
    c2=ClassA()
    c1.a=c2
    c2.a=c1
    del c1
    del c2
    print gc.garbage
    print gc.collect()
    print gc.garbage
    time.sleep(10)
if __name__ == '__main__':

    f3()