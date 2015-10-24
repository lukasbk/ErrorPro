import shlex, subprocess
from PIL import Image

def plot(data_sets, functions, show=True, x_label="", y_label=""):
    plotfile = 'tmp/gnuplot.plt'
    outputfile = 'tmp/gnuplot.png'
    datafile_beg = 'tmp/data'

    # code for gnuplot.plt
    code = r'''
reset
set term pngcairo enhanced
set output '%(output)s'
%(x_label)s
%(y_label)s
%(var_defs)s
%(functions)s
%(plot)s
'''
    var_defs_str = ""
    functions_str = ""
    plot_str = "plot "
    first_plot = True

    # labels
    if x_label:
        x_label = "set xlabel '"+x_label+"'"
    if y_label:
        y_label = "set ylabel '"+y_label+"'"

    # plot functions
    function_counter = 0
    for f in functions:
        # save all values to gnuplot variables
        fname = "f"+str(function_counter)
        for var in f["term"].free_symbols:
            if not var == f["x"]:
                var_defs_str += var.name + " = " + str(var.value) + "\n"

        # save functions
        functions_str += fname+"("+f["x"].name+")"+" = " + str(f["term"]) + "\n"

        # save plot commands
        if not first_plot:
            plot_str+=", "
        plot_str += fname+"(x)"

        # add title
        if f["title"]:
            plot_str += " title '"+f["title"]+"'"

        first_plot = False
        function_counter += 1

    data_set_counter = 0
    for data_set in data_sets:

        # create data-string
        data = ""
        for line in range(0,len(data_set["x_values"])):
            data += str(data_set["x_values"][line]) + " "
            data += str(data_set["y_values"][line]) + " "
            if not data_set["x_uncerts"] is None:
                data += str(data_set["x_uncerts"][line]) + " "
            if not data_set["y_uncerts"] is None:
                data += str(data_set["y_uncerts"][line]) + " "
            data += "\n"

        # write to file
        datafile = datafile_beg + str(data_set_counter)
        with open(datafile,'w') as handle:
            handle.write(data)

        # save plot commands
        if not first_plot:
            plot_str+=", "
        plot_str += "'" + datafile +"'"
        if not data_set["x_uncerts"] is None and not data_set["y_uncerts"] is None:
            plot_str += " with xyerrorbars"
        elif not data_set["x_uncerts"] is None:
            plot_str += " with xerrorbars"
        elif not data_set["y_uncerts"] is None:
            plot_str += " with yerrorbars"

        # add title
        if data_set["title"]:
            plot_str += " title '"+data_set["title"]+"'"

        first_plot = False
        data_set_counter += 1


    with open(plotfile,'w') as handle:
        handle.write(code % {"output":outputfile,"x_label":x_label, "y_label": y_label, "var_defs": var_defs_str, "functions": functions_str, "plot": plot_str})

    proc=subprocess.Popen(shlex.split('gnuplot "'+plotfile+'"'))
    proc.communicate()

    if show:
        img = Image.open(outputfile)
        img.show()
