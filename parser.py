from pypeg2 import *
import re

class Unit(str):
    grammar = contiguous( "[",re.compile(r"[^\]]+"), "]" )

class Error(str):
    grammar = contiguous( "<",re.compile(r"[^>]+"), ">" )

class Comment(str):
    grammar = "#", restline, endl

class Command(str):
    grammar = "$", restline, endl

class PythonCode(str):
    grammar = ">", restline, endl

class SingleAssignment():
    grammar = name(), "=", attr("value",re.compile(r"[^\[<]+")), optional(attr("error", Error)), optional(attr("unit", Unit)), endl

class MultiAssignmentSpec():
    grammar = name(), optional(attr("error", Error)), optional(attr("unit", Unit))

class MultiAssignmentHeader(List):
    grammar = contiguous(csl(MultiAssignmentSpec, separator=omit(re.compile(r"[^\S\r\n]+"))))

class MultiAssignmentEntry(str):
    grammar = re.compile(r"[^}\s]+")

class MultiAssignmentRow(List):
    grammar = contiguous(csl(MultiAssignmentEntry, separator=omit(re.compile(r"[^\S\r\n]+"))))

class MultiAssignment(List):
    grammar = "{", attr("header",MultiAssignmentHeader), some(MultiAssignmentRow), "}"

class Program(List):
	grammar = maybe_some([Comment, SingleAssignment, MultiAssignment, Command])


def parse_file(fileHandle):
	syntaxTree = parse(fileHandle,Program)
	return syntaxTree
