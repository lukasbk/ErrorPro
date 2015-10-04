import numpy as np
import sympy
import quantities as q
import re

# regex for tell numbers/units,names apart i.e. find stuff not part of numbers
nonum = "[a-df-zA-DF-Z]"

def parse_head(head, phi, unit, longname):
    """
    take name header (x1[1e3 m])
    make phi  map i->name
         longname map name->long name
         unit map name->unit
    """
    names = head.split(',')
    for i in range(len(names)):
        name = names[i]
        ln = None   # long name
        u  = None   # unit

        # extract long name
        lns = re.findall('"[\w ]*"', name)
        if lns and len(lns[0]) > 2:
            name = name.replace(lns[0], "")
            ln = lns[0][1:-1]

        # extract unit specifiers
        uspecs = re.findall('\[.*\]', name)
        if uspecs and len(uspecs[0]) > 2:
            name = name.replace(uspecs[0], "")
            u = uspecs[0][1:-1]

        # sort stuff found into structures
        name = name.strip()
        phi[i] = name
        if u:
            unit[name]=u
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
      varnames[multip*unit]
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

    data_stack = {} # stack for data where error or value are still missing
    unit = {}           # in the end map name->unit
    longname = {}       # map name->full name

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
            parse_head(head, phi, unit, longname)
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
                    #if error data is added to value data
                    if (phi[i][-4:] == "_err" and phi[i][:-4] in data_stack):
                        n = phi[i][:-4]
                        ln = longname[n] if n in longname else ""
                        v = data_stack[n]
                        e = dt[i]
                        u = unit[phi[i]] if phi[i] in unit else ""
                        data[n]=q.Measurement(n, ln, v, e, unit[n], u)
                    #if value data is added to error data
                    elif phi[i]+"_err" in data:
                        n = phi[i]
                        ln = longname[n] if n in longname else ""
                        v = dt[i]
                        e = data_stack[n+"_err"]
                        u = unit[phi[i]] if phi[i] in unit else ""
                        data[n]=q.Measurement(n, ln, v, e, u, unit[n+"_err"])
                    #if one is still missing
                    else:
                        data_stack[phi[i]] = dt[i]

            except IndexError as e:
                print("Too many elements for\n'%s'.\n%s" % (phi, e))

        elif line[:2] == '$ ':
            l_arr=line.split("=")
            if not len(l_arr) == 2:
                raise SyntaxError("bad syntax in calculation\n%s" % line)

            name = l_arr[0][1:]
            assignment = l_arr[1]

            u = None
            ln = ""   # long name

            # extract long name
            lns = re.findall('"[\w ]*"', name)
            if lns and len(lns[0]) > 2:
                name = name.replace(lns[0], "")
                ln = lns[0][1:-1]

            # extract unit specifiers
            uspecs = re.findall('\[.*\]', assignment)
            if uspecs and len(uspecs[0]) > 2:
                assignment = assignment.replace(uspecs[0], "")
                u = uspecs[0][1:-1]


            # sort stuff found into structures
            name = name.strip()

            data[name] = q.Result(name, ln, assignment, u, data)

         # allowing the execution of arbitrary python code entered by the user
         # is possibly dangerous. This may be removed when more features are implemented
        elif line[0] == '>':
            exec(line[1:].strip())

        line = fl_getline(fl)

    return data
