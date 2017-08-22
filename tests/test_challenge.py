import unittest

from types import SimpleNamespace

from challenges import Challenge


class ChallengeTestCase(unittest.TestCase):

    """Test cases of the challenge base class."""

    def setUp(self):
        self.challenge = Challenge()

    def test_class_attributes(self):
        """Check setting of class attributes."""
        self.assertIn('sample', self.challenge.sample)
        self.assertIn('expected result', self.challenge.expect)
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
        self.assertIn('sample', Challenge.sample)
        self.assertIn('sample', self.challenge.sample)
        self.challenge.sample = 'mine'
        self.assertIn('sample', Challenge.sample)
        self.assertIn('mine', self.challenge.sample)

    def test_instance_shadows_class_attribute_of_expect(self):
        """ Show that instance attribute shadows class attribute."""
        self.assertIn('expected result', Challenge.expect)
        self.assertIn('expected result', self.challenge.expect)
        self.challenge.expect = 'my result'
        self.assertIn('expected result', Challenge.expect)
        self.assertIn('my result', self.challenge.expect)

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
        result = self.challenge.edges(start=2, stop=4)
        self.assertEqual(result.__name__, 'edges')
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
        result = self.challenge.edges(start=2)
        self.assertEqual(len(list(result)), 3)

    def test_read_edges_without_given_range(self):
        """Show reading edges without given range starting from line 0."""
        self.challenge.sample = '''
        1->9
        2->9
        3->9
        '''
        self.challenge.read()
        result = self.challenge.edges()
        self.assertEqual(len(list(result)), 3)

    def test_read_fasta_from_to(self):
        """Show reading FASTA limited by start and stop."""
        self.challenge.sample = '''
        0
        1
        >FAS_1
        CCTGCGGAAGATCGGCACTAGAATAGCCAGAACCGTTTCTCTGAGGCTTCCGGCCTTCCC
        TCCCACTAATAATTCTGAGG
        >FAS_2
        CCATCGGTAGCGCATCCTTAGTCCAATTAAGTCCCTATCCAGGCGCTCCGCCGAAGGTCT
        ATATCCATTTGTCAGCAGACACGC
        >FAS_3
        CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGAC
        TGGGAACCTGCGGGCAGTAGGTGGAAT
        >FAS_4
        CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGAC
        TGGGAACCTGCGGGCAGTAGGTGGAAT
        14
        '''
        self.challenge.read()
        result = self.challenge.fasta(start=5, stop=11)
        self.assertEqual(result.__name__, 'fasta')
        self.assertEqual(len(list(result)), 2)

    def test_read_fasta_from(self):
        """Show reading FASTA self limiting."""
        self.challenge.sample = '''
        0
        1
        >FAS_1
        CCTGCGGAAGATCGGCACTAGAATAGCCAGAACCGTTTCTCTGAGGCTTCCGGCCTTCCC
        TCCCACTAATAATTCTGAGG
        >FAS_2
        CCATCGGTAGCGCATCCTTAGTCCAATTAAGTCCCTATCCAGGCGCTCCGCCGAAGGTCT
        ATATCCATTTGTCAGCAGACACGC
        >FAS_3
        CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGAC
        TGGGAACCTGCGGGCAGTAGGTGGAAT
        >FAS_4
        AAA
        TTT
        14
        '''
        self.challenge.read()
        result = self.challenge.fasta(start=5)
        self.assertEqual(result.__name__, 'fasta')
        fasta = dict(result)
        self.assertEqual('AAATTT', fasta['FAS_4'])
        self.assertEqual(len(fasta), 3)

    def test_read_fasta_without_given_range(self):
        """Show reading FASTA limited by start and stop."""
        self.challenge.sample = '''
        >FAS_1
        CCTGCGGAAGATCGGCACTAGAATAGCCAGAACCGTTTCTCTGAGGCTTCCGGCCTTCCC
        TCCCACTAATAATTCTGAGG
        >FAS_2
        CCATCGGTAGCGCATCCTTAGTCCAATTAAGTCCCTATCCAGGCGCTCCGCCGAAGGTCT
        ATATCCATTTGTCAGCAGACACGC
        >FAS_3
        CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGAC
        TGGGAACCTGCGGGCAGTAGGTGGAAT
        >FAS_4
        CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGAC
        TGGGAACCTGCGGGCAGTAGGTGGAAT
        '''
        self.challenge.read()
        result = self.challenge.fasta()
        self.assertEqual(result.__name__, 'fasta')
        self.assertEqual(len(list(result)), 4)

    def test_read_fasta_format(self):
        """Show reading FASTA matches expected format."""
        self.challenge.sample = '''
        0
        1
        >FAS_1
        LLL
        ---
        MMM
        *
        >FAS_2
        AAA
        TTT
        8
        '''
        self.challenge.read()
        result = self.challenge.fasta(start=2)
        self.assertEqual(result.__name__, 'fasta')
        fasta = dict(result)
        self.assertIn('FAS_1', fasta.keys())
        self.assertEqual('LLL---MMM*', fasta['FAS_1'])
        self.assertIn('FAS_2', fasta.keys())
        self.assertEqual('AAATTT', fasta['FAS_2'])

    def test_fasta_strands(self):
        """ Check the method works as expected. """
        self.challenge.sample = '''
        >FAS_1
        AAA
        >FAS_2
        CCC
        '''
        self.challenge.read()
        result = self.challenge.fasta_strands()
        self.assertEqual(['AAA', 'CCC'], result)

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
