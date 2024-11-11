from expr import *

class AstPrinter(Visitor):

    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)
    
    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value == None: return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: Unary) -> None:
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name: str, *exprs: tuple[Expr]) -> str:
        res: str = f"({name}"
        
        for expr in exprs:
            res += " "
            res += expr.accept(self)
        res += ")"

        return res