import csv
from os.path import isfile
class csvloader:
    def __init__(self,csvfile):
        self.csvfile = csvfile
        if not isfile(csvfile):
            return 
        with open(csvfile,encoding='utf-8') as f:
            read = csv.reader(f)
            if not read:
                return 
            self.values = []
            for i in read:
                self.values.append(i)
        #header 头部信息
        self.header = self.values.pop(0)
        for head in self.header:
            if not head.strip() :
                self.header.remove(head)
        self.data = []
        for i in self.values:
            item = {}.fromkeys(self.header)
            if not i:
                continue
            for v in range(len(self.header)):
                if not i[v].strip():
                   i[v] = None
                try :
                    item[self.header[v]] = i[v]   
                except : pass
            self.data.append(item)
        self._index = 0

    def __iter__(self): return self

    def __next__(self):
        if self._index < len(self.data):
            res = self.data[self._index]
            self._index += 1
            return res
        else:
            raise StopIteration
