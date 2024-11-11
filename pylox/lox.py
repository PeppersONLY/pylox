import sys
import scanner
from token_c import Token

class Lox:
    
    def __init__(self):
        self.had_error: bool = False

        args: list = sys.argv

        if len(args) > 2:
            print("Usage: pylox [script]")
            exit()
        elif len(args) == 2:
            self.run_file(args[1])

    def run_file(self, path: str):
        with open(path) as f:
            source: str = f.read()
        self.run(source)
        if self.had_error: exit(65)
    
    def run(self, source: str):
        scanner_inst: scanner.Scanner = scanner.Scanner(source, self)
        tokens: list[Token] = scanner_inst.scan_tokens()

        for token in tokens:
            print(token, token.lexeme)
    
    def error(self, line: int, message: str):
        self.report(line, "", message)
    
    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

if __name__ == "__main__":
    lox = Lox()