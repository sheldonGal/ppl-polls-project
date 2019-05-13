from functools import wraps
from apps.mdb.mdb_macros.utils import wrapper_common

def text_color(color):
    allowed_colors = (
        'red','pink','purple','deep-purple','indigo','blue','light-blue','lime',
        'yellow','amber','orange','deep-orange','brown','grey','blue-grey', 'white'
    )
    assert color in allowed_colors, 'unknown color has been given'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return wrapper_common(func, 'klass', f'{color}-text', *args, **kwargs)

        return wrapper

    return decorator


