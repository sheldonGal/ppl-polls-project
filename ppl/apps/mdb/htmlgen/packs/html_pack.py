from contextlib import contextmanager
from apps.mdb.htmlgen.attributes import Hattrs

__all__ = ['Hpack']



from apps.mdb.mdb_macros.css import text_color as icon_color


@contextmanager
def htag(doc, tag, *args, **kwargs):
    position = len(doc.result)
    doc._append('')
    attributes = Hattrs(*args, **kwargs)
    yield attributes
    if not attributes._attrs:
        doc.result[position] = f'<{tag}>'
    else:
        doc.result[position] = f'<{tag} {attributes}>'
    doc._append(f'</{tag}>')




class Hpack:
    def __init__(self, doc):
        self._doc = doc
        self.complex = self.__class__._with(self._doc)
        self.simple = self.__class__._no_with(self._doc)

    def pack(self):
        return self.simple, self.complex


    class _with:
        def __init__(self, doc):
            self._doc = doc

        def tag(self, tag, *args, **kwargs):
            return htag(self._doc, tag, *args, **kwargs)

    class _no_with:
        def __init__(self, doc):
            self._doc = doc

        def text(self, *args):
            assert args, 'must supply at least one arg'
            self._doc._append(' '.join(html_escape(arg) for arg in args))
        def sp_text(self, *args):
            assert args, 'must supply at least one arg'
            self.sp()
            self.text(*args)
        def nl_text(self, *args):
            assert args, 'must supply at least one arg'
            self.nl()
            self.text(*args)


        def nl(self, times = 1):
            self._doc._append('\n' * times)
        def tab(self, times = 1):
            self._doc._append('\t' * times)
        def sp(self, times = 1):
            self._doc._append(' ' * times)

        def nl_asis(self, *args):
            self.nl()
            self.asis(*args)
        def sp_asis(self, *args):
            self.sp()
            self.asis(*args)

        def asis(self, *args):
            self._doc._append(' '.join(args))

        def custom_stag(self, tag, stag_end, *args, **kwargs):
            self._doc._append(f'<{tag} {Hattrs(*args, **kwargs)}{stag_end}')

        def otag(self, tag, *args, **kwargs):
            self.custom_stag(tag, '>', *args, **kwargs)
        def sctag(self, tag, *args, **kwargs):
            self.custom_stag(tag, '/>', *args, **kwargs)

def html_escape(s):
    if isinstance(s,(int,float)):
        return str(s)
    try:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    except AttributeError:
        raise TypeError(
            "You can only insert a string, an int or a float inside a xml/html text node. "
            "Got %s (type %s) instead." % (repr(s), repr(type(s)))
        )