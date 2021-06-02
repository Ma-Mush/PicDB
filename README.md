# PicDB

Attention
This project created in Telegeram-chat on phone and I'm not sure if the code is pretty :) 
Perhaps there were already such projects, but I did not know about them and came up with this one myself.
if you find bugs or fix my code, I will be happy :)
USE ONLY STRING!

Внимание
Этот проект создавался в Телеграм-чате на телефоне и я не уверен, что код красивый)
Возможно такие проекты уже были, но я не знал о них (и не знаю), этот придумал сам
если вы найдете баги или исправите мой код, я буду рад) 
ИСПОЛЬЗУЙТЕ ТОЛЬКО STRING!

+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+=++=+=+=+=+

Documentation
Документация

# import
from PicDB import PicBD

# _ = PicDB(filename)
Connect to "db"

Подкючение к "БД"

# _.read_db()
Return what the program is working with

Возвращает то, с чем работает программа

# _.get_all_data()
Return list with lists of data

Возвращает массив с массивами данных

[["data1", "data2"], [...], ...]

# _.pretty_read()
Return beautiful view of data :) 

Возвращает красивый вид данных)

# _.create_titles(mass)
mass - ["title1", "title2", ...]

mass - list with titles

mass - массив с заголовками

# ._edit_data(title_last, last_data, title_new, new_data)

name | what is it
------------- | -------------
title_last | ident title for search string / идентификация столбца для поиска строки
last_data | data in string for replacement data in title_new / данные в строке для замены данных в title_new
title_new | ident title for replacement data / идентификация столбца для замены
new_data | new data in searched cell / новые данные в найденной ячейке

# _.insert_data(mass)
Insert data 

mass - ["data in title1", "data in title2", ...]

mass - list with data / массив с данными

# _.select_data(title, data)
Return list with lists found items

Возвращает массив с массивами найденных данных

name | what is it
------------- | -------------
title | ident title for search string / идентификация столбца для поиска строки
data | data for ident cell / данные в строке для поиска ячейки

# _.delete_datat(title, data)
Delete data in cell

Удаляет данные в ячейке

name | what is it
------------- | -------------
title | ident title for search string / идентификация столбца для поиска строки
data | data for ident cell / данные в строке для поиска ячейки


# Examples / Примеры 
```python
from PicDB import PicBD
sql = PicBD('test_PicBD.png') # Connect to our "db"
sql.create(['id', 'hash']) # Create 2 titles - id and hash
sql.insert_data(['3234235', '134234234']) # insert data 
a = sql.select_data('234', 'id') # Selecrt string with id = 234
print(a) # [['234', '234']]
sql.edit_data('id', '234', 'hash', '1234') #
a = sql.select_data('234', 'id') #
print(a) #
b = sql.search('id', '3234235') #
print(b) #
a = sql.get_all_data() #
print(a) #
```
скоро допишу


