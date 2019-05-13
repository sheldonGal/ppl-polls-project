from functools import wraps
from apps.mdb.mdb_macros.utils import wrapper_common
from apps.mdb.mdb_macros.css import text_color as icon_color
from apps.mdb.mdb_macros.utilities import margin

def icon_size(size):
    allowed_sizes = (
        'xs', 'sm', 'lg', 2,3,4,5,6,7,8,9,10
    )
    assert size in allowed_sizes, 'unknown size has been given'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            to_add = f'fa-{size}x' if type(size) is int else f'fa-{size}'
            return wrapper_common(func, 'klass', to_add, *args, **kwargs)

        return wrapper
    return decorator


from apps.mdb.htmlgen import DjHtmlDoc

@margin('m','l',2)
@icon_color('red')
@icon_size(3)
def icon(icon, *args, **kwargs):
    doc, djs, djc, hts, htc = DjHtmlDoc().pack()
    with htc.tag('div', *args, **kwargs):
        pass
    print(str(doc))
    print(kwargs)
icon('a')