#import units

class Output:
    def __init__(self, directory):
        self._files = []
        self._used_filenames = []


    def addFile(self, filename, content):
        self._files.append((filename, content))

    def save(self, data, config):
        # if activated, create automatic csv-file of results
        # TODO Make csv-file nice
        if config["auto_csv"]:
            content = ""
            for q in data:
                content += "%s,%s,%s,%s,%s\n" % (data[q].longname,data[q].name,data[q].value,data[q].uncert,data[q].value_prefUnit)
            self._make_file(config["auto_csv"], content, config["directory"])

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
