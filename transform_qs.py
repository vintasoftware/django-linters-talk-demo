import astroid


QS_RETURN_METHODS = {'filter', 'exclude', 'all'}  # etc...


def infer_queryset_return(node, context=None):
    try:
        qs_instance = next(node.func.expr.infer(context))
    except astroid.InferenceError:
        raise astroid.UseInferenceDefault

    if qs_instance.is_subtype_of('django.db.models.query.QuerySet'):
        return iter([qs_instance])
    else:
        raise astroid.UseInferenceDefault


def looks_like_queryset_method_call(node):
    if isinstance(node.func, astroid.Attribute):
        func_name = node.func.attrname
    elif isinstance(node.func, astroid.Name):
        func_name = node.func.name
    else:
        func_name = ''
    return func_name in QS_RETURN_METHODS


def add_transforms(manager):
    manager.register_transform(
        node_class=astroid.Call,
        transform=astroid.inference_tip(infer_queryset_return),
        predicate=looks_like_queryset_method_call)


add_transforms(astroid.MANAGER)
