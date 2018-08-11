from flask import  render_template,url_for,Response,flash,redirect,request
from dynamic import app,db,bcrypt
from dynamic.forms import RegistrationForm,LoginForm
from flask_login import login_user, current_user, logout_user, login_required


from dynamic.models import User, Post

import time
import subprocess
from time import sleep
import os


posts2 = [
    {
        'author':'AgrimSingh',
        'title':'3457'
    },
    
]

@app.route('/')
@app.route("/all")
def home():
    #posts=Post.query.all()
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template('index.html',posts=posts,posts2=posts2)#posts2=posts2

@app.route("/user")
def inventory():
    #page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).filter_by(author=current_user)

    return render_template('index2.html',posts=posts,posts2=posts2)#posts2=posts2


# 
# def github_login():
#     if not github.authorized:
#         return redirect(url_for('github.login'))
#     account_info = github.get('/user')
#     if account_info.ok:
#         account_info_json = account_info.json()
#         return'<h1>Your Github name is {}'.format(account_info_json['login'])
#     return'<h1>Requst Failed</h1>'


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            subprocess.Popen('git clone http://gitlab.zycus.net/root/training.git',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            flash('Repo list taken check in account', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    subprocess.Popen('rm -r training',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    lst = []
    files = []
    if not os.path.exists('/home/site/training/'+ current_user.username ):

        flash('No files available for this user ','Danger')
        lst=[x for x in os.listdir('/home/site/default/')if x.endswith(".yml")]
        for i in lst:
            #if i.endswith('.yml'):
            files.append(open('/home/site/default/'+ i).read())
        posts=zip(lst,files)
            #lst=[x for x in os.listdir('/home/site/training/Agrim.Singh/') if x.en$
        # for i in range(0,len(list)):
        #     x= files[i]
        #     print list[i]
        #     print x

        #lst=[x for x in os.listdir('/home/site/training/Agrim.Singh/') if x.endswith(".yml")]
        #lst=os.path.join('training/'+ current_user.username ,lst)

    else:
        lst=[x for x in os.listdir('/home/site/training/'+ current_user.username ) if x.endswith(".yml")]
        for i in lst:
            
            files.append(open('/home/site/training/'+current_user.username+'/'+ i).read())
        posts=zip(lst,files)
    #lst=os.listdir('/home/site/training/Agrim.Singh')#{{ current_user.username }}
    return render_template('account.html', title='Account',posts=posts)

@app.route("/post")
def new_post():
    return render_template('post.html', title='Account',posts=posts)




@app.route('/save', methods=['GET', 'POST'])
def save():
    a= request.form['path']
    b= request.form['file']
    if os.path.exists('/home/site/training/'+ current_user.username):
        open('/home/site/training/'+current_user.username+'/'+a,"w+").write(b)
    else:
        open('/home/site/default/'+a,"w+").write(b)

    flash('File Edited', 'success')
    return redirect(url_for('account'))

#@app.route('/index/<string:path>&<file>/')
@app.route('/index/path')
#@login_required

def index():
    # if request.method == 'POST':
    #     result = request.form[path]
    #     cmd='ansible-playbook ',result
     
    
    def inner(command,current_user):
        st=""
        user=int(current_user)
    	p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    	for line in iter(p.stdout.readline, b''):
    		if line: # Don't print blank line
    			yield line + '<br/>\n'
                st="%s%s"%(st,line)
        #This ensures the process has completed, AND sets the 'returncode' attr
    	while p.poll() is None:                                                                                                                                        
        	sleep(.1) #Don't waste CPU-cycles
    	# Empty STDERR buffer
    	err = p.stderr.read()
    	if p.returncode != 0:
            st="%sError: %s"%(st,err)
            yield("Error: " + str(err))
            # The run_command() function is responsible for logging STDERR
        print st,command#,\
        print current_user
        task=Post(title=command,content=st,user_id=user)  
        db.session.add(task)
        db.session.commit()  
        #simulate a long process to watch
    if os.path.exists('/home/site/training/'+ current_user.username):
        cmd='ansible-playbook training/'+ current_user.username+'/'+request.args["path"] 
    else:
        cmd='ansible-playbook /home/site/default/'+request.args["path"] 

    return Response(inner(cmd,current_user.id), mimetype='text/html')


# @app.route('/display')
# def display():
#     query=request.args["path"]
#     print query
#     flash (url_for('index',path=query ),'success')
#     op=inner('ansible-playbook /home/site/default/'+query)
#     return redirect(url_for('account')op=op)
