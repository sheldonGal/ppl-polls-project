from functools import wraps

__all__ = ['wrapper_common', 'klass']

def wrapper_common(func, key, to_add, *args, **kwargs):
    curr = kwargs.pop(key, '')
    if curr:
        curr += ' '
    kwargs[key] = curr + to_add
    return func(*args, **kwargs)



def klass(name):
    assert type(name) is str

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return wrapper_common(func, 'klass', name, *args, **kwargs)

        return wrapper

    return decorator

