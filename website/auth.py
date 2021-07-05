from flask import Blueprint,render_template,url_for,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user , login_required, logout_user ,current_user 
from .models import User,Todo,Admins#,myModelView
from flask_admin.contrib.sqla import ModelView
#create blueprints

auth=Blueprint('auth', __name__)

@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')

        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!", category="success" )
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again.",  category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)


# @auth.route('/adminlogin',methods=["GET","POST"])
# def adminlogin():
#     if request.method=="POST":
#         name=request.form.get('name')
#         password=request.form.get('password')

#         admin= Admins.query.filter_by(name=name).first()
#         if admin:
#             if admin.password==password:
#                 myModelView.b=True
#                 return redirect('/admin')
#             else:
#                 return "Wrong Password Admin-san!!"
#         else:
#             return "You are not authorized!"
#     return render_template("opadmin.html")

# @auth.route('/adminlogout',methods=["GET","POST"])
# def adminlogout():
#     myModelView.b=False
#     return redirect('/admin')
 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstname=request.form.get('firstname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user= User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!.",category="error" )
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.',category='error')
            
        elif len(firstname)<2:
            flash('Firstname must be greater than 1 character.',category='error')
        elif len(password1)<7:
            flash('Password must be greater than 7 characters.',category='error')
        elif password1!=password2:
            flash('Passwords don\'t match',category='error')
        else:
            new_user=User(email=email, password=generate_password_hash(password1,method='sha256'),firstname=firstname)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))
            #add user to database
    return render_template("signup.html", user=current_user)


