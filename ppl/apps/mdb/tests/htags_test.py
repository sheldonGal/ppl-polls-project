from django.test import TestCase
from apps.mdb.htmlgen.htmldoc import DjHtmlDoc

class HpackTests(TestCase):
    def setUp(self):
        self.doc = DjHtmlDoc()

    def test_hpack_tag_no_attrs(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        with htc.tag('div'):
            pass
        self.assertEqual(str(doc), '<div></div>')

    def test_hpack_tag_with_arg_attrs(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        with htc.tag('div', 'required', klass = 'container', other = 'other'):
            pass
        self.assertEqual(
            str(doc),
            '<div class="container" other="other" required></div>'
        )

    def test_hpack_tag_with_inner_attrs(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        with htc.tag('div') as divattrs:
            divattrs.update('required', klass='container', other='other')
        self.assertEqual(
            str(doc),
            '<div class="container" other="other" required></div>'
        )

    def test_hpack_tag_with_arg_and_inner_attrs(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        with htc.tag('div', 'required', klass='container') as divattrs:
            divattrs.update(klass='md-5', other='other')
        self.assertEqual(
            str(doc),
            '<div class="container md-5" required other="other"></div>'
        )

    def test_hpack_tag_nesting(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        with htc.tag('div') as _:
            with htc.tag('div', klass='container') as _1:
                pass
            with htc.tag('div', klass='container') as _2:
                _.update(added='added in child _2')
                _2.update('required')
                with htc.tag('div'):
                    pass
        self.assertEqual(
            str(doc),
            '<div added="added in child _2">' +
                '<div class="container">' +
                '</div>' +
                '<div class="container" required>'+
                    '<div></div>'+
                '</div>'+
            '</div>'
        )

    def test_hpack_text(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        hts.text('1 < 2', '2 < 3')
        self.assertEqual(str(doc), '1 &lt; 2 2 &lt; 3')
        a = 1
        b = 2
        hts.sp_text(a, '<', b)
        self.assertEqual(str(doc), '1 &lt; 2 2 &lt; 3 1 &lt; 2')

    def test_hpack_asis(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        hts.asis('1 < 2', '1 < 3')
        hts.sp_asis('4','5')
        self.assertEqual(str(doc), '1 < 2 1 < 3 4 5')

    def test_hpack_otag(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        hts.otag('tag_name', 'required', klass='someclass')
        self.assertEqual(str(doc), '<tag_name class="someclass" required>')

    def test_hpack_sctag(self):
        doc, djs, djc, hts, htc = self.doc.pack()
        hts.sctag('tag_name', 'required', klass='someclass')
        self.assertEqual(str(doc), '<tag_name class="someclass" required/>')


