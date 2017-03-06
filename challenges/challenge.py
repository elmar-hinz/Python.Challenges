# python
# vim: set fileencoding=UTF-8 :

import re
import types

class Challenge:

    lineBreak = '\n'
    sample = 'sample'
    splitPattern = '\s+|\s?,\s?'
    edgePattern = '^(\d+)->(\d+)(:(\d+))?$'

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
        return  [int(i) for i in re.compile(self.splitPattern)
                .split(self.line(line_nr))]

    def lineToFloats(self, line_nr):
        return  [float(i) for i in re.compile(self.splitPattern)
                .split(self.line(line_nr))]

    def lineToEdge(self, nr):
        return self._toEdge(re.compile(self.edgePattern).match(self.line(nr)))

    def readEdges(self, first=0, last=None):
        nr = first
        while True:
            try:
                line = self.line(nr)
            except IndexError:
                break
            match = re.compile(self.edgePattern).match(line)
            if match:
                yield(self._toEdge(match))
                if nr == last:
                    break
                else:
                    nr = nr + 1
            else:
                break

    def _toEdge(self, match):
        edge = types.SimpleNamespace()
        edge.tail = int(match.group(1))
        edge.head = int(match.group(2))
        if match.group(4):
            edge.weight = int(match.group(4))
        return edge

    #--------------------------------------------------
    # Formatting
    #--------------------------------------------------

    def formatListOfIntegers(self, integers, joint=', '):
        return joint.join(str(x) for x in integers)

    def formatPath(self, integers, backwards=False):
        if backwards:
            joint = '<-'
        else:
            joint = '->'
        return self.formatListOfIntegers(integers, joint)

