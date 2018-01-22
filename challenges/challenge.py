"""Core module of challenges

This module holds the base class of all challenges.
"""

import re
import math
import types
from collections import defaultdict


class Challenge:
    """Base class of all challenges

    Design concept is the Template Method Design Pattern (GOF).

    Attributes:

    :sample:    The input of the challenge.
    :output:    The output of the challenge

    Workflow:

    The `main` method controls the overall workflow by calling the worker
    methods. This is the common character of all challenges.
    The base class controls the workflow of the derived workers.

    Workers:

    The worker methods need to be implemented by the inheriting class.

    :read:     Read the input into a list of lines.
    :build:    Build the data model from the lines.
    :calc:     Run the main algorithm of the challenge.
    :format:   Create the output string required by the grader.

    Library:

    The other methods support the implementation of the workers. They address
    the extraction of data from the input lines or the formatting of the
    output.

    Sample:

    The attribute `sample` is both used as class and as instance attribute.
    When the instance attribute is injected it shadows the class attribute. By
    this the class attribute sets a tiny but useful default.

    When the challenge runner is executed with the option `--klass` no
    instance variable is injected and the sample from the class is used::

        prompt> challenge MyChallenge --klass

    When the runner is executed with the option `--file` the files content is
    injected::

        prompt> challenge MyChallenge --file ~/Downloads/data.txt

    """

    sample = '''
        sample
        sample
    '''
    """Holds a minimal example of the input with additional whitespace.

    This class variable should always be preset with a tiny sample of input.
    Whitespace surrounding lines is for readability. It typically needs to be 
    stripped to get the actual sample.
    """

    expect = '''
        expected result
        expected result
    '''
    """Holds the expected result with additional leading whitespace.
    
    Whitespace surrounding lines is for readability. It typically needs to be 
    stripped to get the actual expactation.
    """

    br = '\n'
    """Line breaks as expected by the most graders."""

    split_pattern = '\s+|\s?,\s?'
    """Reg expression to split input lines.

    Used by some of the input parsing functions. The default splits by
    whitespace and/or comma. If the input is separated differently like colons
    or semicolons it needs adjustment in the inheriting class.
    """

    edge_pattern = '^(\d+)->(\d+)(:(\d+))?$'
    """Reg expression to extract edges of a graph.
    
    With or without weight.
    
        2->3
        2->3:22

    A default setting used by methods that extract edges from input lines.
    May need adjustment for different kind of edge input formats.
    """

    multi_edge_pattern = '^(\d+)->(\d+(,?\s*\d+)*)$'
    """Reg expressen to extrct edges of a graph. 
    
    Multiple edges on one line.
    
        2->3, 4, 5
    
    A default setting used by methods that extract edges from input lines.
    May need adjustment for different kind of edge input formats.
    """

    fasta_pattern = '^[\-\*A-Z]+$'
    """Reg expression for FASTA sequences.

    Matches lines holding FASTA sequences.
    """

    def __init__(self):
        self.lines = []
        """A list of lines that will be filled by the method read()."""

        self.model = types.SimpleNamespace()
        """The imported data model.

        A flexible namespace object to take up any kind of data. In simple
        cases this may be completely overwritten, i.e by a list or dict.
        """
        self.result = types.SimpleNamespace()
        """The resulting data model.

        A flexible namespace object to take up any kind of data. In simple
        cases this may be completely overwritten, i.e by a list or dict.
        """

        self.output = ''
        """The output string.

        The string representation of the resulting model as expected by the
        grader.
        """

    def main(self):
        """Control the workflow of the challenge.

        Usually this method doesn't need to be overwritten.

        The workers share data via instance variables.
        The overall input is injected into self.sample.
        The overall output is read from self.result.
        """
        self.read()
        self.build()
        self.calc()
        self.format()

    # --------------------------------------------------
    # Default and abstract workers
    # --------------------------------------------------

    def read(self):
        """Extract the input string self.sample into self.lines.

        Typically this method can be used as is.
        """
        self.lines = self.example().splitlines()

    def build(self):
        """Set up the model from the input lines.

        This method must be implemented.
        Reads from self.lines.
        Fills self.model.
        """
        pass

    def calc(self):
        """Main algorithm of the challenge.

        This method must be implemented. Here the interesting stuff happens.
        Best practice is to delegate to functions, that are named by the
        algorithms used or even to other classes that implement the algorithm.

        Reads from self.model.
        Fills self.result.
        """
        pass

    def format(self):
        """Format the output string.

        In simple cases this method can be used as is. In other cases it
        needs to be reimplemented.

        Reads from self.result.
        Fills self.output.
        """
        self.output = str(self.result)

    # --------------------------------------------------
    # Accessing example and expectation
    # --------------------------------------------------

    def example(self):
        """Get the sample, with heading whitespace trimmed"""
        lines = self.sample.strip().splitlines()
        return '\n'.join(line.strip() for line in lines)

    def expectation(self):
        """Get the expecation, with heading whitespace trimmed"""
        lines = self.expect.strip().splitlines()
        return '\n'.join(line.strip() for line in lines)

    # --------------------------------------------------
    # Accessing input lines
    # --------------------------------------------------

    def line(self, nr: int):
        """ Return one line by the given number.

        :param nr: line number
        :return: line as string
        """
        return self.lines[nr]

    def lines_to_list(self, start: int = 0, stop: int = None):
        """Return a list of lines.

        If stop is not given all remaining lines are used.

        :param start: index of first line
        :param stop: index of line after last line
        :return: list of lines
        """
        if stop:
            return self.lines[start:stop]
        else:
            return self.lines[start:]

    def _to_words(self, line: str):
        """ Split line into words

        The split behaviour can be adjusted by changing self.split_pattern.

        :param line: the string to split
        :return: list of words
        """
        return list(re.compile(self.split_pattern).split(line))

    def line_to_words(self, nr: int):
        """ Split one line into a list of words.

        :param nr: line number
        :return: list of words
        :see: self._to_words()
        """
        return self._to_words(self.line(nr))

    def lines_to_words(self, start: int = 0, stop: int = None,
                       flatten: bool = False):
        """Split a range of lines into words.

        If stop is not given all remaining lines are used.

        :param start: index of first line
        :param stop: index of line after last line
        :param flatten: flatten to one dimensional list
        :return: one or two dimensional list of words
        :see: self._to_words()
        """
        words = []
        for line in self.lines_to_list(start, stop):
            if flatten:
                words += self._to_words(line)
            else:
                words.append(self._to_words(line))
        return words

    def _to_integers(self, line:str):
        """ Split line into integers

        The split behaviour can be adjusted by changing self.split_pattern.

        :param line: the string to split
        :return: list of integers
        """
        return [int(i) for i in re.compile(self.split_pattern).split(line)]

    def line_to_integer(self, nr: int):
        """ Return line as integer.

        :param nr: line number
        :return: integer
        """
        return int(self.line(nr))

    def line_to_integers(self, nr: int):
        """ Split one line into  a list of integers.

        :param nr: line number
        :return: list of integers
        :see: self._to_integers
        """
        return self._to_integers(self.line(nr))

    def lines_to_integers(self, start:int=0, stop=None, flatten=False):
        """Split a range of lines into integers

        If stop is not given all remaining lines are used.

        :param start: index of first line
        :param stop: index of line after last line
        :param flatten: flatten to one dimensional list
        :return: one or two dimensional list of integers
        :see: self._to_integers()
        """
        integers = []
        for line in self.lines_to_list(start, stop):
            if flatten:
                integers += self._to_integers(line)
            else:
                integers.append(self._to_integers(line))
        return integers

    def _to_floats(self, line:str):
        """ Split line into floats

        The split behaviour can be adjusted by changing self.split_pattern.

        :param line: the string to split
        :return: list of floats
        """
        return [float(f) for f in re.compile(self.split_pattern).split(line)]

    def line_to_float(self, nr: int):
        """ Return line as float.

        :param nr: line number
        :return: float
        """
        return float(self.line(nr))

    def line_to_floats(self, nr: int):
        """ Split one line into  a list of floats.

        :param nr: line number
        :return: list of floats
        :see: self._to_floats
        """
        return self._to_floats(self.line(nr))

    def lines_to_floats(self, start:int=0, stop=None, flatten=False):
        """Split a range of lines into floats

        If stop is not given all remaining lines are used.

        :param start: index of first line
        :param stop: index of line after last line
        :param flatten: flatten to one dimensional list
        :return: one or two dimensional list of floats
        :see: self._to_floats()
        """
        floats = []
        for line in self.lines_to_list(start, stop):
            if flatten:
                floats += self._to_floats(line)
            else:
                floats.append(self._to_floats(line))
        return floats

    def line_to_permutation(self, nr: int, terminals: bool = False):
        """Convert one line to a permutation

        optionally surrounded by terminals

        Example: (+1 -3, -2)
        Result: (1, -3, 2)
        If terminals is True: (0, 1, -3, 2, 4)

        The number of the line is selected by nr.
        Input may be surrounded by a pair of round parenthesis.

        :param nr: line number
        :param terminals: if True surrounded by 0 and n + 1
        :return: permutation
        """
        line = self.line(nr)
        match = re.compile('^\((.*)\)$').match(line)
        if match:
            digits = match.group(1)
        else:
            digits = line
        perm = [int(d) for d in re.compile(self.split_pattern).split(digits)]
        if terminals:
            perm = [0] + perm + [len(perm) + 1]
        return tuple(perm)

    def line_to_permutations(self, nr: int):
        """Convert one line to multiple permutations

        Example: (+1 -3, -2)(+4 +5)
        Result: [(1, -3, 2), (4, 5)]

        The number of the line is selected by line_nr.

        :param nr: line number
        :return: list of permutations (tuples)
        """
        matches = re.findall('\(([^)]*)\)', self.line(nr))
        result = []
        for digits in matches:
            result.append(tuple(int(d) for d in re.compile(
                self.split_pattern).split(digits)))
        return result

    # noinspection PyMethodMayBeStatic
    def _to_edges(self, line:str):
        """Convert input string to edges.

        Detects if the line in single edge or multi edge format.

        Single edge formats:

            tail->head
            tail->head:weight

        Multi edge formats:

            tail->head, head, head

        Edge is of type namespace:

            edge.tail
            edge.head
            edge.weight if given

        :param line: input string
        :return: list of edge
        """
        edges = []
        match = re.compile(self.edge_pattern).match(line)
        if match:
            edge = types.SimpleNamespace()
            edge.tail = int(match.group(1))
            edge.head = int(match.group(2))
            if match.group(4):
                edge.weight = int(match.group(4))
            edges.append(edge)
        else:
            match = re.compile(self.multi_edge_pattern).match(line)
            if match:
                tail = int(match.group(1))
                rest = match.group(2)
                heads = [int(i) for i in
                         re.compile(self.split_pattern).split(rest)]
                for head in heads:
                    edge = types.SimpleNamespace()
                    edge.tail = tail
                    edge.head = head
                    edges.append(edge)
        return edges

    def line_to_edge(self, nr: int):
        """Convert one line to an edge.

        :param nr: line number
        :return: edge (namespace: tail, head, weight)
        :see: self._to_edges
        """
        return self._to_edges(self.line(nr))[0]

    def line_to_edges(self, nr: int):
        """Convert one line to multiple edges.

        1->2,3,4

        :param nr: line number
        :return: edge (namespace: tail, head, weight)
        :see: self._to_edges
        """
        return self._to_edges(self.line(nr))

    def lines_to_edges(self, start: int = 0, stop: int = None):
        """Retrun a list of edges for range of lines.

        1->2       # simple edge
        1->2:22    # weighted edge
        1->2,3,4   # muliple edges per line

        If stop is not given all remaining lines are used.

        :param start:
        :param stop:
        :return: list of edges (namespace: tail, head, weight)
        :see: self._to_edges
        """
        edges = []
        for line in self.lines_to_list(start, stop):
                edges += self._to_edges(line)
        return edges

    def lines_to_graph(self, start: int = 0, stop: int = None):
        """Retrun a graph for range of lines

        If stop is not given all remaining lines are usee.

        Formats:

            1->2       # simple edge
            1->2:22    # weighted edge
            1->2,3,4   # muliple edges per line

        Properties:

            graph.edges:
                dict, tails as keys and list of heads as values

            graph.weights:
                dict, pairs of tail, head as keys and weight as value

        :param start:
        :param stop:
        :return: graph, namespace with graphs properties
        :see: self._to_edges
        """
        graph = types.SimpleNamespace()
        graph.edges = defaultdict(list)
        graph.weights = dict()
        edges = []
        nodes = []
        for line in self.lines_to_list(start, stop):
            edges += self._to_edges(line)
        for edge in edges:
            nodes.append(edge.head)
            nodes.append(edge.tail)
            graph.edges[edge.tail].append(edge.head)
            try:
                graph.weights[(edge.tail, edge.head)] = edge.weight
            except AttributeError:
                pass
        graph.nodes = sorted(set(nodes))
        graph.edge_count = len(edges)
        graph.node_count = len(graph.nodes)
        return graph

    def edges(self, start: int = 0, stop: int = None):
        """Generator to read edges from lines.

        !!! DEPRECATED !!! use lines_to_edges()

        Reads a range of lines, one edge per line, and yields the edges.

        By the start and stop parameters a range can be given.
        The stop parameter is the index behind the last line to use.

        The line to start is set by the parameter start. It defaults to zero.
        The line to stop is set by the parameter stop. When it is not provided
        lines are used as long as they match the edge_pattern reg expression.
        The match behaviour can be adjusted by the self.edge_pattern.
        """
        def _to_edge(match):
            edge = types.SimpleNamespace()
            edge.tail = int(match.group(1))
            edge.head = int(match.group(2))
            if match.group(4):
                edge.weight = int(match.group(4))
            return edge

        if stop is None:
            stop = math.inf
        nr = start
        while nr < stop:
            try:
                line = self.line(nr)
            except IndexError:
                break
            match = re.compile(self.edge_pattern).match(line)
            if match:
                yield (_to_edge(match))
                nr += 1
            else:
                break  # If edges end before stop, which may be infinity

    def fasta(self, start: int = 0, stop: int = None):
        """Generator to read FASTA formatted samples.

        Reads multiple fasta sequences and yields them.

        By the start and stop parameters a range can be given.
        The stop parameter is the index behind the last line to use.

        The line to start is set by the parameter start. It defaults to zero.
        The line to stop is set by the parameter stop. When it is not provided
        lines are used as long as they match the FASTA format.
        The match behaviour can be adjusted by the self.fasta_pattern.
        """
        name, sequence = '', ''
        if stop is None:
            stop = math.inf
        nr = start
        while nr < stop:
            try:
                line = self.line(nr)
            except IndexError:
                break
            if line.startswith('>'):
                if name != '' and sequence != '':
                    # Yield previous sequence if any
                    yield name, sequence
                name, sequence = line[1:], ''  # Reset
            else:
                match = re.compile(self.fasta_pattern).match(line)
                if match:
                    sequence += line
                else:
                    break  # If edges end before stop, which may be infinity
            nr += 1
        # Yield final sequence
        yield name, sequence

    def fasta_strands(self, start: int = 0, stop: int = None):
        """ Get the strands of a fasta read as list.

        Takes the same arguments as self.fasta() and delegates to it.
        """
        return list(dict(self.fasta(start, stop)).values())

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def format_list_of_integers(self, integers: list, joint: str = ', '):
        """Join a list of integers to a string

        Use the given joint.
        """
        return joint.join(str(x) for x in integers)

    def format_path(self, integers: list, backwards: bool = False):
        """Join a list of integers to path of nodes.

        The joint is -> by default. If the parameter
        backwards is True the joint is <-.
        """
        if backwards:
            joint = '<-'
        else:
            joint = '->'
        return self.format_list_of_integers(integers, joint)

    def format_permutations(self, permutations: list, separator: str = '\n',
                            element_separator: str = ' '):
        entries = []
        for perm in permutations:
            entry = '('
            entry += element_separator.join(
                ('+' if i > 0 else '') + str(i) for i in perm)
            entry += ')'
            entries.append(entry)
        return separator.join(entries)
