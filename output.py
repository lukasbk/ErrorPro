#import units

class Output:
    def __init__(self, directory):
        self._directory = directory
        self._files = []

    def addFile(self, filename, content):
        self._files.append((filename, content))

    def liveOutput(self, content):
        print(content)

    def save(self, data, config):
        if config["auto_results"]:
            f = open(self._directory +"/"+ "results.csv","w+")
            for q in data:
                f.write("%s,%s,%s,%s,%s\n" % (data[q].longname,data[q].name,data[q].value,data[q].uncert,data[q].value_prefUnit))
            f.close()

        for filename, content in self._files:
            f = open(self._directory + filename,"w+")
            f.write(content)
            f.close()
