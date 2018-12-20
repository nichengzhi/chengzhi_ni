class ClassA():
    def __init__(self):
        print 'object born,id:%s'%str(hex(id(self)))
    def __del__(self):
        print 'object del,id:%s'%str(hex(id(self)))

def f2():
    while True:
        c1=ClassA()
        c2=ClassA()
        c1.t=c2
        c2.t=c1
        del c1
        del c2
'''创建了c1，c2后，0x237cf30（c1对应的内存，记为内存1）,0x237cf58（c2对应的内存，记为内存2）这两块内存的引用计数都是1，
执行c1.t=c2和c2.t=c1后，这两块内存的引用计数变成2.
在del c1后，内存1的对象的引用计数变为1，由于不是为0，所以内存1的对象不会被销毁，所以内存2的对象的引用数依然是2，
在del c2后，同理，内存1的对象，内存2的对象的引用数都是1。
虽然它们两个的对象都是可以被销毁的，但是由于循环引用，导致垃圾回收器都不会回收它们，所以就会导致内存泄露。'''
#f2()