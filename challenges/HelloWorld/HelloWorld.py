from lib.challenge import Challenge

class  HelloWorld(Challenge):

    sample = '''
        5
        WorldHello
    '''

    def build(self):
        self.model.splitAt = self.lineToIntegers(0)[0]
        self.model.word = self.line(1)

    def calc(self):
        first = self.model.word[self.model.splitAt:]
        second = self.model.word[:self.model.splitAt]
        self.result = first + ' ' + second

