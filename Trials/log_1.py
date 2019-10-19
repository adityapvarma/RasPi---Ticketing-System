from flask import Flask,render_template,request

app=Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def login():
    return render_template('log.html')

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method=='POST':
        user=request.form['username']
        pwd=request.form['pwd']

        return render_template('home.html',username=user, pwd=pwd)

app.run()
