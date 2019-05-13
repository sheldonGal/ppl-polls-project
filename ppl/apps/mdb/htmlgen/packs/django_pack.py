from contextlib import contextmanager
from apps.mdb.htmlgen.attributes import Djattrs

__all__ = ['DjPack']

djopen = '{%'
djclose = '%}'

@contextmanager
def djtag(doc, attributes, tag, close_cmd = ''):
    """
    Context manager, allows the use with the ``with`` statement.

    .. code-block:: python

       with djtag(...) as attrs:
           pass

    Where ``attrs`` is the attributes of this specific django tag.
    :param doc:
    :param attributes:
    :param tag:
    :param close_cmd:
    :return: TODO - add attributes
    """
    position = len(doc.result)
    doc._append('')

    yield attributes

    if not attributes.line:
        doc.result[position] = f'{djopen} {tag} {djclose}'
    else:
        doc.result[position] = f'{djopen} {tag} {attributes} {djclose}'
    if close_cmd:
        doc._append(f'{djopen} {close_cmd} {djclose}')


class DjPack:
    def __init__(self, doc):
        """
        Constructs a ``DjPack`` instance.
        :param doc: an instance of ``DjHtmlDoc``
        """
        self._doc = doc
        self.complex = self.__class__._with(self._doc)
        self.simple = self.__class__._nowith(self._doc)

    def pack(self):
        """
        Inspired by ``yattag``, supplies the user with two packs; a simple and a complex one.
        The complex pack contains methods that return a context manager.
        :return: simple, complex
        """
        return self.simple, self.complex

    class _nowith:
        """
        Simple methods, i.e., not context managers
        """
        def __init__(self, doc):
            """
            :param doc: instance of ``DjHtmlDoc``
            """
            self._doc = doc

        def line(self, tag, *args):
            """
            Appends to the ``Djattrs`` all args in a single line.
            """
            self._doc._append(f'{djopen} {tag} {Djattrs(*args)} {djclose}')

        def csrf_token(self):
            """
            {% csrf_token %}
            """
            self._doc._append('{% csrf_token %}')

        def text(self, *args):
            """
            Appends the args to the document by the ``Djattrs`` constructor.
            :param args:
            :return:
            """
            self._doc._append(str(Djattrs(*args)))


    class _with:
        def __init__(self, doc):
            self._doc = doc

        def tag(self, tag, text):
            return djtag(self._doc, Djattrs(text), tag, close_cmd = f'end{tag}')

        def block(self, name):
            return djtag(self._doc, Djattrs(name), 'block', close_cmd = 'endblock')

        def for_(self, *args):
            return djtag(self._doc, Djattrs(*args), 'for', close_cmd = 'endfor')

        def if_(self, *args):
            return djtag(self._doc, Djattrs(*args), 'if', close_cmd = 'endif')

        def elif_(self, *args):
            return djtag(self._doc, Djattrs(*args), 'elif')

        def else_(self):
            return djtag(self._doc, Djattrs(), 'else')
