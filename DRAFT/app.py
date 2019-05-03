

from flask import (Flask, url_for, render_template, request, flash, redirect, session, jsonify)
import tt
app = Flask(__name__)
app.secret_key = 'your secret here'

numRequests = 0

@app.route('/', methods=['GET','POST'])
def home():
    
    if request.method == 'POST' and request.form['submit'] == 'Login':
        flash("Login is not yet implemented")
        
    '''Direct to home page'''
    conn = tt.getConn('ovw') 
    tips = tt.getTips(conn)
    
    return render_template('home.html', tips=tips)

#Edited by Anna (Sunday April 21st)
@app.route('/addPost/', methods=['GET','POST'])
def addPost():
    if request.method == 'POST' and request.form['submit'] == 'Add Post':
        title = request.form.get('title')
        text = request.form.get('post-text')
        tipDict = {'title': title, 'text': text, 'uid': 1, 'hero': None, 'map': None, 'image': None, 'difficulty': 'Intermediate'}
        conn = tt.getConn('ovw')
        tt.insertPost(conn, tipDict)
    elif request.method == 'POST' and request.form['submit'] == 'Login':
        flash("Login is not yet implemented")
    else: 
         title = request.args.get('title')
         text = request.args.get('text')
    #flash("Post is here!! {}".format(title))
    return render_template('postTipOrTrick.html')
    


if (__name__ == '__main__'):
    app.debug = True
    app.run('0.0.0.0', 8081)