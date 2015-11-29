from errorpro.project import Project
from IPython.core.magic import register_cell_magic
import pydoc

default_project = Project()

def wrappedHelpText (wrappedFunc):
    def decorator (f):
         f.__doc__ = 'This method wraps the following method:\n\n' + pydoc.text.document(wrappedFunc)
         return f
    return decorator

@register_cell_magic
def calc(line, cell):
    default_project.calc(cell)

@wrappedHelpText(default_project.save)
def save(*args, **kwargs):
    return default_project.save(*args, **kwargs)

@wrappedHelpText(default_project.set)
def set(*args, **kwargs):
    return default_project.set(*args, **kwargs)

@wrappedHelpText(default_project.load)
def load(*args, **kwargs):
    return default_project.load(*args, **kwargs)

@wrappedHelpText(default_project.table)
def table(*args, **kwargs):
    return default_project.table(*args, **kwargs)

@wrappedHelpText(default_project.formula)
def formula(*args, **kwargs):
    return default_project.formula(*args, **kwargs)

@wrappedHelpText(default_project.mean_value)
def mean_value(*args, **kwargs):
    return default_project.mean_value(*args, **kwargs)

@wrappedHelpText(default_project.plot)
def plot(*args, **kwargs):
    return default_project.plot(*args, **kwargs)

@wrappedHelpText(default_project.fit)
def fit(*args, **kwargs):
    return default_project.fit(*args, **kwargs)

@wrappedHelpText(default_project.assign)
def assign(*args, **kwargs):
    return default_project.assign(*args, **kwargs)
