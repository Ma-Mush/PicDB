import numpy as np
from PIL import Image

class PicDB(object):
    def __init__(self, filename):
        self.filename = filename
    
    def _to_format_db(self, string, mod=0):
       ret =[]
       for i in range(0, len(string), 3):
           ret.append([ord(_) for _ in string[i:i+3]] )
       if len(ret[-1]) != 3:
           ret[-1] += [0 for i in range(3-len(ret[-1]))]
       if mod == 0:
           data = np.zeros((1, len(ret) , 3), dtype=np.uint8)
           for i in range(len(data[0])) :
               data[0][i] = ret[i]
       elif mod ==1:
           data = np.zeros((string.count("\n"), len(ret) , 3), dtype=np.uint8)
           tek = 0
           for i in range(len(data[0])) :
               if string[i] == "\n":
                   tek += 1
               data[tek][i] = ret[i]
       return data

    def _to_db(self, text):
        tfdb = self._to_format_db(text)
        image = Image.fromarray(tfdb, "RGB")
        image.save(self.filename)

    def read_db(self):
        image = np.asarray(Image.open(self.filename).convert("RGB"))
        ret = ""
        for i in image[0]:
             for j in i:
                 ret += chr(j)
        return ret.strip()

    def get_all_data(self):
        db = self.read_db().split("\n")
        for i in range(len(db)):
            db[i] = db[i].split("%tit%")[1].split("%new%")
        ret = []
        for i in range(len(db[0])):
            ret.append([db[j][i] for j in range(len(db))])
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
              mass[i] = mass[i] + "%tit%"
        a = "\n".join(mass)
        self._to_db(a)

    def edit_data(self, title_last, last_data, title_new, new_data):
        db = self.read_db().split("\n")
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
            db[i] = db[i].replace("\x00", "") + mass[i] + "%new%"
        db = "\n".join(db)
        self._to_db(db)

    def select_data(self, title, data):
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
                    ret2.append(tek[index])
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
        db = self.read_db().split("\n")
        ind = None
        ind = []
        for i in db:
            if i.split("%tit%")[0] == title:
                 tek = i.split("%tit%")[1].split("%new%")
                 for j in range(len(tek)):
                     if tek[j] == data:
                         ind.append(j)
        if ind != []:
            for i in range(len(db)):
                tek = db[i].split("%tit%")[1].split("%new%")
                tit = db[i].split("%tit%")[0]
                for index in ind:
                    print(db[i], tek)
                    db[i] = tek[:index]
                    if len(db) != index:
                        db[i] += tek[index+1:]
                    db[i] = tit + "%tit%" + "%new%".join(db[i])
        db = "\n".join(db)
        self._to_db(db)

