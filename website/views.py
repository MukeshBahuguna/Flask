from flask import Blueprint,render_template,request,flash,jsonify,redirect
from flask_login import login_required,current_user 
from .models import Todo,Admins
from . import db
import json
#create blueprints(allows us to have multiple urls or routes not in just one file but multiple files. )
views=Blueprint('views', __name__)

@views.route('/',methods=["GET","POST"])
@login_required
def home():
    if request.method=="POST":
        note=request.form.get("note")
        check=Todo.query.filter_by(data=note).first()
        
        if len(note)<1:
            flash("Note is too short!" ,category='error')
        else:
            if check is not None:
                if check.data==note:
                    pass# I could have written ""if check is None:"" here after this!! for flashing and stuff
            else:
                new_note=Todo(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash("Note added!" , category='success')
    return render_template("home.html",user=current_user)

@views.route('/delete-note',methods=["POST"])
def delete_note():
    note=json.loads(request.data) #python dict object
    noteId= note['noteId']
    note =Todo.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #if signed or logged in
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route("/update", methods=["GET","POST"])
def update():
    if request.method=="POST":
        oldnote = request.form.get("oldnote")
        newnote = request.form.get("newnote")
        note = Todo.query.filter_by(data=oldnote).first()
        note.data = newnote
        db.session.commit()
        return redirect("/")

    return render_template("update.html",user=current_user)
    

