# coding=utf-8

from threading import Thread, Lock
from flask import (Flask, url_for, render_template, request, flash, redirect, session, jsonify, Response, send_from_directory)
import tt, os, imghdr
from werkzeug import secure_filename
app = Flask(__name__)
app.secret_key = 'your secret here'
lock = Lock()

numRequests = 0

app.config['UPLOADS'] = 'uploads'
app.config['MAX_UPLOAD'] = 16777215

@app.route('/', methods=['GET','POST'])
def home():
    '''Direct to home page'''
    session['location'] = "home"

    conn = tt.getConn('ovw') 

    #if someone is logged in
    if 'user' in session:
        
        #retrieve tip information with their respective like counts 
        tips = tt.getTipsAndLikes(conn)
        uID = tt.getuIDFromUser(conn,session['user'])['uID']
        
        # loop through every tip in our tips dictionary and check to see if 
        #the logged in user has liked the post.
        for tip in tips:

            #if the user has liked the post, then we want to show the "unlike"
            #button so the user can undo their like. otherwise, if the user
            #has not liked a post, show the "like" button so the user has the 
            #option to like it. tip['likeText'] is accessed in the template
            #when jinja2 is building the like buttons
            userLikes = tt.checkLikes(conn,tip['tipID'],uID)
            tip['likeText'] = 'Unlike' if userLikes else 'Like'
    
    #otherwise, if no one is logged in, just retrieve tips with totalLike info
    else:
        tips=tt.getTipsAndLikes(conn)
        
    popTip = tt.popularTip(conn)
    
    return render_template('home.html', tips=tips, today=popTip)



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
            f = request.files['img']
            #check filetype
            mime_type = imghdr.what(f.stream)
            if mime_type not in ['jpeg','gif','png']:
                raise ValueError('Not a JPEG, GIF or PNG: {}'.format(mime_type))
            #check filesize
            fSize = os.fstat(f.stream.fileno()).st_size
            if fSize > app.config['MAX_UPLOAD']:
                raise ValueError('File is too large, please upload a smaller image.')
            image = f.read()
            
        except ValueError as err:
            flash('Image Upload Failed {why}'.format(why=err))
            return render_template('postTipOrTrick.html')
        except:
            pass
        
        conn = tt.getConn('ovw')
        uID = tt.getuIDFromUser(conn,session['user'])['uID'] #gets the current user's uID
        print(session['user'])
        print(uID)
        tipDict = {'title': title, 'text': text, 'uid': uID, 'hero': hero, 'map': tipMap, 'image': image, 'difficulty': diff}
        
        tipID = tt.insertPost(conn, tipDict)['tipID']
        print(tipID)
        return redirect( url_for('tip', tipID = tipID) )
        
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        return redirect( url_for('login') )

    if 'user' not in session:
        flash("You must be logged in to post a tip!")
        
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
        
        
        
        #if someone is logged in, get their uID so we can use it later
        if 'user' in session:
            uID = tt.getuIDFromUser(conn,session['user'])['uID']
        
        for tip in tips:
            
            tip['totalLikes']=tt.tipLikes(conn,tip['tipID'])
            
            # we check to see if the user is in session again
            #down here, so we do not waste a computation getting the uID
            #every single time we run the loop. assume tt.getuIDFromUser worked
            #because it is only run when someone is logged in
            if 'user' in session:
                userLikes = tt.checkLikes(conn,tip['tipID'],uID)
                tip['likeText'] = 'Unlike' if userLikes else 'Like'

                
        #update filter_dict for display
        for key, value in filter_dict.iteritems():
            if value == '%':
                filter_dict[key] = u'All'
        filter_dict['searchTerm'] = filter_dict['searchTerm'].strip("%")
        
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

    tip['totalLikes']=tt.tipLikes(conn,tip['tipID'])

    
    #note that since this is the first place we check if user is in session,
    #we save the uID and use it later. this is because we conditionally
    #use it later if the comments form is used
    if 'user' in session:
        uID = tt.getuIDFromUser(conn,session['user'])['uID'] #gets the current user's uID
        
        #check if the logged in user has liked this specific tip
        userLikes = tt.checkLikes(conn,tip['tipID'],uID)
        tip['likeText'] = 'Unlike' if userLikes else 'Like'
     
    #retrieves new comment data in form for the tip and inserts into DB.
    if request.method == 'POST' and request.form['addComment'] == 'Add Comment':
        
        if 'user' in session:
            
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
    if request.method == 'POST' and request.form['submit'] == 'Create your account!':
        return redirect(url_for('createAccount'))
    
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
            session['logged_in'] = False
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
    if image == 'NULL' or image == None:
        return send_from_directory('static', 'image-placeholder.jpg')
    else:
        return Response(image, mimetype='image/'+imghdr.what(None,image))
        
@app.route('/createAccount/', methods=['GET','POST'])
def createAccount():
    if request.method == 'POST' and request.form['submit'] == 'Create Account':
        #check passwords
        pass1 = request.form.get('pass1')
        pass2 = request.form.get('pass2')
        if pass1 != pass2:
            flash("Your two passwords did not match please try again")
            return render_template('createAccount.html')

        #check that username is novel
        userName = request.form.get('username')
        conn = tt.getConn('ovw')
        if tt.getuIDFromUser(conn,userName) is not None:
            flash("That username already exsists on our server! please try again")
            return render_template('createAccount.html')
        else:
            uID = tt.addUser(conn, userName, pass1)
            flash("Welcome to OTT Agent " + userName + "!")
            session['logged_in'] = True
            session['user'] = userName
            return redirect( url_for('home') )
        
    return render_template('createAccount.html')
    
@app.route('/user/<userName>')#, methods=['GET','POST'])
def userPage(userName):
    if not session['logged_in']: #check that they are logged in
        flash("Please log in to view your profile!")
        return redirect( url_for('home') )
    elif session['user'] != userName: #check that they are the user they say they are
        flash("Please log in to view your profile!")
        #logout any stored user info and return to homepage
        session['logged_in'] = False
        session.pop('user')
        return redirect( url_for('home') )
    else:
        conn = tt.getConn('ovw')
        tips = tt.getTipbyUser(conn, userName)
        return render_template('userPage.html', tips=tips)

@app.route('/likePost',methods=['POST','GET'])
def likePost():
    if 'user' in session:
        
        likeButtonText = request.form.get('likeButtonText');
        tipID = request.form.get('tipID');

         #connect to the database
        conn = tt.getConn('ovw');
        uID=tt.getuIDFromUser(conn, session['user'])['uID']
        
        #locking because we check for several things and modify the database
        lock.acquire()
        tt.setLikes(conn,int(tipID),int(uID));
        newLikes = tt.tipLikes(conn,tipID);
        lock.release()
        
        #if like buttontext is like, change to unlike. otherwise, the
        #button text is not like, so change it back to like.
        likeButtonText = "Unlike" if likeButtonText=="Like" else "Like"
        

        return jsonify({'likeButtonText':likeButtonText, 'newLikes':newLikes,'tipID':tipID})

    
    
if (__name__ == '__main__'):
    app.debug = True
    app.run('0.0.0.0', 8081)