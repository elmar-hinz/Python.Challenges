# vim: set fileencoding=UTF-8 :

import time
import sys
from challenge.scaffold import Scaffold

class Runner:

    def __init__(self, conf):
        self.start = time.time()
        self.conf = conf
        conf.parse_arguments()

    def main(self):
        if self.conf.args.list:
            self.list_challenges()
        elif self.conf.args.scaffold:
            if self.conf.args.challenge:
                Scaffold(self.conf).scaffold()
            else:
                self.conf.print_help()
        elif self.conf.args.challenge:
            self.run_challenge()
            if self.conf.args.verbose:
                print("--- Time: %s ---" % str(time.time() - self.start))
        else:
            self.conf.print_help()

    def run_challenge(self):
        Challenge = self.conf.get_challenge()
        self.set_sample(Challenge)
        Challenge.main()
        self.write(Challenge)

    def set_sample(self, challenge):
        if self.conf.args.file:
            sample = self.read_file()
        elif self.conf.args.klass:
            sample = challenge.sample
        else:
            stdin = sys.stdin.read().strip()
            if stdin:
                sample = stdin
            else:
                self.conf.print_help()
        challenge.sample = sample

    def read_file(self):
        with open(self.conf.get_input_file(), 'r') as pointer:
            sample = pointer.read()
        return sample

    def write(self, challenge):
        result = challenge.output
        print(result)
        with open(self.conf.get_latest_file(), 'w') as pointer:
            pointer.write(result)
        with open(self.conf.get_latest_at_root(), 'w') as pointer:
            pointer.write(result)
        if self.conf.args.write:
            with open(self.conf.get_sample_file(), 'w') as pointer:
                pointer.write(challenge.sample)
            with open(self.conf.get_result_file(), 'w') as pointer:
                pointer.write(result)

    def list_challenges(self):
        print(' * ' + '\n * '.join(self.conf.get_challenges()))


