# https://github.com/elmar-hinz/Python.Challenges
from challenges import Challenge

class HelloFastaChallenge(Challenge):
    """
    Given: A DNA strand followed by fasta reads.
    Return: The id of the read which the shortest distance to the given strand.
    """

    sample = '''
        ACCGGTCC
        >Fasta1
        AGCG
        GGCC 
        >Fasta2
        ACCC
        GTCC 
        >Fasta3
        ACCG
        TTTT 
    '''

    expect = 'Fasta2'

    def build(self):
        self.model.strand = self.line(0)
        self.model.fasta = self.fasta(1)

    def calc(self):
        winner = None
        maximum = 0
        for id, strand in self.model.fasta:
            counter = 0
            for position, base in enumerate(self.model.strand):
                if strand[position] == base:
                    counter += 1
            if counter > maximum:
                maximum = counter
                winner = id
        self.result = winner