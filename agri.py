from flask import Flask,render_template,url_for,redirect,request,flash,session,g,Response
from flask_bootstrap import Bootstrap
from Forms import LoginForm,RegistrationForm,ForgotPass,UploadForm,FeedbackForm,RegionForm,CropForm,DeleteCrop,DeleteUser
from Mail import SendMail
from flask_mysqldb import MySQL
import os
import jinja2
from flask_pymongo import PyMongo
from flask_babel import Babel
from flask_babel import _
from googletrans import Translator
import re
from ocr import text
import requests
import json
from bson.json_util import dumps


def translate(str,l):
    trans=Translator()
    s=trans.translate(str,dest=l)
    return s
        
users=[]
v=0
SECRET_KEY = os.urandom(32)
app=Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Alohomora'
app.config['MYSQL_DB'] = 'agriculture'
#app.config['MONGO_URI'] = "mongodb://localhost:27017/feedback"
app.config['MONGO_URI'] = "mongodb://localhost:27017/ayes"
mongo=PyMongo(app)
mysql = MySQL(app)
bootstrap=Bootstrap(app)
babel = Babel(app)
#csrf = CSRFProtect(app)


"""@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])"""



@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm(request.form)
    cur = mysql.connection.cursor()
    #app.jinja_env.globals.update(trans=Language.translate)
    if request.method == 'POST' and form.validate_on_submit():
        #print(form.username.data)
        #print(form.password.data)
        if(form.username.data=="admin" and form.password.data=="admin"):
            session['user']="Admin"
            return render_template('AdminPortal.html')
        cur.execute("select * from farmer where username= %s and pass= %s ",(form.username.data,form.password.data))
        account=cur.fetchone()
        if account:
            """print(account[0])
            print(account[1])
            print(account[2])
            print(account[3])"""
            session['user']=account[1]
            return redirect(url_for('portal',id=account[0],n=account[1],e=account[2],m=account[3],l=account[4]))       
        else:
            flash("Credentials Invalid!")
    #print("HERE")
    print(form.errors)
    mysql.connection.commit()       
    cur.close()
    return render_template('Login.html',title='Login',form=form)
