# python
# vim: set fileencoding=UTF-8 :

import re
import types

class Challenge:

    sample = 'sample'
    splitter = '\s+|\s?,\s?'

    def __init__(self):
        self.lines = []
        self.model = types.SimpleNamespace()
        self.result = types.SimpleNamespace()
        self.output = ''

    def main(self):
        self.read()
        self.build()
        self.calc()
        self.format()

    #--------------------------------------------------
    # Default workflow
    #--------------------------------------------------

    def read(self):
        lines = self.sample.strip().splitlines()
        self.lines = [line.strip() for line in lines]

    def build(self):
        pass

    def calc(self):
        pass

    def format(self):
        self.output = str(self.result)

    #--------------------------------------------------
    # Accessing lines
    #--------------------------------------------------

    def line(self, number):
        return self.lines[number]

    def lines(self):
        return self.lines

    def lineToIntegers(self, line_nr):
        return  [int(i) for i in re.compile(self.splitter)
                .split(self.line(line_nr))]

    def lineToFloats(self, line_nr):
        return  [float(i) for i in re.compile(self.splitter)
                .split(self.line(line_nr))]

    #--------------------------------------------------
    # Packing
    #--------------------------------------------------

    def packIntegers(self):
        self.output = ', '.join(str(x) for x in self.result)

