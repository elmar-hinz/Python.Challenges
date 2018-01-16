import unittest

from HelloWorld.challenge import HelloWorldChallenge


class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        self.challenge = HelloWorldChallenge()

    def test__init__(self):
        self.assertIsInstance(self.challenge, HelloWorldChallenge)
        self.assertIn('WorldHello', self.challenge.sample)
        self.assertIn('Hello World', self.challenge.expect)

    def test_build(self):
        self.challenge.read()
        self.challenge.build()
        self.assertEqual(5, self.challenge.model.split_at)
        self.assertEqual('WorldHello', self.challenge.model.word)

    def test_calc(self):
        self.challenge.model.split_at = 5
        self.challenge.model.word = 'honeymoon'
        self.challenge.calc()
        self.assertEqual('moon honey', self.challenge.result)

    def test_full_integration(self):
        self.challenge.main()
        self.assertEqual(self.challenge.expectation(), self.challenge.output)
