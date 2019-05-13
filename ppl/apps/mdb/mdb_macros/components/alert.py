from functools import wraps
from apps.mdb.mdb_macros.utils import wrapper_common

def alert_type(atype):
    allowed_types = ('primary', 'secondary', 'success','danger', 'warning', 'info', 'light', 'dark')

    assert atype in allowed_types, 'unknown alert type'

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            to_add = f'alert alert-{atype}'
            return wrapper_common( # changed both 'role' and 'klass'
                wrapper_common, 'role', 'alert',
                func, 'klass', to_add, *args, **kwargs
            )
        return wrapper
    return decorator

def dismissable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return wrapper_common(func, 'klass', 'alert-dismissible fade show', *args, **kwargs)
    return wrapper

from apps.mdb.htmlgen import DjHtmlDoc

@alert_type('warning')
@dismissable
def alert(doc, func_message, *args, **kwargs):
    doc, djs, djc, hts, htc = doc.pack()
    with htc.tag('div', *args, **kwargs):
        func_message(doc)
        with htc.tag('button', type='button', klass='close', data_dismiss='alert', aria_label='Close'):
            with htc.tag('span', aria_hidden = 'true'):
                hts.asis('&times;')

    print(str(doc))

def message(doc):
    doc, djs, djc, hts, htc = doc.pack()
    with htc.tag('strong'):
        hts.text('Holy guacamole!')
    hts.sp_text('you should check in on some of those fields below.')
a = DjHtmlDoc()
alert(a, message)
alert(a, message)