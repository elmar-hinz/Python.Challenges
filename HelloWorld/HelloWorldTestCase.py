import unittest

from HelloWorld.HelloWorld import HelloWorld


class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.challenge = HelloWorld()

    def test__init__(self):
        self.assertIsInstance(self.challenge, HelloWorld)

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
