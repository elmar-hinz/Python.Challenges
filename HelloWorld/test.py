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
        self.challenge.model.word = 'WorldHello'
        self.challenge.calc()
        self.assertEqual('Hello World', self.challenge.result.word)
        self.assertEqual(11, self.challenge.result.length)

    def test_format(self):
        self.challenge.result.word = 'Hello World'
        self.challenge.result.length = 11
        self.challenge.format()
        self.assertEqual(self.challenge.expectation(), self.challenge.output)

    def test_full_integration(self):
        self.challenge.main()
        self.assertEqual(self.challenge.expectation(), self.challenge.output)
