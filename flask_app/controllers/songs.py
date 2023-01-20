from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.song import Song

@app.route('/new') #form for creating new song.
def new():
    if "user_id" not in session:
        redirect('/')
    return render_template('new_song.html')

@app.route('/create',methods=['POST']) #process creating song form.
def create():
    if not Song.is_valid(request.form):
        return redirect('/new')
    Song.save(request.form)
    return redirect('/dashboard')

@app.route('/update/<int:id>') #show the update form.
def update(id):
    if "user_id" not in session:
        redirect('/')

    return render_template('edit_song.html', song=Song.get_by_id({"id":id}))

@app.route('/change',methods=['POST']) #process update song form.
def change():
    if not Song.is_valid(request.form):
        return redirect(f'/update/{request.form["id"]}')
    Song.update_song(request.form)

    return redirect('/dashboard')

@app.route('/songs/<int:id>') #show one song.
def show(id):
    if "user_id" not in session:
        redirect('/')

    return render_template('show_one.html', user=User.get_by_id({"id": session['user_id']}),song=Song.get_by_id({"id":id}))

@app.route('/songs/delete/<int:id>') #delete one song.
def destroy(id):
    Song.delete_song_by_id(id)
    return redirect ('/dashboard')



