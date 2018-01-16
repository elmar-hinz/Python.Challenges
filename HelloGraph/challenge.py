# https://github.com/elmar-hinz/Python.Challenges
from challenges import Challenge

class HelloGraphChallenge(Challenge):
    """
        Given: Two nodes and a list of edges
        Return: Graph between the nodes and it's weight
    """

    sample = '''
        2
        4
        1->2:2
        2->3:4
        3->4:10
        4->5:8
        5->6:1
    '''

    expect = '''
        2->3->4
        14
    '''

    def build(self):
        self.model.start = self.line_to_integer(0)
        self.model.stop = self.line_to_integer(1)
        self.model.graph = dict()
        for edge in self.edges(2):
            self.model.graph[edge.tail] = (edge.head, edge.weight)

    def calc(self):
        head = None
        tail = self.model.start
        self.result.graph = [tail]
        self.result.weight = 0
        while tail != self.model.stop:
            self.result.weight += self.model.graph[tail][1]
            tail = self.model.graph[tail][0]
            self.result.graph.append(tail)

    def format(self):
        self.output = self.format_path(self.result.graph)
        self.output += self.br
        self.output += str(self.result.weight)
