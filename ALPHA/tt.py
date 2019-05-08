# Emma Lurie and Anna Farrell-Sherman

import sys
import MySQLdb
import datetime


def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    return conn
    

def insertPost(conn, tip_dict):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    title = tip_dict['title']
    text = tip_dict['text']
    uid = tip_dict['uid']
    hero = tip_dict['hero']
    mapName = tip_dict['map']
    image = tip_dict.get('image')
    difficulty = tip_dict.get('difficulty')
    
    datePosted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # if image and difficulty: 
    curs.execute('''insert into tips(title, postText, image, hero, map, difficulty, datePosted) 
                    values 
                    (%s, %s, %s, %s, %s, %s, %s);''', 
            (title, text, image, hero, mapName, difficulty, datePosted))
    conn.commit()
    return "success"
        

def getTips(conn):
    '''returns all tips in the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips')
    return curs.fetchall()
    
def getTip(conn, tID):
    '''Returns a specific tip from the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips where tipID = %s', (tID,))
    return curs.fetchone()

def getSearchResults(conn, filter_dict):
    '''return all the relevant search results'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)


    #create list of filter clauses
    clauses = []
    if filter_dict['mapName'] != 'All':
        clauses.append("map = '%s'" % filter_dict['mapName'])
        
    if filter_dict['heroName'] != 'All':
        clauses.append("hero = '%s'" % filter_dict['heroName'])
        
    if filter_dict['difficulty'] != 'All':
        clauses.append("difficulty = '%s'" % filter_dict['difficulty'])
    
    if filter_dict['searchTerm'] != '':
        clauses.append("postText like '%s'" % ('%' + filter_dict['searchTerm'] + '%',))
    
    #concatenate clauses lists into sql query string

    if len(clauses) == 0: 
        queryString = 'select * from tips;'
    
    elif len(clauses) == 1:
        queryString = "select * from tips where " + clauses[0]  + ";"
        
    else: 
        queryString =  "select * from tips where " + clauses[0] + " and " + " and ".join(clauses[1:]) + ";"
    
    #execute queryString
    curs.execute(queryString)
    return curs.fetchall()

if __name__ == '__main__':
    conn= getConn('ovw')
    #print len(getSearchResults(conn, {'mapName': 'sdfds', 'difficulty': 'All',
    #'heroName': 'All', 'searchTerm': 'kill'}))
        
