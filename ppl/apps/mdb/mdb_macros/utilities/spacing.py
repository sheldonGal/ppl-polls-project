from functools import wraps
from apps.mdb.mdb_macros.utils import wrapper_common

__all__ = ['margin']

def margin(prop, side, size):
    allowed_properties = ('m','p')
    allowed_sides = (
        't', # top
        'b', # bottom
        'l', # left
        'r', # right
        'x', # left and right
        'y', # top and bottom
        'blank' # margin or padding on all 4 sides
    )
    allowed_sizes = (0,1,2,3,4,5)

    assert prop in allowed_properties, 'm or p'
    assert side in allowed_sides, 'unknown side'
    assert size in allowed_sizes, '0 to 5'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return wrapper_common(func, 'klass', f'{prop}{side}-{size}', *args, **kwargs)

        return wrapper
    return decorator