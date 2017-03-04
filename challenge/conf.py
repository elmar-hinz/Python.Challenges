# vim: set fileencoding=UTF-8 :

import argparse
import os
import sys
import importlib
import glob

__version__ = '1.0'

class Conf:

    def __init__(self):
        file_extension = '.txt'
        self.root = os.path.dirname(os.path.realpath(__file__ + '/..'))

    def parse_arguments(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("challenge", nargs='?',
                help="The challenge to run.")
        self.parser.add_argument("-f", "--file", action="store",
            help="Load sample from given file.")
        self.parser.add_argument("-k", "--klass", action="store_true",
            help="Use the sample given in the challenge class.")
        self.parser.add_argument("-l", "--list", action="store_true",
            help="List challenges.")
        self.parser.add_argument("-v", "--verbose", action="store_true",
            help="Verbose output.".format(__version__))
        self.parser.add_argument("-V", "--version", action="version",
            version="%(prog)s {}".format(__version__))
        self.parser.add_argument("-w", "--write", action="store_true",
            help="Write input and sample file into challenge directory.")
        if len(sys.argv)==1:
            self.print_help()
        self.args = self.parser.parse_args()

    def print_help(self):
        self.parser.print_help()
        sys.exit(1)

    def get_challenge_dir(self):
        return self.root + '/' + self.args.challenge

    def get_input_file(self):
        return os.path.realpath(self.args.file)

    def get_sample_file(self):
        return os.path.realpath(self.get_challenge_dir() + '/sample.txt')

    def get_result_file(self):
        return os.path.realpath(self.get_challenge_dir() + '/result.txt')

    def get_latest_file(self):
        return os.path.realpath(self.get_challenge_dir() + '/latest.txt')

    def get_latest_at_root(self):
        return os.path.realpath(self.root + '/latest.txt')

    def get_challenges(self):
        pattern = self.root + '/*/'
        return [d for d in (os.path.basename(d[:-1])
                for d in glob.glob(pattern))
                if d[0:1] == d[0:1].upper() and d[0:1] != '_'
               ]

    def get_challenge(self):
        challenge = self.args.challenge
        name = challenge + '.' +  challenge + '.' + challenge
        return self.get_class(name)()

    def get_class(self, klass ):
        parts = klass.split('.')
        module = ".".join(parts[:-1])
        kls = parts[-1]
        return getattr(importlib.import_module(module), kls)


