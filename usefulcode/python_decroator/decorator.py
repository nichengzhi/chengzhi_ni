#! /usr/bin/env python
# encoding: utf-8

# decorator: add more function for original function

import logging

def use_logging(func):
    logging.warn("%s is running" % func.__name__)
    func()

def foo():
    print('i am foo')

use_logging(foo)

#a simple decorator
def use_logging(func):

    def wrapper():
        logging.warn("%s is running" % func.__name__)
        return func()#this will run the func()
    return wrapper
foo2 = use_logging(foo)#use user_logging function to decroate foo function
foo2()
#use @
@use_logging#more eleagent same as use_logging(foo)
def foo3():
    print("i am foo")

foo3()
#if foo function need parameter

def use_logging4(func):
    def wrapper(*args, **kwargs):
        logging.warn("%s is running" % func.__name__)
        return func(*args, **kwargs)
    return wrapper
@use_logging4
def foo4(name, age = None, height = None):
    print("I am %s, age %s, height %s" % (name, age, height))

foo4("nige",18,188)
#if decorator need parameter
def use_logging5(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            """wrap func: call_it"""
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator
@use_logging5("warn")
def foo5(name, age = None, height = None):
    """foo function"""
    print("I am %s, age %s, height %s" % (name, age, height))
foo5("nige",18,188)
## class decorator, use call method
class Foodec(object):
    def __init__(self, func):
        self._func = func
    def __call__(self, *args, **kwargs):
        print('class decorator running')
        print("%s is running" % self._func.__name__)
        self._func(*args, **kwargs)
        print('class decorator ending')
@Foodec
def foo6(name, age = None, height = None):
    print("I am %s, age %s, height %s" % (name, age, height))
foo6("nige",18,188)
#multiple decorator
"""
@a
@b
@c
def f ():
    pass

equals : f = a(b(c(f)))

"""
#the function after decorator, the metadata for original function is changed
print foo5.__name__#return wrapper which is the decorator function name
print foo5.__doc__
#add wraps to eleminate this effect
from functools import wraps
def use_logging6(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """wrap func: call_it"""
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator
@use_logging6("warn")
def foo7(name, age = None, height = None):
    """foo function"""
    print("I am %s, age %s, height %s" % (name, age, height))
print foo7.__name__
print foo7.__doc__
#also you can use update warpper
from functools import update_wrapper
def use_logging7(level):
    def decorator(func):
        
        def wrapper(*args, **kwargs):
            """wrap func: call_it"""#this will add function doc information
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args, **kwargs)
        return update_wrapper(wrapper,func)
    return decorator
@use_logging7("warn")
def foo8(name, age = None, height = None):
    """foo function"""
    print("I am %s, age %s, height %s" % (name, age, height))
print foo8.__name__
print foo8.__doc__