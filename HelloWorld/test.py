import unittest

from HelloWorld.challenge import HelloWorldChallenge

class HelloWorldTest(unittest.TestCase):
    def setUp(self):
        self.challenge = HelloWorldChallenge()

    def test__init__(self):
        self.assertIsInstance(self.challenge, HelloWorldChallenge)

    def test_build(self):
        self.challenge.lines = ['5', 'xxx']
        self.challenge.build()
        self.assertEqual(5, self.challenge.model.split_at)
        self.assertEqual('xxx', self.challenge.model.word)

    def test_calc(self):
        self.challenge.model.split_at = 5
        self.challenge.model.word = 'honeymoon'
        self.challenge.calc()
        self.assertEqual('moon honey', self.challenge.result)
