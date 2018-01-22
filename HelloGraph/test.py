import unittest
from HelloGraph.challenge import HelloGraphChallenge

class HelloGraphTest(unittest.TestCase):

    def setUp(self):
        self.challenge = HelloGraphChallenge()

    def test__init__(self):
        self.assertIsInstance(self.challenge, HelloGraphChallenge)
        self.assertIn('5->6', self.challenge.sample)
        self.assertIn('2->3->4', self.challenge.expect)

    def test_build(self):
        self.challenge.read()
        self.challenge.build()
        self.assertEqual(2, self.challenge.model.start)
        self.assertEqual(4, self.challenge.model.stop)
        self.assertIn(4, self.challenge.model.edges[3])
        self.assertEqual(10, self.challenge.model.weights[(3, 4)])

    def test_format(self):
        self.challenge.result.weight = 14
        self.challenge.result.path = [2, 3, 4]
        self.challenge.format()
        self.assertEqual(self.challenge.expectation(), self.challenge.output)

    def test_full_integration(self):
        self.challenge.main()
        self.assertEqual(self.challenge.expectation(), self.challenge.output)