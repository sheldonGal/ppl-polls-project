from functools import wraps
from apps.mdb.mdb_macros.utils import wrapper_common

def button_factory(atype, outline = False, rounded = False, size = None, block = False):
    allowed_types = (
        'primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'link',
        'default', 'elegant', 'unique', 'pink', 'purple', 'deep-purple', 'indigo', 'light-blue',
        'cyan', 'dark-green', 'light-green', 'yellow', 'brown', 'amber','deep-orange', 'blue-grey', 'mdb-color'
    )
    allowed_sizes = ('sm', 'lg', None)

    assert atype in allowed_types, 'unknown type'
    assert size in allowed_sizes, 'unknown size'

    if size is None:
        size_add = ''
    else:
        size_add = f' btn-{size}'
    if block:
        block_add = f' btn-block'
    else:
        block_add = ''

    if outline and rounded:
        to_add = f'btn btn-outline-{atype} btn-rounded waves-effect{size_add}{block_add}'
    elif outline:
        to_add = f'btn btn-outline-{atype} waves-effect{size_add}{block_add}'
    elif rounded:
        to_add = f'btn btn-{atype} btn-rounded{size_add}{block_add}'
    else:
        to_add = f'btn btn-{atype}{size_add}{block_add}'


    rounded_add = 'btn-rounded waves-effect'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return wrapper_common(func, 'klass', to_add, *args, **kwargs)

        return wrapper

    return decorator



