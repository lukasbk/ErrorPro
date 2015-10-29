import numpy as np
from itertools import zip_longest
from units import convert_to_unit
from sympy import S
from quantities import adjust_to_unit

# TODO actually scientific notation should be used somehow

# format quantity for output
def format_quantity(q, unit_system, rounding):
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
            # round if possible and wanted
            if rounding and not (value is None or uncert is None):
                v, u = round_accordingly(value[i], uncert[i])
            # don't round
            else:
                v = "%.8f" % value[i] if value is not None else ""
                u = "%.8f" % uncert[i] if uncert is not None else ""
            value_str.append(v)
            uncert_str.append(u)

    # if it's a single value
    else:
        # round if possible and wanted
        if rounding and not (value is None or uncert is None):
            value_str, uncert_str = round_accordingly(value, uncert)
        # don't round
        else:
            value_str = "%.8f" % value if value is not None else ""
            uncert_str = "%.8f" % uncert if uncert is not None else ""

    # create unit string
    if unit == S.One:
        unit = ""
    else:
        unit = str(unit)

    return (description, value_str, uncert_str, unit)



# round value and uncertainty according to uncertainty
def round_accordingly(value, uncertainty):

    if uncertainty == 0:
        return (str(value), str(uncertainty))

    uFirstDigitPos=np.floor(np.log10(uncertainty))
    uFirstDigit=np.floor(uncertainty*10**(-uFirstDigitPos))
    if uFirstDigit<3:
        precision=np.int_(uFirstDigitPos-1)
    else:
        precision=np.int_(uFirstDigitPos)

    uCeiled=np.ceil(uncertainty*10**(-precision))/10**(-precision)
    # TODO np.round rounds down at exactly 0.5, not up!!
    vRounded=np.round(value,-precision)

    if precision>=0:
        viewPrecision="0"
    else:
        viewPrecision=str(-precision)
    value_str = ("{v:."+viewPrecision+"f}").format(v=vRounded)
    uncert_str = ("{u:."+viewPrecision+"f}").format(u=uCeiled)
    return (value_str, uncert_str)



class Output:
    def __init__(self):
        self._files = []
        self._used_filenames = []


    def addFile(self, filename, content):
        self._files.append((filename, content))

    def save(self, data, config):

        unit_system = __import__(config["unit_system"]).system

        # if activated, create automatic csv-file of results
        # TODO use order from commands, not random order like it's now
        if config["auto_results"]:

            content = [[],[],[],[],[],[],[]]
            content_str = ""
            single_counter = 0
            set_counter = 0
            # iterate quantities
            for q_name in data:
                q = data[q_name]

                description, value, uncert, unit = format_quantity(q, unit_system, config["rounding"])

                # if it's a data set
                if isinstance(value, list):
                    content[5].append(description + " [" + unit + "]")
                    content[6].append("")
                    for i in range(0,len(value)):
                        content[5].append(value[i])
                        content[6].append(uncert[i])
                    content[5].append("")
                    content[6].append("")
                # if it's single data
                else:
                    content[0].append(description)
                    content[1].append(value)
                    content[2].append(uncert)
                    content[3].append(unit)

            # transpose array
            content = zip_longest(*content, fillvalue="")

            # create string
            line_strs = []
            for line in content:
                line_strs.append(",".join(line))
            content_str = "\n".join(line_strs)

            # save to file
            self._make_file(config["auto_results"], content_str, config["directory"])

        # save all registered files
        for filename, content in self._files:
            self._make_file(filename, content, config["directory"])

    def _make_file(self, filename, content, directory):
        # if filename already used, add number
        ext_filename = filename
        i = 2
        while ext_filename in self._used_filenames:
            filename_arr = filename.partition(".")
            ext_filename = filename_arr[0] + "_" + i + filename_arr[1] + filename_arr[2]
            i += 1
        self._used_filenames.append(ext_filename)

        # write contents to file
        f = open(directory +"/"+ ext_filename,"w+")
        f.write(content)
        f.close()
