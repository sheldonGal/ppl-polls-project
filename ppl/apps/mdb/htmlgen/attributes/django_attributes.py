class Djattrs:
    """
    Container for so called "django attributes".
    It is recommended that when working with this class, attempt to use the `update` method's logic (cuase its cool).
    """
    def __init__(self, *args):
        """
        Optional initial arguments will be added via `update` method.
        :param args:
        """
        self.line = list()
        if args:
            self.update(*args)

    def update(self, *args):
        """
        Supports the following argument syntax::

           :param args: is iterated over, when faced with a ``decorate syntax`` all arguments
           that follow will now be decorated by this ``decorate syntax`` until it replaced.
           Default is ``plain text decoration`` i.e., `asis` insert.

           For double quotes wrapped arguments - `dqs_`, `dq_`, `"_"`
           For ``{{ var }}`` wrapped arguments -  `vars_`, `var_`, `{{ _ }}`, `{{_}}`
           For default variables, i.e., asis - `text_`, `txt_`, `_`


        :return: None
        """
        appender = self.text
        add = list()
        for arg in args:
            if arg in ('dqs_', 'dq_', '"_"', 'vars_', 'var_', '{{ _ }}', '{{_}}', 'text_', 'txt_', '_') and add:
                appender(*add)
                add.clear()
            if arg in ('dqs_', 'dq_', '"_"'):
                appender = self.dquote
            elif arg in ('vars_', 'var_', '{{ _ }}', '{{_}}'):
                appender = self.vars
            elif arg in ('text_', 'txt_', '_'):
                appender = self.text
            else:
                add.append(arg)
        if add:
            appender(*add)


    def dquote(self, *args):
        """wraps each argument in double quotes"""
        assert args, 'must supply atleast one argument'
        self.line.append(' '.join([f'"{arg}"' for arg in args]))
        return self

    def vars(self, *args):
        """wraps each argument with {{ }}"""
        assert args, 'must supply atleast one argument'
        self.line.append(' '.join([f'{{{{ {arg} }}}}' for arg in args]))
        return self

    def text(self, *args):
        """keeps arguments as is"""
        assert args, 'must supply at least one argument'
        for arg in args:
            self.line.append(arg)
        return self

    def reset(self, text = ''):
        """replace or initialize this attribute class data."""
        if not text:
            self.line = list()
        else:
            self.line = [text]
        return self

    def __repr__(self):
        """str representation"""
        return ' '.join(self.line)

