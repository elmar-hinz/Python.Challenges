import unittest
from types import SimpleNamespace

from challenges import Challenge


class ChallengeTestCase(unittest.TestCase):
    """Test cases of the challenge base class."""

    def setUp(self):
        self.challenge = Challenge()

    def test_class_attributes(self):
        """Check setting of class attributes."""
        self.assertEqual(Challenge.sample, 'sample')
        self.assertEqual(Challenge.br, '\n', Challenge.br)
        self.assertEqual(Challenge.split_pattern, '\s+|\s?,\s?')
        self.assertEqual(Challenge.edge_pattern, '^(\d+)->(\d+)(:(\d+))?$')

    def test_instance_attributes(self):
        """Check setting of instance attributes."""
        self.assertIsInstance(self.challenge.lines, list)
        self.assertIsInstance(self.challenge.model, SimpleNamespace)
        self.assertIsInstance(self.challenge.result, SimpleNamespace)
        self.assertEqual(self.challenge.output, '')

    def test_instance_shadows_class_attribute_of_sample(self):
        """ Show that instance attribute shadows class attribute."""
        self.assertEqual(Challenge.sample, 'sample')
        self.assertEqual(self.challenge.sample, 'sample')
        self.challenge.sample = 'mine'
        self.assertEqual(Challenge.sample, 'sample')
        self.assertEqual(self.challenge.sample, 'mine')

    def test_read(self):
        """Show that read creates list of lines."""
        self.challenge.sample = 'one\ntwo'
        self.challenge.read()
        self.assertEqual(self.challenge.lines, ['one', 'two'])

    def test_build(self):
        """Show that build is callable."""
        self.challenge.build()
        self.assertTrue(True)

    def test_calc(self):
        """Show that calc is callable."""
        self.challenge.calc()
        self.assertTrue(True)

    def test_format(self):
        """Show that format writes result into output as string."""
        self.challenge.result = 2
        self.challenge.format()
        self.assertIsInstance(self.challenge.output, str)
        self.assertEqual(self.challenge.output, '2')

    def test_line(self):
        """ Show that a line is retrievable by index."""
        self.challenge.lines = ['one', 'two', 'three']
        self.assertEqual(self.challenge.line(1), 'two')

    def test_line_to_integers(self):
        """Show a line can be retrieved as integers."""
        self.challenge.lines = ['one', '1, 2, 3']
        result = self.challenge.line_to_integers(1)
        self.assertEqual(result, [1, 2, 3])

    def test_line_to_floats(self):
        """Show a line can be retrieved as floats."""
        self.challenge.lines = ['one', '1.11, 2.22']
        result = self.challenge.line_to_floats(1)
        self.assertEqual(result, [1.11, 2.22])

    def test_line_to_edge(self):
        """Show a line can be retrieved as edge."""
        self.challenge.lines = ['one', '1->2:12']
        result = self.challenge.line_to_edge(1)
        self.assertIsInstance(result, SimpleNamespace)
        self.assertEqual(result.tail, 1)
        self.assertEqual(result.head, 2)
        self.assertEqual(result.weight, 12)

    def test_line_to_edge_without_weight(self):
        """Show a line can be retrieved as edge."""
        self.challenge.lines = ['one', '1->2']
        result = self.challenge.line_to_edge(1)
        self.assertIsInstance(result, SimpleNamespace)
        self.assertEqual(result.tail, 1)
        self.assertEqual(result.head, 2)
        with self.assertRaises(AttributeError):
            print(result.weight)

    def test_read_edges_from_to(self):
        """Show reading edges limited by start and stop."""
        self.challenge.sample = '''
        0
        1->9
        2->9
        3->9
        4->9
        5
        '''
        self.challenge.read()
        result = self.challenge.read_edges(start=2, stop=4)
        self.assertEqual(result.__name__, 'read_edges')
        self.assertEqual(len(list(result)), 2)

    def test_read_edges_from(self):
        """Show reading edges self limiting."""
        self.challenge.sample = '''
        0
        1->9
        2->9
        3->9
        4->9
        5
        '''
        self.challenge.read()
        result = self.challenge.read_edges(start=2)
        self.assertEqual(len(list(result)), 3)

    def test_read_edges_without_given_range(self):
        """Show reading edges without given range starting from line 0."""
        self.challenge.sample = '''
        1->9
        2->9
        3->9
        '''
        self.challenge.read()
        result = self.challenge.read_edges()
        self.assertEqual(len(list(result)), 3)

    def test_format_list_of_integers(self):
        """Show concatenation of list of integers."""
        self.assertEqual(self.challenge.format_list_of_integers([1, 2]),
                         '1, 2')

    def test_format_path(self):
        """Show concatenation of list of nodes to a path."""
        result = self.challenge.format_path([11, 22, 33])
        self.assertEqual(result, '11->22->33')
        result = self.challenge.format_path([11, 22, 33], backwards=True)
        self.assertEqual(result, '11<-22<-33')
