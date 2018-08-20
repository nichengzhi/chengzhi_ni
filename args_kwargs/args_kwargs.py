def test_kwargs(first, *args, **kwargs):
   print('Required argument: ', first)
   for v in args:
      print('Optional argument (*args): ', v)
   for k, v in kwargs.items():
      print('Optional argument %s (*kwargs): %s' % (k, v))

test_kwargs(1,*[1,2,2],**{'a':5,'b':6})