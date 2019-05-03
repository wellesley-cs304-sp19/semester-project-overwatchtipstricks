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
        
#returns all tips in the database
def getTips(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from tips')
    return curs.fetchall()
    
