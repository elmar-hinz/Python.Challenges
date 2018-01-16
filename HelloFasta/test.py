import unittest
from HelloFasta.challenge import HelloFastaChallenge

class HelloFastaTest(unittest.TestCase):

    def setUp(self):
        self.challenge = HelloFastaChallenge()

    def test__init__(self):
        self.assertIsInstance(self.challenge, HelloFastaChallenge)
        self.assertIn('Fasta3', self.challenge.sample)
        self.assertIn('Fasta2', self.challenge.expect)

    def test_build(self):
        self.challenge.read()
        self.challenge.build()
        self.assertEqual('ACCGGTCC', self.challenge.model.strand)
        fasta = list(self.challenge.model.fasta)
        self.assertEqual('Fasta3', fasta[2][0])
        self.assertEqual('ACCGTTTT', fasta[2][1])

    def test_full_integration(self):
        self.challenge.main()
        self.assertEqual(self.challenge.expectation(), self.challenge.output)