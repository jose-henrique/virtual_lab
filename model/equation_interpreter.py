import re

TOKENS = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("PLUS", r"\+"),
    ("MINUS", r"\-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("LAPREN", r"\("),
    ("RPAREN", r"\)"),
    ("SPACE", r"\s+"),
]

token_regex = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKENS))

def lexer(code: str):
    tokens = []
    for match in token_regex.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind == "SPACE":
            continue
        if kind == "NUMBER":
            value = float(value) if "." in value else int(value)
        tokens.append((kind, value))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)
    
    def eat(self, kind=None):
        token = self.peek()
        if kind and token[0] != kind:
            raise SyntaxError(f"Esperado {kind}, mas veio {token}")
        self.pos += 1
        return token
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        value = 0
        while True:
            kind, value = self.peek()
            if kind == "PLUS":
                self.eat("PLUS")
            elif kind == "NUMBER":
                self.eat("NUMBER")
            else:
                break


parser = Parser(lexer("2 + 2"))
print(lexer("2 + 2"))
parser.parse()