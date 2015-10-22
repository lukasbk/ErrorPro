from pypeg2 import *
import re

class Unit(str):
    grammar = contiguous( "[",re.compile(r"[^\]]+"), "]" )

class Uncertainty(str):
    grammar = contiguous( "<",re.compile(r"[^>]+"), ">" )

class Function(str):
    type = "Function"
    grammar = "$", name(), restline, endl

class PythonCode(str):
    type = "PythonCode"
    grammar = ">", restline, endl

class SingleAssignment():
    type = "SingleAssignment"
    grammar = name(), "=", attr("value",re.compile(r"[^\[{<]+")), optional(attr("uncertainty", Uncertainty)), optional(attr("unit", Unit)), endl

class MultiAssignmentSpec():
    grammar = name(), optional(attr("uncertainty", Uncertainty)), optional(attr("unit", Unit))

class MultiAssignmentHeader(List):
    grammar = contiguous(csl(MultiAssignmentSpec, separator=omit(re.compile(r"[^\S\r\n]+"))))

class MultiAssignmentEntry(str):
    grammar = re.compile(r"[^}\s]+")

class MultiAssignmentRow(List):
    grammar = contiguous(csl(MultiAssignmentEntry, separator=omit(re.compile(r"[^\S\r\n]+"))))

class MultiAssignment(List):
    type = "MultiAssignment"
    grammar = "{", attr("header",MultiAssignmentHeader), some(MultiAssignmentRow), "}"

class Program(List):
    grammar = maybe_some([SingleAssignment, MultiAssignment, Function, PythonCode])


def parse_file(fileHandle):
    code = fileHandle.read()
    code = re.sub("#.*$", "", code, 0, re.MULTILINE) # remove comments
    syntaxTree = parse(code,Program)
    return syntaxTree
