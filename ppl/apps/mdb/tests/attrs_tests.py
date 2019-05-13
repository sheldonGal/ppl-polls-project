from django.test import TestCase
from apps.mdb.htmlgen.attributes import Hattrs, Djattrs

class Hattrs_add_method_Test(TestCase):
    """
    Tests for `Hattrs` class.
    """
    def test_add_simple(self):
        attrs = Hattrs()

        attrs\
            .add('class', 'container', 'md-2')\
            .add('required')
        self.assertEqual(
            str(attrs), 'class="container md-2" required'
        )

    def test_add_repeated_keys(self):
        attrs = Hattrs()

        attrs.add('class', 'class1')\
            .add('class', 'class2')\
            .add('class', 'class3')\
            .add('other', 'other1', 'other2', 'other3')
        self.assertEquals(
            str(attrs),
            'class="class1 class2 class3" other="other1 other2 other3"'
        )

    def test_add_repeated_values(self):
        attrs = Hattrs()

        attrs.add('class', 'class1', 'class2', 'class3')\
            .add('class', 'class2', 'class4')\
            .add('class', 'class3', 'class4', 'class5')\
            .add('class', 'class1','class2','class3','class4','class5')

        self.assertEqual(
            str(attrs),
            'class="class1 class2 class3 class4 class5"'
        )

class Hattrs_Update_Test(TestCase):
    """
    Tests the `update` method of `Hattrs` class.
    """
    def test_update_simple(self):
        attrs = Hattrs('required', klass='class1', other = 'other1')
        self.assertEqual(
            str(attrs),
            'class="class1" other="other1" required'
        )

    def test_update_with_add(self):
        attrs = Hattrs('required', klass='class1', other='other1')
        attrs.add('class', 'class1', 'class2')
        attrs.add('other', 'other1', 'other2')
        self.assertEqual(
            str(attrs),
            'class="class1 class2" other="other1 other2" required'
        )

    def test_update_with_add_required(self):
        attrs = Hattrs('required', klass='class1')
        attrs.add('required')
        self.assertEqual(str(attrs), 'class="class1" required')

    def test_update_with_add_required_overriding(self):
        attrs = Hattrs('required', klass='class1')
        attrs.add('required', 'req1')
        self.assertEqual(str(attrs), 'class="class1" required="req1"')

class DjattrsTest(TestCase):
    def test_dquote(self):
        attrs = Djattrs()
        attrs.dquote('arg1')
        self.assertEqual(str(attrs), '"arg1"')

    def test_dquote_multiple(self):
        attrs = Djattrs()
        attrs.dquote('arg1', 'arg2')\
            .dquote('arg3')\
            .dquote('arg4', 'arg5')
        self.assertEqual(
            str(attrs),
            '"arg1" "arg2" "arg3" "arg4" "arg5"'
        )

    def test_args_single(self):
        attrs = Djattrs()
        attrs.vars('arg1')
        self.assertEqual(
            str(attrs),
            '{{ arg1 }}'
        )

    def test_arg_multiple(self):
        attrs = Djattrs()
        attrs.vars('arg1', 'arg2', 'arg3')
        self.assertEqual(
            str(attrs),
            '{{ arg1 }} {{ arg2 }} {{ arg3 }}'
        )

    def test_text_single(self):
        attrs = Djattrs()
        attrs.text('text one')
        self.assertEqual(
            str(attrs),
            'text one'
        )

    def test_text_multiple(self):
        attrs = Djattrs()
        attrs.text('text one', 'text two')\
            .text('text three')
        self.assertEqual(
            str(attrs),
            'text one text two text three'
        )

    def test_reset_simple(self):
        attrs = Djattrs()
        attrs.text('text one', 'text two', 'text three')
        self.assertEqual(str(attrs), 'text one text two text three')
        attrs.reset('reseted text')
        self.assertEqual(str(attrs), 'reseted text')

    def test_reset_complex(self):
        attrs = Djattrs()
        attrs.dquote('dquote1', 'dquote2')\
            .vars('arg1', 'arg2')\
            .text('text1', 'text2')
        self.assertEquals(
            str(attrs), '"dquote1" "dquote2" {{ arg1 }} {{ arg2 }} text1 text2'
        )

        attrs.reset()

        self.assertEqual( str(attrs), '')
        attrs.dquote('dquote1', 'dquote2') \
            .vars('arg1', 'arg2') \
            .text('text1', 'text2')
        self.assertEquals(
            str(attrs), '"dquote1" "dquote2" {{ arg1 }} {{ arg2 }} text1 text2'
        )

        attrs.reset('new start')
        attrs.dquote('dquote1', 'dquote2') \
            .vars('arg1', 'arg2') \
            .text('text1', 'text2')
        self.assertEquals(
            str(attrs), 'new start "dquote1" "dquote2" {{ arg1 }} {{ arg2 }} text1 text2'
        )

    def test_constructor_simple(self):
        attrs = Djattrs('a', 'b', 'c')
        self.assertEqual(str(attrs), 'a b c')

    def test_constructor_text_prefix_simple(self):
        attrs = Djattrs('_', 'a','b','c')
        self.assertEquals(str(attrs), 'a b c')

    def test_constructor_text_prefix_complex(self):
        attrs = Djattrs('_', 'a', 'b', 'text_', 'c', 'd', 'txt_', 'e', 'f', '_', 'g')
        self.assertEqual(str(attrs), 'a b c d e f g')

    def test_constructor_dq_prefix_simple(self):
        attrs = Djattrs('"_"', 'a', 'b', 'c')
        self.assertEqual(str(attrs), '"a" "b" "c"')

    def test_constructor_dq_prefix_complex(self):
        attrs = Djattrs('dq_', 'a', 'b', 'dq_', 'dqs_', 'c', '"_"', 'd')
        self.assertEqual(str(attrs), '"a" "b" "c" "d"')

    def test_constructor_vars_prefix_simple(self):
        attrs = Djattrs('{{ _ }}', 'a','b')
        self.assertEqual(str(attrs), '{{ a }} {{ b }}')

    def test_constructor_vars_prefix_complex(self):
        attrs = Djattrs('var_', 'a', 'vars_', 'vars_', 'vars_', 'b', '{{_}}', 'c')
        self.assertEqual(str(attrs), '{{ a }} {{ b }} {{ c }}')

    def test_constructor_complex(self):
        attrs = Djattrs('a', 'b', 'dq_', 'c', 'var_', 'd')
        self.assertEqual(str(attrs), 'a b "c" {{ d }}')





