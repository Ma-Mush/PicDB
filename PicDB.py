import numpy as np
from PIL import Image

class PicDB(object):
    def __init__(self, filename):
        self.filename = filename
    
    def _to_format_db(self, string):
        string = string.split("\n")
        ret = []
        for i in range(len(string)):
            ret.append([])
            for j in range(0, len(string[i]), 3):
                ret[i].append([ord(_) for _ in string[i][j:j+3]])
            if len(ret[i][-1]) != 3:
                ret[i][-1] += [0 for i in range(3-len(ret[i][-1]))]
        data = np.zeros((len(string), max([len(i) for i in ret]), 3), dtype=np.uint8)
        for i in range(len(ret)):
            for j in range(len(ret[i])):
                data[i][j] = ret[i][j]
        return data

    def _to_db(self, text):
        tfdb = self._to_format_db(text)
        image = Image.fromarray(tfdb, "RGB")
        image.save(self.filename)

    def read_db(self):
        image = np.asarray(Image.open(self.filename).convert("RGB"))
        ret = []
        for i in image:
            string = ""
            for j in i:
                for m in j:
                    string+= chr(m)
            ret.append(string.strip())
        return "\n".join(ret)

    def get_all_data(self):
        db = self.read_db().split("\n")
        for i in range(len(db)):
            db[i] = db[i].split("%tit%")[1].split("%new%")
        ret = []
        for i in range(len(db[0])):
            ret.append([db[j][i].replace("\\n", "\n") for j in range(len(db))])
        return ret[:-1]

    def pretty_read(self):
        db = self.read_db().split("\n")
        titles = [i.split("%tit%")[0] for i in db]
        ret = ""
        data = self.get_all_data()
        spaces = [] 
        for i in range(len(titles)):
            sp = [len(titles[i])]
            for j in data:
                sp.append(len(j[i]))
            spaces.append(max(sp))
        for i in range(len(titles)):
            s = (spaces[i] - len(titles[i])+3)
            ret += "|" + " "*s+titles[i] + " "*s
        ret += "|\n"
        for i in range(len(data)):
            for j in range(len(data[i])):
                s = (spaces[j] - len(data[i][j])+3)
                ret += "|" + " "*s + data[i][j] + " "*s
            ret += "|\n"
        return ret
        
    def create_titles(self, mass):
        for i in range(len(mass)) :
              mass[i] = mass[i].replace("\n", "\\n") + "%tit%"
        a = "\n".join(mass)
        self._to_db(a)

    def edit_data(self, title_last, last_data, title_new, new_data):
        db = self.read_db().split("\n")
        title_last, last_data,\
        title_new, new_data = \
                    title_last.replace("\n", "\\n"), last_data.replace("\n", "\\n"),\
                    title_new.replace("\n", "\\n"), new_data.replace("\n", "\\n")
        ind = []
        for i in range(len(db)):
              if db[i].split("%tit%")[0]== title_last:
                  datatit =db[i].split("%tit%")[1].split("%new%")
                  for j in range(len(datatit)) :
                      if datatit[j] == last_data:
                          ind.append(j)
        if ind != []:
            for i in range(len(db)):
                if db[i].split("%tit%")[0] == title_new:
                    datatit =db[i].split("%tit%")[1].split("%new%")
                    for index in ind:
                        datatit[index] = new_data
                    db[i] = title_new +"%tit%"+ "%new%".join(datatit)
                    break
        db = "\n".join(db)
        self._to_db(db)

    def insert_data(self, mass):
        db = self.read_db().split("\n")
        for i in range(len(db)):
            db[i] = db[i].replace("\x00", "") + mass[i].replace("\n", "\\n") + "%new%"
        db = "\n".join(db)
        self._to_db(db)

    def select_data(self, title, data):
        title, data = title.replace("\n", "\\n"), data.replace("\n", "\\n")
        db = self.read_db().split("\n")
        ret2 = []
        ret = []
        ind = []
        for i in db:
            if i.split("%tit%")[0] == title:
                 tek = i.split("%tit%")[1].split("%new%")
                 for j in range(len(tek)):
                     if tek[j] == data:
                         ind.append(j)
        if ind != []:
            for i in db:
                tek = i.split("%tit%")[1].split("%new%")
                for index in ind:
                    ret2.append(tek[index].replace("\\n", "\n"))
            lret2 = len(ret2)
            ldb = len(db)
            if  lret2 != ldb:
                r2db = int(lret2/ldb)
                for i in range(r2db):
                    tek = []
                    for j in range(i, lret2, r2db):
                        tek.append(ret2[j])
                    ret.append(tek)
            else:
                ret = [ret2]
        return ret

    def delete_data(self, title, data):
        title, data = title.replace("\n", "\\n"), data.replace("\n", "\\n")
        db = self.read_db().split("\n")
        ind = []
        for i in db:
            tek = i.split("%tit%")
            if tek[0] == title:
                 tek = tek[1].split("%new%")
                 for j in range(len(tek)):
                     if tek[j] == data:
                         ind.append(j)
        if ind != []:
            for i in range(len(db)):
                k = 0
                for index in ind:
                    index -= k
                    tek = db[i].split("%tit%")
                    data = tek[1].split("%new%")
                    db[i] = data[:index] + data[index+1:]
                    db[i] = tek[0] + "%tit%" + "%new%".join(db[i])
                    k+=1
        db = "\n".join(db)
        self._to_db(db)

    def update_titles(self, new_titles):
        db = self.read_db().split("\n")
        new_titles = [i.replace("\n", "\\n") for i in new_titles]
        for i in range(min(len(new_titles), len(db))):
            ind = db[i].find("%tit%")
            db[i] = new_titles[i] + db[i][ind:]     
        if len(new_titles) < len(db):
            del db[len(new_titles):]
        else:
            n = len(db[i].split("%tit%")[1].split("%new%"))
            for i in range(len(new_titles)-len(db)):
                db.append(new_titles[-i-1]+"%tit%" + "%new%"*n)
        db = "\n".join(db)
        self._to_db(db)

