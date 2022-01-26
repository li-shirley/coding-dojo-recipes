from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import model_user, model_recipe
from flask_app import bcrypt

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')

@app.route('/user/create', methods = ['post'])
def user_create():
    if not model_user.User.validate_registration(request.form):
        return redirect('/') 
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': pw_hash
    }
    user_id = model_user.User.create(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/login', methods = ['post'])
def login():
    if not model_user.User.validate_login(request.form):
        return redirect('/')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = model_user.User.get_one(data)
    all_recipes = model_recipe.Recipe.get_all()
    return render_template('dashboard.html', all_recipes=all_recipes, user=user)

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')
