from flask import Flask,render_template,request, redirect, url_for
from mysql.connector import *
from random import randint

db=connect(host="localhost", user="root", passwd='padmanabhav98', database='cloud_tr2')
c=db.cursor()


app=Flask(__name__)
app.config["DEBUG"] = True


#Global variable used
unm=''
st_bal=0
log_err=''
point_err=''
l=['A','B','C','D','E','F']
usern_err=''
repass_err=''
typesel_err=''
get_user=''
def_us=''
tid_err=''
amt_err=''


"""
tid_err
unm-name for dyn pages
get_user-username
st_bal - starting balance
log_err-invalid credentials
point_err-same to and from point
l-list of stops
usern_err- username taken
repass_err- re enter mistake password reg
typesel_err= didnt select type
def_us - default username retained reg page
amt_err - amt_err
"""



@app.route('/', methods=['POST','GET'])
def index():
    return render_template('log.html',log_err_p=log_err)


@app.route('/home', methods=['POST','GET'])
def home():
    global log_err
    global unm
    global st_bal
    global get_user
    log_err=''
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
                    ua=i[3]
                    unm=i[2]

                    c.execute('select* from account;')
                    bl=[]
                    for i in c:
                        bl.append(i)

                    for i in bl:
                        if i[0]==user:
                            st_bal=i[1]
                            get_user=user
                            break
                    
            
        
        if ua ==2:
            return render_template('home_tc.html',username=unm,bal=st_bal,tid_err_p='')
        elif ua==1:
            return render_template('home_pass.html',point_err_p=point_err,username=unm,bal=st_bal);
        else:
            log_err='Username and Password Not Found! Please check your credentials'
            return redirect(url_for('index'))


#cost and bakance pending
        

@app.route('/home/gen_tick', methods=['POST','GET'])
def gen_tick():
    global point_err
    point_err=''
    if request.method=='POST':
        to_op=request.form['to']
        from_op=request.form['from']
        no_op=int(request.form['no'])
        

        if to_op==from_op:
            point_err='Both From and To locations are identical. Please try again!'
            return render_template('home_pass.html',point_err_p=point_err)
        else:
            if l.index(to_op)>l.index(from_op):
                t_cost=no_op*5*(l.index(to_op)-l.index(from_op))
            else:
                t_cost=no_op*5*(l.index(from_op)-l.index(to_op))
            return render_template('home_pass.html',point_err_p=point_err,cost=t_cost,bal=st_bal,username=unm)

@app.route("/register", methods=['POST','GET'])
def reg():
    global usern_err
    global def_us
    usern_err=''
    def_us='\b'
    if request.method=='POST':
        return render_template('reg_page.html',usern_err_p=usern_err, repass_err_p=repass_err,typesel_err_p=typesel_err)


@app.route("/register/us_check", methods=['POST', 'GET'])
def us_checks():
    global usern_err
    global def_us
    def_us=''
    usern_err=''
    if request.method=='POST':
        
        c.execute("select username from users;")
        l=[]
        for i in c:
            l.append(i)

        l=[i[0] for i in l]

        usern=request.form['username']
        if usern in l:
            usern_err=str(usern)+' already Exists'
        else:
            usern_err=str(usern)+' is Available'

        return render_template('reg_page.html',usern_err_p=usern_err, repass_err_p=repass_err,typesel_err_p=typesel_err,def_us=usern_err)

@app.route("/register/check",methods=['POST','GET'])
def reg_check():
    global usern_err
    global repass_err
    global log_err
    global typesel_err
    repass_err=''
    usern_err=''
    log_err=''
    typesel_err=''

    if request.method=='POST':

        usern=request.form['username']
        ps1=request.form['pwd1']
        ps2=request.form['pwd2']
        typ=request.form['atype']
        name=request.form['name']
        

        #check username availability
        c.execute("select username from users;")
        l=[]
        for i in c:
            l.append(i)

        l=[i[0] for i in l]

        usern=request.form['username']
        if usern in l:
            usern_err=str(usern)+' already Exists'
            return render_template('reg_page.html',usern_err_p=usern_err,repass_err_p=repass_err,typesel_err_p=typesel_err)

        if ps1!=ps2:
            repass_err="Passwords Do Not Match! Please try again!"
            return render_template('reg_page.html',usern_err_p=usern_err,repass_err_p=repass_err,typesel_err_p=typesel_err)

        if typ=='passenger':
            ua=1
        elif typ=='public_tr':
            ua=2
        else:
            typesel_err="Please select an Account Type!"
            return render_template('reg_page.html',usern_err_p=usern_err,repass_err_p=repass_err,typesel_err_p=typesel_err)
        
            
        
        sql="insert into users(username,password,name,access) values(%s,%s,%s,%s);"
        val=(usern,ps1,name,ua)
        c.execute(sql,val)
        db.commit()

        sql="insert into account(username,balance) values (%s,%s);"
        val=(usern,0)
        c.execute(sql,val)
        db.commit()

        

        log_err='Account Registered Successfully!'
        return redirect(url_for('index'))


