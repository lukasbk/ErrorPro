
class Output():
    def __init__(self):
        self.files = []

    def addFiles(self, files_obj):
        self.files.append(files_obj)

    def generate(self, data, config):
        i = 1
        for f_obj in self.files:
            f_obj.save("plot"+str(i)+"_", config["directory"])
            i += 1



class Files():
    """
    class to flexibly save files like gnuplot or matplotlib plots
    """
    def save(self, prefix, directory):
        pass
