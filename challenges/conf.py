import argparse
import glob
import importlib
import os
import sys


class Conf:
    def __init__(self):
        sys.path.insert(0, '.')
        sys.setrecursionlimit(5000)
        self.root = os.path.realpath('.')
        self.parser = None
        self.args = None
        path = '{0}/version.txt'.format(os.path.realpath(
            os.path.dirname(__file__)))
        with open(path) as f:
            self.version = f.read().strip()

    def parse_arguments(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('challenge', nargs='?',
                                 help='the challenge to run, to scaffold or '
                                      'to test')
        self.parser.add_argument('-f', '--file', action='store',
                                 help='load sample from given file')
        self.parser.add_argument('-k', '--klass', action='store_true',
                                 help='use sample form challenge class file')
        self.parser.add_argument('-l', '--list', action='store_true',
                                 help='list challenges')
        self.parser.add_argument('-s', '--scaffold', action='store_true',
                                 help="scaffold challenge")
        self.parser.add_argument('-u', '--unittest', action='store_true',
                                 help='unittest challenge')
        self.parser.add_argument('-v', '--verbose', action='store_true',
                                 help='verbose output')
        self.parser.add_argument('-V', '--version', action='version',
                                 version='%(prog)s {}'.format(self.version))
        self.parser.add_argument('-w', '--write', action='store_true',
                                 help='write input and sample file into '
                                      'challenge directory')
        if len(sys.argv) == 1:
            self.print_help()
        self.args = self.parser.parse_args()
        if self.args.challenge and self.args.challenge[-1:] == '/':
            self.args.challenge = self.args.challenge[0:-1]

    def print_help(self):
        self.parser.print_help()
        sys.exit(1)

    def get_challenge_dir(self):
        return self.root + '/' + self.args.challenge

    def get_challenge_file(self):
        challenge = self.args.challenge
        return self.root + '/' + challenge + '/challenge.py'

    def get_unittest_file(self):
        challenge = self.args.challenge
        return self.root + '/' + challenge + '/test.py'

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

    def get_challenge_name(self):
        return self.args.challenge

    def get_full_qualified_challenge_name(self):
        challenge = self.get_challenge_name()
        return challenge + '.challenge.' + challenge + 'Challenge'

    def get_full_qualified_unittest_name(self):
        challenge = self.get_challenge_name()
        return challenge + '.test.' + challenge + 'Test'

    def get_challenge(self):
        return self.get_class(self.get_full_qualified_challenge_name())()

    def get_unittest(self):
        return self.get_class(self.get_full_qualified_unittest_name())

    @staticmethod
    def get_class(class_):
        parts = class_.split('.')
        module = ".".join(parts[:-1])
        return getattr(importlib.import_module(module), parts[-1])
