"""Core module of challenges

This module holds the base class of all challenges.
"""

import re
import types


class Challenge:
    """Base class of all challenges

    Idea of this class is the Template Method Design Pattern (GOF).

    Workflow
    ========

    The main() method controls the overall workflow by calling the worker
    methods read(), build(), calc() and format() in that order. Typically the
    main() method is not changed.

    Workers
    =======

    The workers need to be extended or implemented by the inheriting challenge
    implementations.

     * read(): This method is typically not changed.
     * build(): Abstract method that needs implementation.
     * calc(): Abstract method. The implementation holds or calls the algorithm
     of the challenge.
     * format(): Needs implementation for advanced challenges.

    Library
    =======

    The other functions are library methods to support the implementation of
    the workers. Most of them support extraction of data from the input lines
    or formatting the output.
    """

    sample = 'sample'
    """Holds a minimal example of the input.

    This variable should always be overwritten in the derived class by a
    smallest example of the challenges input. It is expected by the challenge
    runner (--klass option) as well as by unit tests to be present.
    """

    br = line_break = '\n'
    """Line breaks as expected by the most graders."""

    split_pattern = '\s+|\s?,\s?'
    """Regex pattern to split input lines.

    Used by some of the input parsing functions. By default it splits by
    whitespace and/or comma. If the input is separated differently like colons
    or semicolons it needs adjustment in the inheriting class.
    """

    edge_pattern = '^(\d+)->(\d+)(:(\d+))?$'
    """Regex to exctract graph edges.

    A default setting used by methods that extract edges from input lines.
    May need adjustment for differnt kind of edge input formats.
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

        This method usually doesn't need a different implementation. This
        workflow is the common character of all challenges.

        The methods share data via instance variables.
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
        lines = self.sample.strip().splitlines()
        self.lines = [line.strip() for line in lines]

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
        """Foramt the output string.

        In simple cases this method can be used as is. In other cases it
        needs to be reimplemented.

        Reads from self.result.
        Fills self.output.
        """
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
