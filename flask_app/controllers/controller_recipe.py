from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models import model_user, model_recipe

@app.route('/recipe/new')
def recipe_new():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = model_user.User.get_one(data)
    return render_template('recipe-create.html', user=user)

@app.route('/recipe/create', methods=['post'])
def create():
    if 'user_id' not in session:
        return redirect('/')
    if not model_recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        **request.form,
        'time' : int(request.form['time']),
        'user_id' : session['user_id']
    }
    model_recipe.Recipe.create(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def recipe_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_data = {
        'id' : id
    }
    data = {
        'id' : session['user_id']
    }
    user = model_user.User.get_one(data)
    recipe = model_recipe.Recipe.get_one(recipe_data)
    return render_template('recipe-edit.html', user=user, recipe=recipe)

@app.route('/recipe/update', methods=['post'])
def recipe_update():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        **request.form,
        'id' : request.form['id']
    }
    if not model_recipe.Recipe.validate_recipe(request.form):
        return redirect(url_for('recipe_edit', id = data['id'])) 
    model_recipe.Recipe.update_one(data)
    return redirect('/dashboard')



