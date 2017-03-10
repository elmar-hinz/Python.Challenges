"""Core module of challenges

This module holds the base class of all challenges.
"""

import re
import types
import math


class Challenge:
    """Base class of all challenges

    Designe concept is the Template Method Design Pattern (GOF).

    Attributes
    ----------

    :sample:    The input of the challenge.
    :output:    The output of the challenge

    Workflow
    --------

    The `main` method controls the overall workflow by calling the worker
    methods. This is the common character of all challenges.
    The base class controls the workflow of the derived workers.

    Workers
    -------

    The worker methods need to be implemented by the inheriting class.

    :read:     Read the input into a list of lines.
    :build:    Build the data model from the lines.
    :calc:     Run the main algorithm of the challenge.
    :format:   Create the output string required by the grader.

    Library
    -------

    The other methods support the implementation of the workers. They address
    the extraction of data from the input lines or the formatting of the
    output.

    Sample
    ------

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

    sample = 'sample'
    """Holds a minimal example of the input.

    This class variable should always be preset with a tiny sample of input.
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

    A default setting used by methods that extract edges from input lines.
    May need adjustment for different kind of edge input formats.
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
        """Format the output string.

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
        """ Return one line by the given number. """
        return self.lines[number]

    def line_to_integers(self, line_nr):
        """ Split one line into  a list of integers.

        The number of the line is selected by line_nr.
        The split behaviour can be adjusted by changing self.split_pattern.
        """

        return [int(i) for i in
                re.compile(self.split_pattern).split(self.line(line_nr))]

    def line_to_floats(self, line_nr):
        """ Split one line into  a list of floats.

        The number of the line is selected by line_nr.
        The split behaviour can be adjusted by changing self.split_pattern.
        """
        return [float(i) for i in
                re.compile(self.split_pattern).split(self.line(line_nr))]

    def line_to_edge(self, nr):
        """Convert one line to an edge.

        The number of the line is selected by line_nr.
        The split behaviour can be adjusted by changing self.edge_pattern.
        """
        print(self.edge_pattern)
        print(self.line(nr))
        m = re.compile(self.edge_pattern).match(self.line(nr))
        print(m)
        return self._to_edge(re.compile(self.edge_pattern).match(
            self.line(nr)))

    def read_edges(self, start=0, stop=None):
        """Generator to read edges from lines.

        Reads a range of lines, one edge per line, and yields the edges.

        By the start and stop parameters a range can be given.
        The stop parameter is the index behind the last line to use.

        The line to start is set by the parameter start. It defaults to zero.
        The line to stop is set by the parameter stop. When it is not provided
        lines are used as long as they match the edge_pattern reg expression.
        The split behaviour can be adjusted by the self.edge_pattern.
        """
        if stop == None:
            stop = math.inf
        nr = start
        while nr < stop:
            try:
                line = self.line(nr)
            except IndexError:
                break
            match = re.compile(self.edge_pattern).match(line)
            if match:
                yield (self._to_edge(match))
                nr += 1
            else:
                break # If edges end before stop, wich may be infinity

    def _to_edge(self, match):
        edge = types.SimpleNamespace()
        edge.tail = int(match.group(1))
        edge.head = int(match.group(2))
        if match.group(4):
            edge.weight = int(match.group(4))
        return edge

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    def format_list_of_integers(self, integers, joint=', '):
        """Join a list of integers to a string

        Use the given joint.
        """
        return joint.join(str(x) for x in integers)

    def format_path(self, integers, backwards=False):
        """Join a list of integers to path of nodes.

        The joint is -> by default. If the parameter
        backwards is True the joint is <-.
        """
        if backwards == True:
            joint = '<-'
        else:
            joint = '->'
        return self.format_list_of_integers(integers, joint)


