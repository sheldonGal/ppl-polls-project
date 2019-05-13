class Hattrs:
    """
    Used as a container for `html` attributes.
    For example:
    .. code-block:: html

       <div class="container md-5" required>...

    `Hattrs` is responsible for rendering aswell.
    """
    def __init__(self, *args, **kwargs):
        """
        Optional arguments allow initial attributes to be set
        """
        self._attrs = dict()
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        """
        Updates this container with newly given attributes.
        For example:

        .. code-block:: python

           update('required', klass='container')

        will result in the following attributes:

        .. code-block:: html

           class="container" required

        :return: None
        """
        args = args or ()
        kwargs = kwargs or {}
        for key, value in kwargs.items():
            key = key.replace('_', '-')
            if key == 'klass':
                key = 'class'
            self.add(key, value)
        for arg in args:
            self.add(arg)


    def add(self, key, *values):
        """
        Add additional `key:value` pairs.
        For the given :param key: add all :param values: as attributes.
        :return: self, for easy multi-use
        """
        if key not in self._attrs:
            self._attrs[key] = list()
        for val in values:
            if val not in self._attrs[key]:
                self._attrs[key].append(val)
        return self


    def __repr__(self):
        """
        Renders the attributes as they will appear in their `html` form.
        :return: str, `html` form.
        """
        def asattr(key, values):
            if values:
                return f'{key}="{values}"'
            return f'{key}'
        def get(key):
            if key not in self._attrs:
                raise KeyError('key doesnt exist')
            return ' '.join(self._attrs[key])
        return ' '.join([asattr(key, get(key)) for key in self._attrs.keys()])

