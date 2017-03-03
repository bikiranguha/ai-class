class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

print MyClass.i

x = MyClass()
print x.i,x.f()