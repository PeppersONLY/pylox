from token_type import TokenType
from typing import Any

class Token:

    def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int):
        self.type: TokenType = type
        self.lexeme: str = lexeme
        self.literal: Any = literal
        self.line: int = line
    
    def to_string(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"