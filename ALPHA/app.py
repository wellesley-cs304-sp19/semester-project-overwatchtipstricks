# coding=utf-8

from flask import (Flask, url_for, render_template, request, flash, redirect, session, jsonify, Response, send_from_directory)
import tt, os, imghdr
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'your secret here'

numRequests = 0

app.config['UPLOADS'] = 'uploads'
app.config['MAX_UPLOAD'] = 2000000

#THIS IS DEFUALT NAME OF EVERY PICTURE UPLOADED!!! we need to fix this
IDnum = '123123'

@app.route('/', methods=['GET','POST'])
def home():
    '''Direct to home page'''
    session['location'] = "home"
    #determine if 

    conn = tt.getConn('ovw') 
    tips = tt.getTips(conn)
    
    return render_template('home.html', tips=tips)


@app.route('/addPost/', methods=['GET','POST'])
def addPost():
    '''inserts a post to the database'''
    
    session['location'] = "addPost"
    
    if request.method == 'POST' and request.form['submit'] == 'Add Post' and ('user' in session):
        title = request.form.get('title')
        text = request.form.get('text')
        hero = request.form.get('hero')
        tipMap = request.form.get('map')
        tipMap = request.form.get('map')
        diff = request.form.get('diff')
        image = None
        try:
            #nm = int(request.form['nm']) # may throw error
            f = request.files['img']
            #check filetype
            mime_type = imghdr.what(f.stream)
            if mime_type not in ['jpeg','gif','png']:
                raise ValueError('Not a JPEG, GIF or PNG: {}'.format(mime_type))
            #check filesize
            fSize = os.fstat(f.stream.fileno()).st_size
            print 'file size is ',fSize
            if fSize > app.config['MAX_UPLOAD']:
                raise ValueError('File is too large, please upload a smaller image.')
            image = f.read()
            
        except ValueError as err:
            flash('Image Upload Failed {why}'.format(why=err))
            return render_template('postTipOrTrick.html')
        except:
            pass
        
        tipDict = {'title': title, 'text': text, 'uid': 1, 'hero': hero, 'map': tipMap, 'image': image, 'difficulty': diff}
        
        conn = tt.getConn('ovw')
        tipID = tt.insertPost(conn, tipDict)['tipID']
        print(tipID)
        return redirect( url_for('tip', tipID = tipID) )
        
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        return redirect( url_for('login') )

    if 'user' not in session:
        flash("You must be logged in to post a tip!")
        
  
    print("ABOUT TO RENDER TEMPLATE")
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
  
        return render_template('search.html', tips=tips,filters=filter_dict)
    return redirect(url_for('home'))
    
@app.route('/tip/<tipID>', methods=['GET','POST'])
def tip(tipID):
    '''displays all associated data for a tip in a new webpage, 
    including all of the comments left on a post. Users can also add comments
    to the post on this page.'''

    #our location will be a numeric string (ex:"123") iff we are saving
    #the tipID as the location
    session['location']=tipID 
    
    #get all data associated with a tip
    conn = tt.getConn('ovw')
    tip = tt.getTip(conn, tipID)
    
    #retrieves new comment data in form for the tip and inserts into DB.
    if request.method == 'POST' and request.form['addComment'] == 'Add Comment':
        
        if 'user' in session:
            uID = tt.getuIDFromUser(conn,session['user'])['uID'] #gets the current user's uID
            
            commentText = request.form.get("commentText")
            
            m = tt.insertComment(conn, {'uID': uID, 'tipID': tipID, 'commentText': commentText})
            if m == 'success':
                flash('Your comment has been added to the database')
            else: 
                flash("Your comment was not able to be added to the database")
        else:
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
            print(session['user'])

        #if the location str is a digit, we have saved the tipID
        if session['location'].isdigit():
            return redirect(url_for("tip",tipID=session['location']))
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
            flash("Successfully logged out. Until next time.")
           
            #if the location str is a digit, we have saved the tipID
            if session['location'].isdigit():
                return redirect(url_for("tip",tipID=session['location']))
            return redirect(url_for(session['location']))
        
        #if 'logged_in' key doesn't exist, that means we are not logged in!
        flash("Sorry, you must be logged in to log out. Go figure.")
        return redirect(url_for('home'))
        
    except Exception as err:
        flash('Whoops! Looks like you encountered the following error: '+str(err))
        return redirect( url_for('home') )
        
@app.route('/image/<tipID>')
def image(tipID):
    conn = tt.getConn('ovw')
    row = tt.getImage(conn, tipID)
    image = row['image']
    if image == 'NULL':
        print("no image")
        return send_from_directory('static', 'image-placeholder.jpg')
    else:
        print len(image),imghdr.what(None,image)
        return Response(image, mimetype='image/'+imghdr.what(None,image))

        
if (__name__ == '__main__'):
    app.debug = True
    
    app.run('0.0.0.0', 8081)