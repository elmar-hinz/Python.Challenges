# https://github.com/elmar-hinz/Python.Challenges
from challenges import Challenge

class HelloGraphChallenge(Challenge):
    """
        Given: Two nodes and a list of edges denoting a path
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
        self.model = self.lines_to_graph(start=2)
        self.model.start = self.line_to_integer(0)
        self.model.stop = self.line_to_integer(1)

    def calc(self):
        tail = self.model.start
        self.result.path = [tail]
        self.result.weight = 0
        while tail != self.model.stop:
            # it's a path, just one way to go
            head = self.model.edges[tail][0]
            self.result.path.append(head)
            self.result.weight += self.model.weights[(tail, head)]
            tail = head

    def format(self):
        self.output = self.format_path(self.result.path)
        self.output += self.br
        self.output += str(self.result.weight)
