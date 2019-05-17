'''This module provides several functions that are useful for a DataBase Interface (DBI).
It wouldn't be necessary except for the hassles with unicode, which require us to 
1. tell the database that we would like data delivered in utf8, instead of whatever default
it uses (probably Latin1), and
2. Provides a way to convert rows to have unicode objects instead of Python strings.

Someday, when we are using Python3, this won't be necessary.
'''

import MySQLdb

def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.set_character_set('utf8')
    curs = conn.cursor()
    curs.execute('set names utf8;')
    curs.execute('set character set utf8;')
    curs.execute('set character_set_connection=utf8;')
    return conn
    
def utf8(val):
    return unicode(val,'utf8') if type(val) is str else val

def dict2utf8(dic):
    '''Because dictionaries are mutable, this mutates the dictionary; it also returns it'''
    for k,v in dic.iteritems():
        dic[k] = utf8(v)
    return dic

def tuple2utf8(tup):
    return tuple(map(utf8,tup))

def row2utf8(row):
    if type(row) is tuple:
        return tuple2utf8(row)
    elif type(row) is dict:
        return dict2utf8(row)
    else:
        raise TypeError('row is of unhandled type: ' + str(type(row)))

if __name__ == '__main__':
    conn = getConn('wmdb')
    curs = conn.cursor()
    curs.execute('select user()')
    row1 = curs.fetchone()
    print('You are connected as {u}'.format(u=row1[0]))
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select name from person where name like %s', ['%Chalamet'])
    print('People whose names end in Chalamet:')
    for p in curs.fetchall():
        row2utf8(p)
        print('\t{n}'.format(n=p['name'].encode('utf8')))

