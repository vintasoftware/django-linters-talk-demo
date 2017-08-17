'''
mypy doesn't have an official API for type inference [1], it doesn't
do inference inside functions that don't have type annotations [2], and
it doesn't try to infer types of modules that don't have a stub or
typing info [3]. Therefore, what we're doing here doesn't make much sense.
It just explores what mypy can do in the future.

[1] https://github.com/python/mypy/issues/2097#issuecomment-319224603
[2] http://mypy.readthedocs.io/en/latest/dynamic_typing.html#dynamically-typed-code
[3] https://github.com/python/mypy/issues/638
'''
import typed_ast.ast3
import typed_astunparse

from mypy import build, types
from mypy.options import Options
from mypy.traverser import TraverserVisitor


options = Options()
options.use_builtins_fixtures = True
options.show_traceback = True
options.strict_optional = True
options.check_untyped_defs = True
options.warn_return_any = True
options.warn_no_return = True

program_text = '''from django.db import models

class PersonQuerySet(models.QuerySet):
    def authors(self):
        return self.filter(role='A')

    def admin_authors(self):
        self.authors().filter(is_admin=True)
'''


class AddClassTypeToSelf(typed_ast.ast3.NodeTransformer):
    # TODO: need to also add return to work...
    def visit_ClassDef(self, class_node):
        for method in class_node.body:
            if isinstance(method, typed_ast.ast3.FunctionDef):
                if len(method.args.args) and method.args.args[0].arg == 'self':
                    if method.args.args[0].annotation is None:
                        method.args.args[0].annotation = typed_ast.ast3.Str(class_node.name)
        return class_node


program_text = typed_astunparse.unparse(
    AddClassTypeToSelf().visit(
        typed_ast.ast3.parse(program_text)))

source = build.BuildSource('main', '__main__', program_text)
result = build.build(sources=[source],
                     options=options,
                     alt_lib_path='stubs')
# mypy already detects admin_authors is missing return...
# however, if `-> 'PersonQuerySet'` is removed,
# it infers the admin_authors expression_stmt body as Any.
# mypy does not infer the type of self when the function is untyped.
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
