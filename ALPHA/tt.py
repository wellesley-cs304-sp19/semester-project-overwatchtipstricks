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
    
    curs.execute('select tipID from tips where datePosted = %s', (datePosted,))
    
    return curs.fetchone()

def insertComment(conn, comment_dict):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    datePosted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # if image and difficulty: 
    print "INSERTING COMMENT:"
    print comment_dict
    curs.execute("insert into comments(uID, tipID, commentText, datePosted) values \
                    (%s, %s, %s, %s);",
            (comment_dict['uID'], comment_dict['tipID'], comment_dict['commentText'], datePosted))
    conn.commit()
    return "success"

def getTips(conn):
    '''returns all tips in the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips')
    return curs.fetchall()
    
def getTip(conn, tipID):
    '''Returns a specific tip from the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips where tipID = %s', (tipID,))
    return curs.fetchone()
    
def getComments(conn, tipID):
    '''Returns comments relevant to a given tip from the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select comments.commentText, comments.datePosted, user.username from comments inner join user using (uID) where tipID = %s", (tipID,))
    return curs.fetchall()

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

def checkLogin(conn,user,pw):
    '''checks for a username and password match. If there is a match,
    this function will return a row. Otherwise, it will return None'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from user where username=%s and password=%s', (user,pw))
    return curs.fetchone()
    
def getuIDFromUser(conn,user):
    '''searches for the uID of a user. this function should only be called 
    after it is verified that someone is logged into the database, otherwise
    will return no results. assume usernames are all unique since there
    is currently no way to make an account'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select uID from user where username=%s', (user,))
    return curs.fetchone()
    
def getImage(conn, tipID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    numrows = curs.execute('''select tipID,uID,image from tips
                            where tipID = %s''', [tipID])
    #MIGHT HAVE TO CHECK FOR ZERO ROWS BEFORE THIS
    return curs.fetchone()
    
if __name__ == '__main__':
    conn= getConn('ovw')
    #print len(getSearchResults(conn, {'mapName': 'sdfds', 'difficulty': 'All',
    #'heroName': 'All', 'searchTerm': 'kill'}))
        
