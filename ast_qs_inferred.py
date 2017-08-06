import astroid
from astroid.builder import AstroidBuilder
from pylint.pyreverse.utils import ASTWalker

import transform_qs # noqa


node = AstroidBuilder(astroid.MANAGER).string_build('''
from django.db import models

class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role='A')

    def admin_authors(self):
        self.authors().filter(
            is_admin=True)
''')


class QuerySetExprHandler:
    def visit_expr(self, node):
        if isinstance(node.value, astroid.Call):
            inferred = next(node.value.infer())
            print(inferred)
            if inferred.is_subtype_of('django.db.models.query.QuerySet'):
                print('Queryset expr not assigned, '
                      f'line {node.lineno} col {node.col_offset}')


handler = QuerySetExprHandler()
ASTWalker(handler).walk(node)
