import ast

tree = ast.parse('''
from django.db import models

class PersonQuerySet(models.QuerySet):
    def admin_authors(self):
        self.filter(
            role='A', is_admin=True)
''')


class QuerySetExprVisitor(ast.NodeVisitor):
    QS_RETURN_METHODS = {'filter', 'exclude', 'all'}  # etc...

    def visit_Expr(self, node):
        if (
                # has a call inside...
                isinstance(node.value, ast.Call) and
                # called function is an attribute of a class (method)...
                isinstance(node.value.func, ast.Attribute) and
                # method returns a queryset...
                node.value.func.attr in self.QS_RETURN_METHODS and
                # method is called over a name...
                isinstance(node.value.func.value, ast.Name) and
                # and that name is 'self'.
                node.value.func.value.id == 'self'):
            print("Queryset expr not assigned, "
                  f"line {node.lineno} col {node.col_offset}")


class QuerySetClassDefVisitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        if any(isinstance(base, ast.Attribute) and
               base.attr == 'QuerySet' for base in node.bases):
            QuerySetExprVisitor().visit(node)


QuerySetClassDefVisitor().visit(tree)
