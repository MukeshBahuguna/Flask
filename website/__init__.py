from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink


db=SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY']= 'cutgee yourp'
    app.config["SQLALCHEMY_DATABASE_URI"]= f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)
    
    #registering the blueprints
    from .views import views
    from .auth import auth
    
    from .models import User,Todo,MyHomeView#,myModelView,LoginMenuLink,LogoutMenuLink
    create_database(app)
    # create_admin() #this was here to create an admin 
    admin=Admin(app,name="Admin Dashboard",index_view=MyHomeView(),template_mode="bootstrap3")
    # admin.add_view(myModelView(User,db.session))
    # admin.add_view(myModelView(Todo,db.session))
    # admin.add_link(LogoutMenuLink(name='Logout', category='', url="/adminlogout"))
    # admin.add_link(LoginMenuLink(name='Login', category='', url="/adminlogin"))


    login_manager=LoginManager()
    login_manager.login_view ='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))# looks for the primary key by default unlike--> User.query.filter_by(email=email)
    

    app.register_blueprint(views, url_prefix='/')# prefix in the url(added in url for a specific page)
    app.register_blueprint(auth, url_prefix='/')
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


