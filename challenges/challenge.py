import re
import types


class Challenge:
    sample = 'sample'
    line_break = '\n'
    split_pattern = '\s+|\s?,\s?'
    edge_pattern = '^(\d+)->(\d+)(:(\d+))?$'

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

    # --------------------------------------------------
    # Default workflow
    # --------------------------------------------------

    def read(self):
        lines = self.sample.strip().splitlines()
        self.lines = [line.strip() for line in lines]

    def build(self):
        pass

    def calc(self):
        pass

    def format(self):
        self.output = str(self.result)

    # --------------------------------------------------
    # Accessing lines
    # --------------------------------------------------

    def line(self, number):
        return self.lines[number]

    def lines(self):
        return self.lines

    def line_to_integers(self, line_nr):
        return [int(i) for i in
                re.compile(self.split_pattern).split(self.line(line_nr))]

    def line_to_floats(self, line_nr):
        return [float(i) for i in
                re.compile(self.split_pattern).split(self.line(line_nr))]

    def line_to_edge(self, nr):
        return self._to_edge(re.compile(self.split_pattern).match(
            self.line(nr)))

    def read_edges(self, first=0, last=None):
        nr = first
        while True:
            try:
                line = self.line(nr)
            except IndexError:
                break
            match = re.compile(self.edge_pattern).match(line)
            if match:
                yield (self._to_edge(match))
                if nr == last:
                    break
                else:
                    nr += 1
            else:
                break

    @staticmethod
    def _to_edge(match):
        edge = types.SimpleNamespace()
        edge.tail = int(match.group(1))
        edge.head = int(match.group(2))
        if match.group(4):
            edge.weight = int(match.group(4))
        return edge

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    @staticmethod
    def format_list_of_integers(integers, joint=', '):
        return joint.join(str(x) for x in integers)

    def format_path(self, integers, backwards=False):
        if backwards:
            joint = '<-'
        else:
            joint = '->'
        return self.format_list_of_integers(integers, joint)
