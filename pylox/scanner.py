from pylox.lox_token import Token
from typing import Any
from token_type import TokenType
import lox

class Scanner:

    def __init__(self, source: str, lox_interp: lox.Lox):
        self.lox_interp: lox.Lox = lox_interp
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.keywords: dict[str, TokenType] = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN, 
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: Any|None=None):
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scan_token(self):
        c: str = self.advance()
        
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case "":
                pass
            case "\r":
                pass
            case "\t":
                #Whitespace
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    self.lox_interp.error(self.line, "Unexpected character.")
    
    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text: str = self.source[self.start:self.current]
        type: TokenType = self.keywords.get(text)
        if type == None: type = TokenType.IDENTIFIER

        self.add_token(type)
    
    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    @staticmethod
    def is_digit(c: str) -> bool:
        return c >= "0" and c <= "9"
    
    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        #Consume for a fractional part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            #consume the "."
            self.advance()

            while self.is_digit(self.peek()): self.advance()
        
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
        
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            self.lox_interp.error(self.lox_interp, self.line, "Unterminated character.")
            return
        
        #Closing "
        self.advance()

        #Trim the surrounding quotes
        value: str = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)
        
    def match(self, expected: str) -> bool:
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.is_at_end(): return "\0"
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current >= len(self.source): return "\0"
        return self.source[self.current+1]