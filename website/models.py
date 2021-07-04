from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
import sqlite3
from flask_admin import Admin,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required,current_user
from flask import url_for,redirect,session,abort,render_template
from flask_admin.menu import MenuLink

class Todo(db.Model):
    id =db.Column(db.Integer ,primary_key=True)
    data=db.Column(db.String(100000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id')) # one to many relationship 1 user to many todo's in small case


class User(db.Model,UserMixin): 
    id=db.Column(db.Integer ,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    firstname=db.Column(db.String(150))
    todo= db.relationship('Todo')# in capital case (name case sensitive here.)
    # to add a column you can just write *********-->engine/connection.execute('alter table table_name add column column_name String')

class Admins(db.Model,UserMixin):
    id=db.Column(db.Integer ,primary_key=True)
    name=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))

class myModelView(ModelView):
    print(current_user)
    b=False 
    def is_accessible(self):
        return myModelView.b

class LoginMenuLink(MenuLink):
    def is_accessible(self):
        return not myModelView.b

class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return myModelView.b            

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        check=myModelView.b
        users=User.query.count()
        todos=Todo.query.count()
        return self.render('admin/index.html', check=check, users=users, todos=todos)

# Also, you can change the root url from /admin to / with the following:

# admin = Admin(
#     app,
#     index_view=AdminIndexView(
#         name='Home',
#         template='admin/myhome.html',
#         url='/'
#     )
# )

#*********comment the part below
# def create_admin():
#     name="XYOUXWILLXDIE"
#     password="lowkeycutgee"
#     connection =sqlite3.connect('database.db', check_same_thread=False)
#     cursor=connection.cursor()
#     #SQL query
#     cursor.execute(""" select password from Admins where name='{name}'""".format(name = name))
#     #takeout important part of result after query exec 
 
#     exist = cursor.fetchone()  
#     if exist is None:
#         cursor.execute("""insert into Admins (name,password) values('{name}', '{password}')""".format(name=name,password=password)) 
#         connection.commit()
#         cursor.close()
#         connection.close()
#     else:
#         pass
