'''
mypy doesn't have an official API for type inference [1] and it doesn't
do inference inside functions that don't have type annotations [2],
so what we're doing here doesn't make much sense. It just explores what
mypy can do in the future.

[1] https://github.com/python/mypy/issues/2097#issuecomment-319224603
[2] http://mypy.readthedocs.io/en/latest/dynamic_typing.html#dynamically-typed-code
'''

from mypy import build, types
from mypy.options import Options
from mypy.traverser import TraverserVisitor


options = Options()
options.use_builtins_fixtures = True
options.show_traceback = True
options.strict_optional = True
options.check_untyped_defs = True  # this doesn't seem to activate inference inside untyped defs
options.warn_return_any = True
options.warn_no_return = True

program_text = '''from django.db import models

class PersonQuerySet(models.QuerySet):
    def authors(self) -> 'PersonQuerySet':
        return self.filter(role='A')

    def admin_authors(self) -> 'PersonQuerySet':
        self.authors().filter(is_admin=True)
'''
source = build.BuildSource('main', '__main__', program_text)
result = build.build(sources=[source],
                     options=options,
                     alt_lib_path='stubs')
# mypy already detects admin_authors is missing return...
print('result.errors', result.errors)


class MyVisitor(TraverserVisitor):
    def visit_expression_stmt(self, node):
        if isinstance(result.types[node.expr], types.Instance):
            typeinfo = result.types[node.expr].type

            if typeinfo.has_base('django.db.models.query.QuerySet'):
                print("Queryset expr not assigned, "
                      f"line {node.line} col {node.column}")

        super().visit_expression_stmt(node)


result.files['__main__'].accept(MyVisitor())
