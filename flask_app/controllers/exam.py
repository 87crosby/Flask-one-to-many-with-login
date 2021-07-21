from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.users import User
from flask_app.models.show import Show

@app.route('/shows')
def exam_index():
    if 'user_id' not in session:
        return redirect('/')

    shows = Show.get_all_shows()
    return render_template('shows.html', shows = shows)

@app.route('/shows/new')
def new_show():
    return render_template('new_show.html')

@app.route('/shows/create', methods = ['POST'])
def create_show():
    if Show.validate_show(request.form):
        data = {
            'title' : request.form['title'],
            'description' : request.form['description'],
            'date' : request.form['date'],
            'users_id': session['user_id']
        }
        Show.create_show(data)
        return redirect('/shows')
    return redirect('/shows/new')

@app.route('/shows/<int:show_id>')
def view_show(show_id):
    show = Show.get_show_by_id({'id': show_id})
    return render_template('show_info.html', show=show)

@app.route('/shows/<int:show_id>/edit')
def edit_show(show_id):
    show = Show.get_show_by_id({'id': show_id})
    if session['user_id'] != show.users_id:
        return redirect(f'/shows/{show_id}')
    return render_template('edit_show.html', show = show)

@app.route('/shows/<int:show_id>/update', methods = ['POST'])
def update_show(show_id):
    data = {
        'title': request.form['title'],
        'description' : request.form['description'],
        'date' : request.form['date'],
        'id' : show_id
    }
    Show.update_show(data)
    return redirect('/shows')

@app.route('/shows/<int:show_id>/delete')
def delete_show(show_id):

    # add check if user can perfrom action
    show = Show.get_show_by_id({'id':show_id})
    return render_template('delete_show.html', show = show)

@app.route('/shows/<int:show_id>/confirm')
def confirm_delete(show_id):
    Show.delete_show({'id':show_id})
    return redirect('/shows')