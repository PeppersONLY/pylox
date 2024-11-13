from abc import ABC, abstractmethod
from pylox.lox_token import Token
from typing import Any

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression: Expr = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value: Any = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        pass
    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        pass
    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        pass
    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        pass