import os
import sys


class Scaffold:
    def __init__(self, conf):
        self.conf = conf

    def scaffold(self):
        directory = self.conf.get_challenge_dir()
        if os.path.exists(directory):
            sys.exit('Directory ' + directory + ' already exists.')
        else:
            try:
                os.makedirs(directory)
            except OSError:
                sys.exit('Sorry, could not create ' + directory + '.')

        file = self.conf.get_challenge_init_file()
        if os.path.exists(file):
            sys.exit('File ' + file + ' already exists.')
        else:
            try:
                with open(file, 'w') as handle:
                    handle.write('')
            except OSError:
                sys.exit('Sorry, could not write ' + file + '.')

        file = self.conf.get_challenge_file()
        if os.path.exists(file):
            sys.exit('File ' + file + ' already exists.')
        else:
            try:
                with open(file, 'w') as handle:
                    handle.write(self.get_class_content())
            except OSError:
                sys.exit('Sorry, could not write ' + file + '.')
        file = self.conf.get_unittest_file()
        if os.path.exists(file):
            sys.exit('File ' + file + ' already exists.')
        else:
            try:
                with open(file, 'w') as handle:
                    handle.write(self.get_unittest_content())
            except OSError:
                sys.exit('Sorry, could not write ' + file + '.')

    def get_class_content(self):
        text = '''
from challenges import Challenge

class {}Challenge(Challenge):

    sample = 'XXX'
    expect = 'XXX'

    def build(self):
        pass

    def calc(self):
        self.result = 'XXX'
'''
        return text.strip().format(self.conf.get_challenge_name())

    def get_unittest_content(self):
        text = '''
import unittest
from {}.challenge import {}Challenge

class {}Test(unittest.TestCase):

    def setUp(self):
        self.challenge = {}Challenge()

    def test__init__(self):
        self.assertIsInstance(self.challenge, {}Challenge)
        self.assertIn('XXX', self.challenge.sample)

    def test_build(self):
        self.skipTest('Not implemented.')

    def test_calc(self):
        self.skipTest('Not implemented.')

    def test_format(self):
        self.skipTest('Not implemented.')

    def test_full_integration(self):
        self.challenge.main()
        self.assertEqual(self.challenge.expect, self.challenge.output)
'''
        n = self.conf.get_challenge_name()
        return text.strip().format(n, n, n, n, n)
