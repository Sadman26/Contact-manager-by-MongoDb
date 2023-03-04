from flask import *
from pymongo import MongoClient
from bson.objectid import ObjectId
app.secret_key = 'my_secret_key'
client=MongoClient('localhost' , 27017)
c=client['test']
db=c['personx']
db2=c['loginx']
app = Flask(__name__,template_folder='temp')
app.secret_key='secret'
@app.route('/home')
def index():
        xyz=session['user']
        persons=list(db.find({"user":xyz}))
        return render_template('index.html',result=persons)
@app.route('/add',methods=['POST'])
def add():
        if request.method=='POST':
                name=request.form['name']
                num=request.form['num']
                xyz=session['user']
                res=db.insert_one({'name':name,'num':num,'user':xyz})
                idx=res.inserted_id
                db2.update_one(
                        {'username':xyz},
                        {'$push':{'personx':idx}}
                )
                return redirect(url_for('index'))
        return render_template('index.html')
@app.route('/edit/<id>',methods=['POST','GET'])
def edit(id):
        if request.method=='POST':
                name=request.form['name']
                num=request.form['num']
                db.update_one({'_id':ObjectId(id)},{'$set':{'name':name,'num':num}})
                return redirect(url_for('index'))
        person=db.find_one({'_id':ObjectId(id)})
        return render_template('edit.html',result=person)
@app.route('/delete/<id>')
def delete(id):
        db.delete_one({'_id':ObjectId(id)})
        return redirect(url_for('index'))
@app.route('/signup',methods=['POST','GET'])
def signup():
        if request.method=='POST':
                username=request.form['username']
                password=request.form['password']
                session['user']=username
                db2.insert_one({'username':username,'password':password})
                return redirect(url_for('index'))
        return render_template('signup.html')
@app.route('/',methods=['POST','GET'])
def login():
        if request.method=='POST':
                username=request.form['username']
                password=request.form['password']
                session['user']=username
                userx=db2.find_one({'username':username,'password':password})
                if userx:
                        return redirect(url_for('index'))
                else:
                        return redirect(url_for('login'))
        return render_template('login.html')
@app.route('/logout')
def logout():
        session.pop('user',None)
        return redirect(url_for('login'))
app.run(debug=True)