from parsing.generated import DatParser
from grako.buffering import Buffer
import re


IMPORT_RE = '^\s*import\s*\(\s*"(.*)"\s*\)\s*$'
EOL_COMMENTS_RE = "#.*?$"

def include_file(regexMatch):
    f = open(regexMatch.group(1))
    return f.read()

def parse(code):
    code = re.sub(IMPORT_RE, include_file, code, 0, re.MULTILINE)

    p = DatParser(
        whitespace=" \t",
        eol_comments_re=EOL_COMMENTS_RE
    )
    ast = p.parse(
        code,
        'program',
        parseinfo=True,
        semantics = DatSemantics()
    )
    return ast

class DatSemantics(object):
    def subformula(self, ast):
        if ast is None:
            return ast
        else:
            return ''.join(ast)

    def _default(self, ast):
        return ast
