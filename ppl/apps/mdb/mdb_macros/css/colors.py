from functools import wraps
from apps.mdb.mdb_macros.utils import wrapper_common

__all__ = ['mdb_color', 'bootstrap_color', 'darktheme_color', 'palette_colors']

def mdb_color(color, dark):
    allowed_colors = ('default', 'primary', 'secondary')
    allowed_dark = (True, False)

    assert color in allowed_colors, 'color unknown'
    assert dark in allowed_dark, 'either True or False'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            to_add = f'{color}-color' if not dark else f'{color}-color-dark'
            return wrapper_common(func, 'klass', to_add, *args, **kwargs)

        return wrapper
    return decorator

def bootstrap_color(color, dark):
    allowed_colors = ('danger', 'warning', 'success', 'info')
    allowed_dark = (True, False)

    assert color in allowed_colors, 'unknown color'
    assert dark in allowed_dark, 'either True or False'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            to_add = f'{color}-color' if not dark else f'{color}-color-dark'
            return wrapper_common(func, 'klass', to_add, *args, **kwargs)

        return wrapper
    return decorator

def darktheme_color(color, dark):
    allowed_colors = ('elegant', 'stylish', 'unique', 'special')
    allowed_dark = (True, False)

    assert color in allowed_colors, 'unknown color'
    assert dark in allowed_dark, 'either True or False'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            to_add = f'{color}-color-dark' if dark else f'{color}-color'
            return wrapper_common(func, 'klass', to_add, *args, **kwargs)

        return wrapper
    return decorator

def palette_colors(color, mode, lvl):
    allowed_colors = ('red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue',
                      'light-blue', 'cyan', 'teal', 'green', 'light-green', 'lime',
                      'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey',
                      'blue-grey', 'mdb-color')
    allowed_modes = (None, 'lighten', 'darken', 'accent') #some colors might not have those defined so check it before using

    assert color in allowed_colors, 'unknown color'
    assert mode in allowed_modes, 'unknown mode'
    if mode is 'lighten':
        assert 1 <= lvl <= 5, 'lighten mode accepts [1,5]'
    if mode == 'darken' or mode == 'accent':
        assert 1 <= lvl <= 4, 'darken and accent modes accept [1,4]'

    def none_mode_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return wrapper_common(func, 'klass', f'{color}', *args, **kwargs)

        return wrapper

    def with_mode_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            to_add = f'{color} {mode}-{lvl}'
            return wrapper_common(func, 'klass', to_add, *args, **kwargs)

        return wrapper

    if mode is None:
        return none_mode_decorator
    return with_mode_decorator

