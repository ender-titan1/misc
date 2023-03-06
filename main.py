from enum import Enum
from dataclasses import dataclass

# pylint: disable-all

class TokenType(Enum):
    TEXT = 0

    BOLD_BEGIN = 1
    BOLD_END = 2

    ITALIC_BEGIN = 3
    ITALIC_END = 4

@dataclass
class Token:
    type: TokenType
    content: str

class Reader:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.content = file.read()

        self.bold = False
        self.italic = False

        self.i = 0
        self.current = ' '
        self.complete = False

        self.output = []

        self.advance()

    def advance(self):
        if self.i == len(self.content):
            self.complete = True
        else:
            self.i += 1
            self.current = self.content[self.i]

    def read(self):
        while not self.complete:

            if self.current == '*':
                self.handle_star()

            self.advance()

    def handle_star(self):
        count = 0
        
        while self.current == '*' and not self.complete:
            count += 1
            self.advance()

        token_type = 0

        if count == 1:
            token_type = 3
        else:
            token_type = 1
        
        

        
