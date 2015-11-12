import numpy as np
from quantities import adjust_to_unit
from itertools import zip_longest
import csv
from sympy import S

def arrange_data(data, unit_system):
    # sort quantities by count
    sorted_data = sorted(data.values(), key=lambda q:q.count)

    # group by length
    data_by_length = {}
    for q in sorted_data:
        if isinstance(q.value, np.ndarray):
            length = len(q.value)
        else:
            length = 1
        if not length in data_by_length:
            data_by_length[length] = []
        data_by_length[length].append(q)

    # find largest amount of quantities with one length (except for length 1)
    max_quantities = 0
    for length in data_by_length:
        if not length == 1:
            if len(data_by_length[length]) > max_quantities:
                max_quantities = len(data_by_length[length])
    columns = [[] for x in range(5 + max_quantities*2)]

    # list single data on the left side
    if 1 in data_by_length:
        for q in data_by_length[1]:
            description, value, uncert, unit = format_quantity(q, unit_system)
            columns[0].append(description)
            columns[1].append(value)
            columns[2].append(uncert)
            columns[3].append(unit)

    # iterate data set length
    for length in data_by_length:
        if length == 1:
            continue
        q_counter = 0
        # iterate quantities of one length
        for q in data_by_length[length]:
            description, value, uncert, unit = format_quantity(q, unit_system)
            # list data sets on the right, grouped by length
            columns[5 + q_counter*2].append(description + " [" + unit + "]")
            columns[6 + q_counter*2].append("")
            for i in range(0,len(value)):
                columns[5 + q_counter*2].append(value[i])
                columns[6 + q_counter*2].append(uncert[i])
            columns[5 + q_counter*2].append("")
            columns[6 + q_counter*2].append("")
            q_counter += 1

        # fill rest of columns with empty space
        for c in range(6 + q_counter*2 + 1, len(columns)):
            columns[c].extend([""] * (length+1))

    # transpose array
    return zip_longest(*columns, fillvalue="")



def format_quantity(q, unit_system, rounding=False):

    # TODO rounding, ...

    description = q.name
    if q.longname:
        description = q.longname + " " + description

    # find unit
    value, uncert, unit = adjust_to_unit(q, unit_system)

    # if it's a data set
    if isinstance(value, np.ndarray):
        value_str = []
        uncert_str = []
        for i in range(0,len(value)):
            v = "%.8f" % value[i] if value is not None else ""

            u = "%.8f" % uncert[i] if uncert is not None else ""
            value_str.append(v)
            uncert_str.append(u)

    # if it's a single value
    else:
        value_str = "%.8f" % value if value is not None else ""
        uncert_str = "%.8f" % uncert if uncert is not None else ""

    # create unit string
    if unit == S.One:
        unit = ""
    else:
        unit = str(unit)

    return (description, value_str, uncert_str, unit)


class Output():
    def __init__(self):
        self.plotfiles = []
        self.latex_codes = []

    def addLatexCode(self, code):
        self.latex_codes.append(code)

    def addPlotFiles(self, files_obj):
        self.plotfiles.append(files_obj)

    def generate(self, data, config):
        # save latex code to file
        # TODO

        # save plots and their source files
        i = 1
        for f_obj in self.plotfiles:
            f_obj.save("plot"+str(i)+"_", config["directory"])
            i += 1

        # automatic csv file
        unit_system = __import__(config["unit_system"]).system
        with open(config["directory"] +"/"+ config["auto_results"],"w") as f:
            writer = csv.writer(f, lineterminator='\n')
            for line in arrange_data(data, unit_system):
                writer.writerow( line )


class Files():
    """
    class to flexibly save files like gnuplot or matplotlib plots
    """
    def save(self, prefix, directory):
        pass
