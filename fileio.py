import numpy as np
import sympy
import sympy.physics.units as u
import re

# SI - prefix
sipref = {'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3, 'h': 1e2, 'da': 1e1,'d': 1e-1, 'c': 1e-2, 'm': 1e-3, 'mu': 1e-6, 'n': 1e-9, 'p': 1e-12}

# locals to be able to parse 'N' as a variable (by default function)
slocals = { 'N': sympy.Symbol('N'), 'O': sympy.Symbol('O'), 'Q': sympy.Symbol('Q'), 'S': sympy.Symbol('S')}

# regex for tell numbers/units,names apart i.e. find stuff not part of numbers
nonum = "[a-df-zA-DF-Z]"

# map for parsing units
usubs = {k:v for k,v in u.__dict__.items() if isinstance(v, sympy.Expr) and v.has(u.Unit)}


def parse_unit(s):
    """
    parse string s containing units and multipliers
    returns (number, expr)
    """
    u = sympy.sympify(s, locals=slocals).subs(usubs).simplify()
    if not isinstance(u, sympy.Mul): return (1, u)
    n, u1 = u.as_two_terms()
    if isinstance(n, sympy.Number):
        return (float(n), u1)
    return (1, u)


def parse_head(head, phi, unit, mult, longname):
    """
    take name header (x1[1e3 m])
    make phi  map i->name
         mult map i->multiplier
         longname map name->long name
         unit map name->unit
    """
    names = head.split(',')
    for i in range(len(names)):
        name = names[i]
        ln = None   # long name
        u  = None   # unit
        m  = None   # multiplier

        # extract long name
        lns = re.findall('"[\w ]*"', name)
        if lns and len(lns[0]) > 2:
            name = name.replace(lns[0], "")
            ln = lns[0][1:-1]

        # extract unit specifiers
        uspecs = re.findall('\[.*\]', name)
        if uspecs and len(uspecs[0]) > 2:
            name = name.replace(uspecs[0], "")
            usp = uspecs[0][1:-1].split()
            if re.findall(nonum, usp[0]):
                u = usp[0]
                m = usp[1] if len(usp)>1 else None
            else:
                m = usp[0]
                u = usp[1] if len(usp)>1 else None

        # sort stuff found into structures
        name = name.strip()
        phi[i] = name
        if m:
            try:
                mult[i] = sipref[m] if m in sipref else float(m)
            except ValueError as e:
                print("Can not parse '%s' as a multiplier, ignoring it." % m)
                mult[i] = 1
        else:
            mult[i] = 1
        if u:
            mul, unit[0] = parse_unit(u)
            mult[i] *= mul
        if ln:
            longname[name] = ln


def fl_getline(fl):
    """
    Get next line from file
    delete parts after #
    delete whitespace at beginning if it is more than '\n'
    """
    line = fl.readline()
    if (not line) or line == '\n':
        return line
    line = line.lstrip()
    i = line.find('#')
    if i == 0:
        return fl_getline(fl)
    if i != -1:
        line = line[:i]
    return line


def parse_file(filename, save=False, data={}):
    """
    Read data from file into map of arrays
    execute embedded commands

    save=True: save equations and results to res.txt
    data (map name->data) can be given as set to add data to

    format for file
    # comment (line is ignored)
    {
      varnames[multip unit]
      varvalues
    }
    $ calculation
    > python code

    notes:
    - no whitespace between varname and []
    - if varname is used twice, second dataset overwrites last one

    return data(name->array), unit(name->unit), longname(name->str)
    """

    fl = open(filename, 'r')

    unit = {}       # in the end map name->unit
    longname = {}   # map name->full name

    line = fl_getline(fl)
    while line:
        # section containing data
        if line[0] == '{':
            phi  = {}   # map i->name
            mult = {}   # map i->multiplicator
            head = line.strip()[1:]
            line = fl_getline(fl)
            while not head:
                head = line.strip()
                line = fl_getline(fl)
            parse_head(head, phi, unit, mult, longname)
            # parse remaining lines (possibly) containing data
            dtlines = []
            while line:
                if line[-2] == '}':
                    if len(line)>2:
                        dtlines.append(np.fromstring(line[:-2], sep=' '))
                    break
                dtlines.append(np.fromstring(line, sep=' '))
                line = fl_getline(fl)
            dt = np.array(dtlines).transpose()
            if dt.ndim != 2:
                print("mismatching dimensions in dataset\n%s" % dt)
                raise ValueError('dimension mismatch')
            try:
                for i in range(len(dt)):
                    data[phi[i]] = dt[i] * mult[i]
            except IndexError as e:
                print("Too many elements for\n'%s'.\n%s" % (phi, e))

        # allowing the execution of arbitrary python code entered by the user
        # is possibly dangerous. This may be removed when more features are implemented
        if line[0] == '>':
            exec(line[1:].strip())

        line = fl_getline(fl)

    return (data, unit, longname) if longname else (data, unit)
