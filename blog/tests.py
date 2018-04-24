from django.test import TestCase

# Create your tests here.


class Person(object):
    def __init__(self, name):
        self.name = name

    # __str__方法的作用，指明具体是哪个对象，而不是内存地址
    def __str__(self):
        return self.name


# <__main__.Person object at 0x0000000002827518>
# charley
new_person = Person("charley")
print(new_person)
