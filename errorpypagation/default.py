from errorpypagation.project import Project
from IPython.core.magic import register_cell_magic
import pydoc

p = Project()

def wrappedHelpText (wrappedFunc):
    def decorator (f):
         f.__doc__ = 'This method wraps the following method:\n\n' + pydoc.text.document(wrappedFunc)
         return f
    return decorator

@register_cell_magic
def calc(line, cell):
    p.calc(cell)

@wrappedHelpText(p.save)
def save(*args, **kwargs):
    return p.save(*args, **kwargs)

@wrappedHelpText(p.set)
def set(*args, **kwargs):
    return p.set(*args, **kwargs)

@wrappedHelpText(p.load)
def load(*args, **kwargs):
    return p.load(*args, **kwargs)

@wrappedHelpText(p.table)
def table(*args, **kwargs):
    return p.table(*args, **kwargs)

@wrappedHelpText(p.formula)
def formula(*args, **kwargs):
    return p.formula(*args, **kwargs)

@wrappedHelpText(p.mean_value)
def mean_value(*args, **kwargs):
    return p.mean_value(*args, **kwargs)

@wrappedHelpText(p.plot)
def plot(*args, **kwargs):
    return p.plot(*args, **kwargs)

@wrappedHelpText(p.fit)
def fit(*args, **kwargs):
    return p.fit(*args, **kwargs)

@wrappedHelpText(p.assign)
def assign(*args, **kwargs):
    return p.assign(*args, **kwargs)
