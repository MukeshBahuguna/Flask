from website import create_app
app=create_app()

if __name__=='__main__':
    app.run(host="0.0.0.0",port=7000,debug=True)

#link for the app :  https://todo-flask-webapp.herokuapp.com