@app.after_request
def after_request5(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response





@app.route("/addcrop",methods=["GET","POST"])
def addcrop():
    form=CropForm(request.form)
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        print(form.cname.data)
        print(form.nit.data)
        print(form.phos.data)
        print(form.pot.data)
        name=form.cname.data
        n1=float(form.nit.data)
        p1=float(form.phos.data)
        k1=float(form.pot.data)
        n=round(n1,2)
        p=round(p1,2)
        k=round(k1,2)
        cur.execute("INSERT INTO crop(crop_name,nit_req,phosp_req,potash_req) VALUES (%s, %s, %s, %s)", (name,n,p,k))
        mysql.connection.commit()
        cur.close()
        flash("Entered Successfully")
    print(form.errors)
    return render_template('AddCrop.html',form=form)
@app.after_request
def after_request9(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/deletecrop",methods=["GET","POST"])
def deletecrop():
    form=DeleteCrop(request.form)
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        print(form.name.data)
        n=form.name.data
        cur.execute("DELETE FROM crop where crop_name LIKE %s", [n])
        mysql.connection.commit()
        cur.close()
        flash("Deleted Successfully")
    print(form.errors)
    return render_template('DeleteCrop.html',form=form)
@app.after_request
def after_request10(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/deleteuser",methods=["GET","POST"])
def deleteuser():
    form=DeleteUser(request.form)
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        print(form.uname.data)
        n=form.uname.data
        cur.execute("DELETE FROM farmer where username LIKE %s", [n])
        mysql.connection.commit()
        cur.close()
        flash("Deleted Successfully")
    print(form.errors)
    return render_template('DeleteUser.html',form=form)
@app.after_request
def after_request10(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response








@app.route('/region/<id>/<n>/<e>/<m>/<l>',methods=['GET','POST'])
def region(id,n,e,m,l):
    form=RegionForm()
    cur = mysql.connection.cursor()
    if request.method=='POST' and form.validate_on_submit():
        cur.execute("select doc from farmer where username LIKE %s",[n])
        t=cur.fetchone()
        print(t)
        if t[0]==1:        
            index2 = int(form.region.data)
            region1=form.region.choices[index2-1][1]        
            cur.execute("select crops_grown from region where district_name = %s",(region1,))
            # where district = {} " .format(region1))   
            s=cur.fetchone()
            print(s)
            str1=str(s)
            print(str1)
            a=[]
            uname=session['user']
            cur.execute("select fid from farmer where username LIKE %s",[uname])
            z1=cur.fetchone()
            cur.execute("select * from land where fk_fid LIKE %s",[z1])
            z=cur.fetchone()
            cur.execute("select land_size from land where fk_fid LIKE %s",[z1])
            b=cur.fetchone()
            print(b[0])
            #str2=list(str1.split(', '))
            s=['G.nut','Cotton','Paddy','Ragi','Maize','Wheat']
            z3=[]
            z1=[]
            for i in s:
                if i in str1:
                    print(i)
                    cur.execute("select * from crop where crop_name = %s", (i,))            
                    s1=cur.fetchone()
                    z1.append(i)
                    if s1==None:
                        continue
                    else:
                        z2=[]
                        j=2
                        for k in range(3):
                        #print(z)
                        #print(s)
                            z2.append(int(z[j]-s1[j])*int(b[0]))
                            j+=1
                        mysql.connection.commit()
                        z3.append(z2)
                else:
                    continue
            r=len(z3)
            print(z1,z3)
            cur.close()
            return render_template('Recommend.html',value1=z1,value2=z3,rows=r,cols=3,i=id,name=n,email=e,mob=m,lang=l)
        else:
            flash("Document Upload not yet done.Finish that step first!")
    return render_template('Region.html',form=form,i=id,name=n,email=e,mob=m,lang=l)
@app.after_request
def after_request4(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

    
@app.route('/recommend/<value1>/<value2>',methods=['GET','POST'])
def recommend(value1,value2):
    print(value1[0])
    print(value2[0][0])    
    return render_template('Recommend.html',value1=value1,value2=value2)
@app.after_request
def after_request3(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response




@app.route("/",methods=['GET','POST'])  
def home():
    """form=LoginForm()"""
    """loader = jinja2.FileSystemLoader('templates')
    env = jinja2.Environment(autoescape=True, loader=loader)
    env.filters['translate'] = translate
    temp = env.get_template('Home.html')
    temp.render()"""
    #return render_template('Home.html')
    #print(_('Your post is now live!'))
    #app.jinja_env.globals.update(trans=Language.translate)
    return render_template('Home.html')
@app.after_request
def after_request6(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



@app.route('/logout',methods=['GET','POST'])
def logout():
    #form=LoginForm()
    print("HEREEEEE")
    session.pop('user')
    return redirect(url_for('login'))
@app.after_request
def after_request7(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


"""@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']"""




@app.route("/portal/<id>/<n>/<e>/<m>/<l>",methods=['GET','POST'])
def portal(id,n,e,m,l):
    #print (val[0])
    #print (val[1])
    #print (val[2])
    #print (val[3])
    if 'user' in session:
        return render_template("Portal.html",i=id,name=n,email=e,mob=m,lang=l)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/getfeedback",methods=['GET','POST'])
def getfeedback():
    data=mongo.db.feedback.find({},{'_id':0})
    data1 = json.loads(dumps(data))
    #data=data1[1]
    data=[]
    for row in data1:
        data.append(row['feedback'])
    return render_template('GetFeedback.html',data=data,len=len(data))



@app.route("/feedback/<id>/<n>/<e>/<m>/<l>",methods=['GET','POST'])
def feedback(id,n,e,m,l):
    form=FeedbackForm()
    if request.method == 'POST' and form.validate_on_submit():
        print("HERE")
        f=form.fd.data
        print("1")
        print (f)
        mongo.db.feedback.insert({'feedback':f })
        print("3")
        flash("Submitted Successully!")
    return render_template("Feedback.html",i=id,name=n,email=e,mob=m,lang=l,form=form)
@app.after_request
def after_request1(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/upload/<id>/<n>/<e>/<m>/<l>",methods=['GET','POST'])
def upload(id,n,e,m,l):
    form=UploadForm(request.form)
    cur = mysql.connection.cursor()
    if request.method == 'POST'and form.validate_on_submit():
        s=form.size.data
        uname=session['user']
        file=request.files['file']
        mongo.save_file(file.filename,file)
        mongo.db.images.insert({'username' : uname, 'filename' : file.filename});   
        #text(uname)
        file=open('text3.txt','r')
        file1=file.readlines()
        file.close()
        for line in file1:
            m1= re.search('Phosphorus(\D+)(\d+\.\d+)',line, re.IGNORECASE) 
            if m1:
                #print(line)
                a1=m1.group(2)
            m2= re.search('Potassium(\D+)(\d+)',line, re.IGNORECASE)
            if m2:
                #print(m1.group(1))
                if m2.group(2)=='0':
                    m2= re.search('Potassium(\D+)(\d+)(\D+)(\d+\.\d+)',line, re.IGNORECASE)
                    b1=m2.group(4)
            m3= re.search('Nitrogen(\D+)(\d+\.\d+)',line, re.IGNORECASE)
            if m3:
                print(line)
                c1=m3.group(2)
        a2=round(float(a1),2)
        b2=round(float(b1),2)
        c2=round(float(c1),2)
        s2=round(float(s),2)
        print(a2)
        print(b2)
        print(c2)
        print(s2)
        cur.execute("select fid from farmer where username LIKE %s",[uname])
        z=cur.fetchone()
        cur.execute("INSERT INTO land(land_size,nit_req,phosp_req,potash_req,fk_fid) VALUES (%s,%s,%s,%s,%s)", (s2,c2,a2,b2,z[0]))
        cur.execute("UPDATE farmer set doc=1 where username LIKE %s",[uname])
        mysql.connection.commit()
        cur.close()
        flash("Uploaded Successfully!!")
        return redirect(url_for('region',id=id,n=n,e=e,m=m,l=l)) 
    return render_template("upload.html",i=id,name=n,email=e,mob=m,lang=l,form=form)
@app.after_request
def after_request2(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response



@app.route("/forgotpass",methods=['GET','POST'])
def forgotpass():
    form=ForgotPass()
    f=LoginForm()
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        e=form.email.data
        print(e)
        cur.execute("select pass from farmer where email= %s ", (e,))
        row=cur.fetchone()
        if row:
            SendMail.mail(row[0],e)
            flash("Password sent to the registered Email Address!")
            return render_template('Login.html',form=f)
        else:
            flash("Email not registred. Try with a registered Email!")
    print(form.errors)
    mysql.connection.commit()       
    cur.close()
    return render_template('ForgotPass.html',form=form)
@app.after_request
def after_request8(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response








"""@app.route("/changepass",methods=['GET','POST'])
def changepass():
    form=ChangePass()
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        p=form.confirm.data
        value=session.pop('u', None)
        print(p)
        print(value)
        cur.execute("update farmer set pass=%s where username=%s", (p,value))
        return render_template('Home.html')
    print(form.errors)
    return render_template('ChangePass.html',form=form)"""







@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm(request.form)
    l=LoginForm()
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        print(form.name.data)
        print(form.email.data)
        print(form.mobileno.data)
        print(form.confirm.data)
        print(form.lang.data)        
        n=form.name.data
        e=form.email.data
        mob=form.mobileno.data
        password=form.confirm.data
        language=form.lang.data
        cur.execute("SELECT username from farmer")
        t=cur.fetchall()
        t1 = list(sum(t, ()))
        #print(t1[0])
        if n not in t1:           
            cur.execute("INSERT INTO farmer(username,email,mobileno,lang,pass,doc) VALUES (%s, %s, %s, %s, %s,%s)", (n,e,mob,language,password,0))
            mysql.connection.commit()
            cur.close()
            #return 'success'
            flash("Registered Successfully")
            users.append(n)        
            return render_template('Login.html',title='Login',form=l)
        else:
            flash("The username is taken!Try another username")
    print("HERE")
    print(form.errors)
    return render_template('Register.html',title='Register',form=form)
@app.after_request
def after_request8(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response







if __name__=='__main__':
    app.run(debug=True)







"""<div class="header" style="position: relative;">
            <div class="col-xs-6">
                <div class="card " >
                    <div class="card-body ">
                        <h4 class="card-title">Details:</h4>
                        
                    </div>
                </div>
            </div>
        </div>"""


