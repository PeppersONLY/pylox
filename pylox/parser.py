from pylox.lox_token import Token
from token_type import TokenType
from expr import *

class Parser:

    class ParseError(Exception):
        pass

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expr:
        try:
            return self.expression()
        except self.ParseError:
            return None

    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr:
        expr: Expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def term(self) -> Expr:
        expr: Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary()
        
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ) after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
    
    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
            
        return False
    
    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type): return self.advance()

        raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str) -> ParseError:
        #lox.error(token, message)
        return self.ParseError()
    
    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON: return

            if self.peek().type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]:
                return
            
            self.advance()

    def check(self, type: TokenType) -> bool:
        if self.is_at_end(): return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]