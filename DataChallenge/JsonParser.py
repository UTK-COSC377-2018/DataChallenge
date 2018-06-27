import json

class JSONParser:

    def __init__(self, files=""):
        if type(files) is tuple:
            files = list(files)
        assert((type(files) is str) or (type(files) is list))
        self.files = []
        self.data = []
        if len(files) != 0:
            if type(files) is str:
                self.files.append(files)
            else:
                self.files.extend(files)
            self._parseFiles()
        return

    def _parseFiles(self):
        for fname in self.files:
            with open(fname) as f:
                tmp = json.load(f)
                self.data.append(tmp)
        return

    def addJSON(self, fname):
        if type(fname) is str:
            with open(fname) as f:
                tmp = json.load(f)
                self.files.append(fname)
                self.data.append(tmp)
        elif (type(fname) is list) or (type(fname) is tuple):
            if type(fname) is tuple:
                fname = list(fname)
            self.files.extend(fname)
            for fn in fname:
                with open(fn) as f:
                    tmp = json.load(f)
                    self.data.append(tmp)
        else:
            raise TypeError("Argument to addJSON must be a list, string, or tuple.")
        return

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __contains__(self, value):
        retval = False
        for json in self.data:
            if value in json:
                retval = True
        return retval
