# coding=utf-8

from flask import (Flask, url_for, render_template, request, flash, redirect, session, jsonify)
import tt, os, imghdr
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'your secret here'

numRequests = 0

app.config['UPLOADS'] = 'uploads'
app.config['MAX_UPLOAD'] = 256000

#THIS IS DEFUALT NAME OF EVERY PICTURE UPLOADED!!! we need to fix this
IDnum = '123123'

@app.route('/', methods=['GET','POST'])
def home():
    '''Direct to home page'''
    try: 
        
        session['location']="home"
       
        conn = tt.getConn('ovw') 
        tips = tt.getTips(conn)
        
        return render_template('home.html', tips=tips)
    except Exception as err:
        flash('Whoops! Looks like you encountered the following form error: '+str(err))
        return redirect( url_for('home') )

@app.route('/addPost/', methods=['GET','POST'])
def addPost():
        
    '''inserts a post to the database'''
    
    session['location']="addPost"
    
    if request.method == 'POST' and request.form['submit'] == 'Add Post':
        title = request.form.get('title')
        text = request.form.get('text')
        hero = request.form.get('hero')
        tipMap = request.form.get('map')
        tipMap = request.form.get('map')
        diff = request.form.get('diff')
        #THIS IMAGE UPLOAD CODE NEEDS TO BE TESTED!!  
        try:
            f = request.files['img']
            fSize = os.fstat(f.stream.fileno()).st_size
            #print 'file size is ',fsize
            if fSize > app.config['MAX_UPLOAD']:
                raise Exception('File is too large, please upload a smaller image.')
            mime_type = imghdr.what(f)
            if mime_type.lower() not in ['jpeg','gif','png']:
                raise Exception('Not a JPEG, GIF or PNG: {}'.format(mime_type))
            filename = secure_filename('{}.{}'.format(IDnum,mime_type))
            pathname = os.path.join(app.config['UPLOADS'],filename)
            #f.save(pathname)
            img = f
        except Exception as err:
            flash('Image Upload Failed {why}'.format(why=err))
            return render_template('postTipOrTrick.html')
        
        tipDict = {'title': title, 'text': text, 'uid': 1, 'hero': hero, 'map': tipMap, 'image': None, 'difficulty': diff}
        
        conn = tt.getConn('ovw')
        tt.insertPost(conn, tipDict)
        
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        return redirect( url_for('login') )
    else: 
         title = request.args.get('title')
         text = request.args.get('text')
    #flash("Post is here!! {}".format(title))
    return render_template('postTipOrTrick.html')
    

@app.route('/search/', methods=['GET','POST'])
def search():
    '''searches database for entries in the database that match the 
    given criteria in the search bar. Fitlers include; map name, hero name, 
    difficulty, any text'''

    #for simplicity, we will not save our search query in the session 
    #because it is post and not get
    session['location']="home" 
    
    if request.method == 'POST' and request.form['submitSearch'] == 'Search':
        conn = tt.getConn('ovw')

        filter_dict = {'searchTerm' : request.form.get('search'), 
        'mapName': request.form.get('maps'),
        'heroName': request.form.get('heroes'),
        'difficulty': request.form.get('difficulty')}

        # print filter_dict
        tips =  tt.getSearchResults(conn, filter_dict)
        # print tips
        if len(tips) == 0:
            flash('''We're sorry, we don't have any tips matching:
                '%s' 
        Map: %s 
        Hero: %s
        Difficulty: %s''' % (filter_dict['searchTerm'], 
        filter_dict['mapName'], filter_dict['heroName'],
        filter_dict['difficulty']))
            
        else: 
            flash('''Displaying results for: '%s' 
        Map: %s 
        Hero: %s
        Difficulty: %s''' % (filter_dict['searchTerm'], 
        filter_dict['mapName'], filter_dict['heroName'],
        filter_dict['difficulty']))
        
        
        return render_template('search.html', tips=tips)
    return redirect(url_for('home'))
    
@app.route('/tip/<tipID>', methods=['GET','POST'])
def tipPage(tipID):
    '''displays all associated data for a tip in a new webpage, 
    including all of the comments left on a post. Users can also add comments
    to the post on this page.'''

    #our location will be a numeric string (ex:"123") iff we are saving
    #the tipID as the location
    session['location']=tipID 
    
    
    conn = tt.getConn('ovw')
    
    #get all data associated with a tip
    tip = tt.getTip(conn, tipID)
    
    #retrieves new comment data in form for the tip and inserts into DB.
    if request.method == 'POST' and request.form['addComment'] == 'Add Comment':
        
        if session['logged_in']:
            uID = tt.getuIDFromUser(conn,session['user']) #gets the current user's uID
            
            commentText = request.form.get("commentText")
            m = tt.insertComment(conn, {'uID': uID, 'tipID': tipID, 'commentText': commentText})
            if m == 'success':
                flash('Your comment has been added to the database')
            else: 
                flash("Your comment was not able to be added to the database")
        flash('You must be logged in to comment.')

    #retreives comments for a given tip    
    comments = tt.getComments(conn, tipID)
    return render_template('trick.html',comments=comments,trick=tip)

@app.route('/login',methods=['POST'])
def login():
    '''validates loginname and password, and updates session information.
    Home page shows correct navbar (login bar, or logged in bar) 
    depending on logged_in status'''
    try:

        username = request.form['loginname']
        password = request.form['loginpass']
        conn = tt.getConn('ovw')
        
        #returns table row if there is a username/password match
        credentials = tt.checkLogin(conn,username,password)
        
        #either flash an error or flash a success message and update session
        if credentials is None:
            flash("Incorrect username or password. Please try again.")
            
        else:
            flash("Login successful. Welcome to OTT, Agent " + username +".")
            session['user'] = username
            session['logged_in'] = True
            
            #if the location str is a digit, we have saved the tipID
            if session['location'].isdigit():
                return redirect(url_for("tipPage",tipID=session['location']))
            return redirect(url_for(session['location']))
        
    except Exception as err:
        flash('Whoops! Looks like you encountered the following form error: '+str(err))
        return redirect( url_for('home') )
    

@app.route('/logout',methods=["POST"])
def logout():
    '''logs out or redirects to homepage with a message if someone
    tries to access the page without being logged in'''
    try:
        
        if session['logged_in']:
            
            #remove session information
            session.pop('user');
            session.pop('logged_in')
            flash("Successfully logged out. Until next time.")
            
           
            #if the location str is a digit, we have saved the tipID
            if session['location'].isdigit():
                return redirect(url_for("tipPage",tipID=session['location']))
            return redirect(url_for(session['location']))
        
        #if session['logged_in'] doesn't exist, that means we are not logged in!
        flash("Sorry, you must be logged in to log out. Go figure.")
        return redirect(url_for('home'))
        
    except Exception as err:
        flash('Whoops! Looks like you encountered the following error: '+str(err))
        return redirect( url_for('home') )
        

        
if (__name__ == '__main__'):
    app.debug = True
    
    app.run('0.0.0.0', 8081)