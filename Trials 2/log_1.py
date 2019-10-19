from flask import Flask,render_template,request, redirect, url_for
from mysql.connector import *

db=connect(host="localhost", user="root", passwd='padmanabhav98', database='cloud_tr1')
c=db.cursor()


app=Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return redirect('login')

@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('log.html')


@app.route('/home', methods=['POST','GET'])
def home():
    if request.method=='POST':
        user=request.form['username']
        pwd=request.form['pwd']

        ua=5 #default Access
        #check with db entries
        l=[]
        c.execute("select* from users;")
        for i in c:
            l.append(i)

        for i in l:
            if user==i[0]:
                if pwd==i[1]:
                    ua=i[2]
                    break
            
        
        if ua in [0,1,2]:
            return render_template('home.html',username=user, pwd=pwd)
        else:
            return render_template('log_err.html')

app.run()
