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
    
    if request.method == 'POST' and request.form['submit'] == 'Login':
        flash("Login is not yet implemented")
        
    '''Direct to home page'''
    conn = tt.getConn('ovw') 
    tips = tt.getTips(conn)
    
    return render_template('home.html', tips=tips)

@app.route('/addPost/', methods=['GET','POST'])
def addPost():
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
            f.save(pathname)
            img = f
        except Exception as err:
            flash('Image Upload Failed {why}'.format(why=err))
            return render_template('postTipOrTrick.html')
        
        tipDict = {'title': title, 'text': text, 'uid': 1, 'hero': hero, 'map': tipMap, 'image': img, 'difficulty': diff}
        
        conn = tt.getConn('ovw')
        tt.insertPost(conn, tipDict)
        
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        flash("Login is not yet implemented")
    else: 
         title = request.args.get('title')
         text = request.args.get('text')
    #flash("Post is here!! {}".format(title))
    return render_template('postTipOrTrick.html')
    

@app.route('/search/', methods=['GET','POST'])
def search():
    if request.method == 'POST' and request.form['submitSearch'] == 'Search':
        conn = tt.getConn('ovw')

        filter_dict = {'searchTerm' : request.form.get('search'), 
        'mapName': request.form.get('maps'),
        'heroName': request.form.get('heroes'),
        'difficulty': request.form.get('difficulty')}

        print filter_dict
        tips =  tt.getSearchResults(conn, filter_dict)
        print tips
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

@app.route('/login',methods=['GET','POST'])
def login():
    return redirect(url_for('home'))
    
    
if (__name__ == '__main__'):
    app.debug = True
    
    app.run('0.0.0.0', 8081)