# Emma Lurie and Anna Farrell-Sherman

import sys
import MySQLdb
import datetime
import dbi

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
    curs.execute('''insert into tips(title, postText, image, hero, map, difficulty, datePosted, uID) 
                    values 
                    (%s, %s, %s, %s, %s, %s, %s, %s);''', 
            (title, text, image, hero, mapName, difficulty, datePosted, uid))
    conn.commit()
    
    curs.execute('select tipID from tips where datePosted = %s', (datePosted,))
    
    return curs.fetchone()

def insertComment(conn, comment_dict):
    '''adds a comment to the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    datePosted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # if image and difficulty: 
    curs.execute("insert into comments(uID, tipID, commentText, datePosted) values \
                    (%s, %s, %s, %s);",
            (comment_dict['uID'], comment_dict['tipID'], comment_dict['commentText'], datePosted))
    conn.commit()
    return "success"

def getTips(conn):
    '''returns all tips in the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips order by datePosted desc')
    all = curs.fetchall()
    for p in all:
        dbi.row2utf8(p)
    return all
    
def getTipsAndLikes(conn):
    '''returns all tips in the database inner joined with their like counts'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select a.*,count(b.tipID) as totalLikes from tips as a left join likes as b on a.tipID=b.tipID group by a.tipID order by datePosted desc")
    all = curs.fetchall()
    for p in all:
        dbi.row2utf8(p)
    return all
    
def getTip(conn, tipID):
    '''Returns a specific tip from the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips,user where tips.uID = user.uID and tipID = %s', (tipID,))
    row = curs.fetchone()

    dbi.dict2utf8(row)
    return row
    
def getTipbyUser(conn, userName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips,user where tips.uID = user.uID and user.username = %s', (userName,))
    return curs.fetchall()
    
def getComments(conn, tipID):
    '''Returns comments relevant to a given tip from the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select comments.commentText, comments.datePosted, user.username from comments inner join user using (uID) where tipID = %s", (tipID,))
    return curs.fetchall()

def getSearchResults(conn, filter_dict):
    '''return all the relevant search results'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    #update filter_dict
    for key, value in filter_dict.iteritems():
        if value == u'' or value == u'All':
            filter_dict[key] = '%'
            
    #update searchTerm to include pattern matching
    filter_dict['searchTerm'] = "% " + filter_dict['searchTerm'] + " %"

    curs.execute("select * from tips where (title like %s or postText like %s) and map like %s and difficulty like %s and hero like %s", 
                    (filter_dict['searchTerm'], filter_dict['searchTerm'], filter_dict['mapName'], filter_dict['difficulty'],filter_dict['heroName'],))
    return curs.fetchall()

# def checkLogin(conn,user,pw):
#     '''checks for a username and password match. If there is a match,
#     this function will return a row. Otherwise, it will return None'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('select * from user where username=%s and password=%s', (user,pw))
#     return curs.fetchone()
    
def getPassword(conn,user):
    '''searches for the uID of a user. returns none if the username does not yet exist'''

    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT password FROM user WHERE username= %s',[user])
    return curs.fetchone()
    
def getuIDFromUser(conn,user):
    '''searches for the uID of a user. returns none if the username does not yet exist'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select uID from user where username=%s', (user,))
    return curs.fetchone()
    
def getUserFromuID(conn,uID):
    '''searches for username of a user based on uID'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select username from user where uID=%s', (uID,))
    return curs.fetchone()
    
def getImage(conn, tipID):
    '''gets the image for a given tip out of the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    numrows = curs.execute('''select tipID,uID,image from tips
                            where tipID = %s''', [tipID])
    return curs.fetchone()
    
def popularTip(conn):
    '''gets the most recently comment on tip from the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select tips.title, tips.uID, tips.datePosted, tips.postText, tips.tipID from comments, tips where tips.tipID = comments.tipID  order by comments.datePosted desc limit 1')
    row = curs.fetchone()
    userID = getUserFromuID(conn, row['uID'])['username']
    row['user'] = userID
    
    dbi.dict2utf8(row)
    return row
    
def addUser(conn, username, password):
    '''adds a user to the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("insert into user(username,password,permission) values (%s, %s, 'player')", (username, password))
    conn.commit()
    curs.execute("select * from user where username = %s", (username,))
    row = curs.fetchone()
    userID = row['uID']
    return userID

def getPermission(conn, username):
    '''gets permission for an account on the server'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select permission from user where username=%s", (username))
    return curs.fetchone()

def checkLikes(conn,tipID,uID):
    ''''checks for existing likes between a user and a post'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    numrows = curs.execute('''select * from likes where uID=%s and tipID=%s''', [uID,tipID])
    return curs.fetchone()
    
def tipLikes(conn,tipID):
    ''''returns total # of likes for a given post'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    numrows = curs.execute('''select count(*) from likes where tipID=%s''', [tipID])
    return curs.fetchone()['count(*)']
    
def setLikes(conn,tipID,uID):
    '''sets the like count for a tip'''
    '''gets the image for a given tip out of the database'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    
    try:

        # checking to see if we have a record of the user liking the post
        tipUserLikeHistory = checkLikes(conn,tipID,uID)

        
        if tipUserLikeHistory:
            
            
           
            #user has liked the post. delete row from table to remove like
            curs.execute('''delete from likes where tipID=%s and uID=%s''', [tipID,uID])
            conn.commit();
            return "success"
    

        
        #user has not liked the post. insert user/tipID pair into likes table
        curs.execute('''insert into likes(tipID,uID) values (%s,%s)''', (tipID,uID))
        conn.commit();
        return "success"
        
    except Exception as err:
        print("ERRROR!!!!! in tt.py: " + str(err))
    
    
if __name__ == '__main__':
    conn= getConn('ovw')
  
        
