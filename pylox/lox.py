import sys
import scanner
from pylox.lox_token import Token
from token_type import TokenType
from parser import Parser
from expr import Expr
from ast_printer import AstPrinter
from lox_runtime_error import LoxRuntimeError
from interpreter import Interpreter

class Lox:
    
    def __init__(self):
        self.had_error: bool = False
        self.had_runtime_error: bool = False
        self.interpreter: Interpreter = Interpreter()

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
        if self.had_runtime_error: exit(70)
    
    def run(self, source: str):
        scanner_inst: scanner.Scanner = scanner.Scanner(source, self)
        tokens: list[Token] = scanner_inst.scan_tokens()
        parser: Parser = Parser(tokens)
        expression: Expr = parser.parse()

        if self.had_error: return

        self.interpreter.interpret(expression)

        print(AstPrinter().print(expression))
    
    def error(self, token: Token, message: str):
        if isinstance(token, Token):
            if token.type == TokenType.EOF:
                self.report(token.line, "at end", message)
            else:
                self.report(token.line, f" at '{token.lexeme}'{message}")
        else:
            line: int = token
            self.report(line, "", message)
    
    def runtime_error(self, error: LoxRuntimeError):
        print(f"{error.message}\n[line {error.token.line}]")
        self.had_runtime_error = True
    
    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

if __name__ == "__main__":
    lox = Lox()