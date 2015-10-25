from parsing.generated import DatParser

def parse(code):
    p = DatParser(
        whitespace=" \t",
        eol_comments_re="#.*?$"
    )
    ast = p.parse(
        code,
        'program',
        parseinfo=True,
        semantics = DatSemantics()
    )
    return ast

class DatSemantics(object):
    def formula(self, ast):
        if ast is None:
            return ast
        else:
            return ''.join(ast)

    def _default(self, ast):
        return ast