@app.route("/home/tickadd", methods=['POST','GET'])
def tickadd():
    global point_err
    point_err=''
    if request.method=='POST':
        to_op=request.form['to']
        from_op=request.form['from']
        no_op=int(request.form['no'])

        if l.index(to_op)>l.index(from_op):
            t_cost=no_op*5*(l.index(to_op)-l.index(from_op))
        else:
            t_cost=no_op*5*(l.index(from_op)-l.index(to_op))

        c.execute('select* from account;')
        bl=[]
        for i in c:
            bl.append(i)

        for i in bl:
            if i[0]==get_user:
                st_bal=i[1]

        if t_cost>st_bal:
            point_err='Insufficient Balance'
            return render_template('home_pass.html',point_err_p=point_err,username=unm,bal=st_bal)
        else:
            c.execute('select* from temp_tr;')
            b=[]
            for i in c:
                b.append(i)

            tr_list=[]
            for i in b:
                tr_list.append(i[0])


            t_id=randint(100000,999999)
            while t_id in tr_list:
                t_id=randint(100000,999999)

            c.execute('insert into temp_tr(tid,username,amount) values (%s,%s,%s);',(t_id,get_user,t_cost))
            db.commit()
            st_bal-=t_cost

            c.execute('update account set balance =%s where username=%s;',(st_bal,get_user))
            db.commit()

            point_err='Ticket Generated! Ticket Code :'+str(t_id)

            return render_template('home_pass.html',point_err_p=point_err,username=unm,bal=st_bal)


@app.route("/home/add_balance",methods=['POST','GET'])
def add_balance_p():
    global amt_err
    c.execute('select* from account;')
    bl=[]
    for i in c:
        bl.append(i)

    for i in bl:
        if i[0]==get_user:
            st_bal=i[1]
            break
    
    return render_template("add_balance.html",bal=st_bal,mess=amt_err)

@app.route("/home/add_balance_re", methods=['POST','GET'])
def add_re():

    global amt_err
    global st_bal
    amt_err=''
    if request.method=='POST':
            amt=int(request.form['addb'])

            if amt<=0:
                amt_err='Please enter a valid amount!'
                return redirect(url_for("add_balance_p"))
            else:
                c.execute('select* from account;')
                bl=[]
                for i in c:
                    bl.append(i)

                for i in bl:
                    if i[0]==get_user:
                        st_bal=i[1]
                        break
                
                c.execute('update account set balance=%s where username=%s;',(amt+st_bal,get_user))
                db.commit()
                amt_err="Money added to wallet Successfully!"
                return redirect(url_for("add_balance_p"))

@app.route('/home_route',methods=['POST','GET'])
def home_route():
    global st_bal
    point_err=''
    c.execute('select* from account;')
    bl=[]
    for i in c:
        bl.append(i)

    for i in bl:
        if i[0]==get_user:
            st_bal=i[1]
            break
    return render_template('home_pass.html',point_err_p=point_err,cost='',bal=st_bal,username=unm)

@app.route("/home_tc/tid_c",methods=['POST','GET'])
def tidc():
    global tid_err
    global st_bal
    if request.method=='POST':
        tid=request.form["tid_en"]

        c.execute("select* from temp_tr")
        bl=[]
        lt=[]
        for i in c:
            bl.append(i)
        for i in bl:
            if i[0]==tid:
                lt=i
                break

        if lt==[]:
            tid_err='Unknown Transaction ID'
            return render_template('home_tc.html',username=get_user,bal=st_bal,tid_err_p=tid_err)
        else:

            c.execute("select* from temp_tr")
            bl=[]
            amt=0
            for i in c:
                bl.append(i)
            for i in bl:
                if i[0]==tid:
                    amt=i[2]
                    break

            c.execute("insert into completed_tr (tid,username,tc_name,amount) values(%s,%s,%s,%s)",(i[0],i[1],get_user,i[2]))
            db.commit()

            c.execute("delete from temp_tr where tid=%s;",(i[0],))
            db.commit()

            c.execute('select* from account;')
            bl=[]
            for i in c:
                bl.append(i)

            for i in bl:
                if i[0]==get_user:
                    st_bal=i[1]
                    break

            
            c.execute("update account set balance=%s where username=%s;",(st_bal+amt,get_user))
            db.commit()
            c.execute('select* from account;')
            bl=[]
            for i in c:
                bl.append(i)

            for i in bl:
                if i[0]==get_user:
                    st_bal=i[1]
                    break
            tid_err="Verified Payment"
            return render_template('home_tc.html',username=get_user,bal=st_bal,tid_err_p=tid_err)


@app.route('/home_pass/view',methods=['POST','GET'])
def pass_view():
    c.execute('select tid,amount from temp_tr where username=%s',(get_user,))
    d1=c.fetchall()
    c.execute('select tid,amount from completed_tr where username=%s',(get_user,))
    d2=c.fetchall()
    return render_template('view_pass.html',data1=d1,data2=d2)

@app.route('/home_tc/view',methods=['POST','GET'])
def tc_view():
    c.execute('select tid,amount,username from completed_tr where tc_name=%s',(get_user,))
    d=c.fetchall()
    return render_template('view_tc.html',data=d)

@app.route('/home_route_tc',methods=['POST','GET'])
def home_route_tc():
    global st_bal
    global tid_err
    tid_err=''
    c.execute('select* from account;')
    bl=[]
    for i in c:
        bl.append(i)

    for i in bl:
        if i[0]==get_user:
            st_bal=i[1]
            break
    return render_template('home_tc.html',name=unm,bal=st_bal,tid_err_p=tid_err)    

app.run("0.0.0.0")
