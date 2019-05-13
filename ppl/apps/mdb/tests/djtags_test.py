from django.test import TestCase
from apps.mdb.htmlgen.htmldoc import DjHtmlDoc

class DjHtmlDoc_Tests(TestCase):
    def setUp(self):
        self.doc = DjHtmlDoc()

    def test_djpack_line(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        dj.line('cycle', 'arg1 arg2')
        self.assertEqual(str(doc), '{% cycle arg1 arg2 %}')

    def test_djpack_line_seporated_args(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        dj.line('cycle', 'arg1', 'arg2')
        self.assertEqual(str(doc), '{% cycle arg1 arg2 %}')

    def test_djpack_line_different_args(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        dj.line('cycle', 'dq_' , 'a', 'b', '_', 'c')
        self.assertEqual(str(doc), '{% cycle "a" "b" c %}')

    def test_djpack_csrf_token(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        dj.csrf_token()
        self.assertEqual(str(doc), '{% csrf_token %}')

    def test_djpack_text(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        dj.text('a','dq_', 'b')
        self.assertEqual(str(doc), 'a "b"')

    def test_djpack_block(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        with djw.block('content') as content:
            content.update('a', 'b')
            content.update('dq_', 'c')
            dj.line('cycle', 'a', 'b')
        self.assertEqual(
            str(doc),
            '{% block content a b "c" %}{% cycle a b %}{% endblock %}'
        )

    def test_djpack_for(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        with djw.for_('a', 'dq_', 'b'):
            pass
        self.assertEqual(str(doc), '{% for a "b" %}{% endfor %}')

    def test_djpack_if_full(self):
        doc, (dj, djw) = self.doc, self.doc.djpack.pack()
        with djw.for_('key, value in elems.items'):
            with djw.if_('cond1'):
                dj.text('do something 1')
                with djw.elif_('cond2'):
                    dj.text('do something 2')
                with djw.elif_('cond3'):
                    dj.text('do something 3')
                with djw.else_():
                    dj.text('do something 4')
        self.assertEqual(
            str(doc),
            '{% for key, value in elems.items %}' +
                '{% if cond1 %}' +
                    'do something 1' +
                '{% elif cond2 %}' +
                    'do something 2' +
                '{% elif cond3 %}' +
                    'do something 3' +
                '{% else %}' +
                    'do something 4' +
                '{% endif %}' +
            '{% endfor %}'
        )



