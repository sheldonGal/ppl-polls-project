from apps.mdb.htmlgen.packs import Hpack, DjPack



class DjHtmlDoc:
    def __init__(self):
        self.result = list()
        self.scripts = list()
        self.css = list()

        self._append = self.result.append
        self._base = None

        self.djpack = DjPack(self)
        self.hpack = Hpack(self)

    def pack(self):
        """
        document, djs, djc, hts, htc
        :return:
        """
        return self, self.djpack.simple, self.djpack.complex, self.hpack.simple, self.hpack.complex

    def extends(self, base_template = None):
        self._base = base_template

    def __repr__(self):
        return ''.join(self.result)

