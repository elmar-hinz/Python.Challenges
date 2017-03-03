# python
# vim: set fileencoding=UTF-8 :

class Challenge:

    sample = 'sample'

    def __init__(self):
        self.lines = []
        self.model = []
        self.result = []
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
        self.lines = self.sample.splitlines()

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
        return  [int(i) for i in self.line(line_nr).split(',')]

    def lineToFloats(self, line_nr):
        return  [float(i) for i in self.line(line_nr).split(',')]

    #--------------------------------------------------
    # Packing
    #--------------------------------------------------

    def packIntegers(self):
        self.output = ', '.join(str(x) for x in self.result)

