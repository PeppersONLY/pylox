from expr import *
from abc import abstractmethod
from typing import Any
from token_type import TokenType
from lox_runtime_error import LoxRuntimeError

class Interpreter(Visitor):

    def interpret(self, expression: Expr):
        try:
            value: Any = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            #Lox.runtimerror(error)
            pass

    @abstractmethod
    @staticmethod
    def visit_literal_expr(expr: Expr) -> Any:
        return expr.value
    
    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> Any:
        right: Any = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)
        
        return None
    
    @staticmethod
    def check_number_operand(operator: Token, operand: Any):
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, "Operand must be a number")
    
    @staticmethod
    def check_number_operands(operator: Token, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float): return

        raise LoxRuntimeError(operator, "Operands must be numbers")

    @staticmethod
    def is_truthy(object: Any) -> bool:
        if object == None: return False
        if isinstance(object, bool): return object
        return True

    @staticmethod
    def is_equal(a: Any, b: Any) -> bool:
        if a == None and b == None: return True
        if a == None: return False

        return a == b
    
    def stringify(self, object: Any) -> str:
        if object == None: return "nil"

        if isinstance(object, float):
            text: str = str(object)
            if text.endswith('.0'):
                text = text[0:len(text) - 2]
            
            return text
        
        return str(object)

    @abstractmethod
    def visit_grouping_expr(self, expr: Expr) -> Any:
        return self.evaluate(expr.expression)
    
    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)
    
    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> Any:
        left: Any = self.evaluate(expr.right)
        right: Any = self.evaluate(expr.left)

        match expr.operator.type:
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL: return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL: return self.is_equal(left, right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                
                raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings")
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            
        return None