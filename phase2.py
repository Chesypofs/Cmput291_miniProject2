from bsddb3 import db

#Create a hash index on tweets.txt with tweet ids as keys and the full tweet record as data named tw.idx
DATABASE = 'tw.idx'
database = db.DB()
database.open(DATABASE, None, db.DB_HASH, db.DB_CREATE)
curs = database.cursor()
f = open('tweets.txt', 'r')
word = f.readline()
while word:
    if word[-1] == '\n':
        word = word[:-1]
    (key, rec)=word.split(':',1)
    curs.put(bytes(key,"utf-8"), bytes(rec,"utf-8"),db.DB_KEYFIRST)
    word = f.readline()
database.close()  

#Create a B+-tree index on terms.txt with terms as keys and tweet ids as data named te.idx
DATABASE = 'te.idx'
database = db.DB()
database.set_flags(db.DB_DUP)
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()
f = open('terms.txt', 'r')
word = f.readline()
while word:
    if word[-1] == '\n':
        word = word[:-1]
    (key, rec)=word.split(':')
    curs.put(bytes(key,"utf-8"), bytes(rec,"utf-8"), db.DB_KEYFIRST)
    word = f.readline()
database.close() 

#Create a B+-tree index on dates.txt with dates as keys and tweet ids as data named da.idx
DATABASE = 'da.idx'
database = db.DB()
database.set_flags(db.DB_DUP)
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()
f = open('dates.txt', 'r')
word = f.readline()
while word:
    if word[-1] == '\n':
        word = word[:-1]
    (key, rec)=word.split(':')
    curs.put(bytes(key,"utf-8"), bytes(rec,"utf-8"), db.DB_KEYFIRST)
    word = f.readline()
database.close() 