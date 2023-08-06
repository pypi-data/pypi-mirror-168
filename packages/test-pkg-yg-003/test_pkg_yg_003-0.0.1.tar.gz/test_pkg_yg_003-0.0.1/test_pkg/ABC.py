# -*- coding:utf-8 -*-


class Abc:

    def __init__(self, a=1, b=2, c=3):
        if not str(a).isdigit():
            raise Exception('a must be number')
        if not str(b).isdigit():
            raise Exception('b must be number')
        if not str(c).isdigit():
            raise Exception('c must be number')
        self.A = a
        self.B = b
        self.C = c

    def sum(self):
        return self.A + self.B + self.C
