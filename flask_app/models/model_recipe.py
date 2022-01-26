from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
DATABASE = 'recipes' 

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.time = data['time']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipes = []
            for recipe in results:
                all_recipes.append(cls(recipe))
            return all_recipes
        return []

    @classmethod 
    def create(cls, data): 
        query = "INSERT INTO recipes (name, description, instructions, time, date_made, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(time)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            recipe = cls(results[0])
            return recipe
        return []

    @classmethod
    def update_one(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, time = %(time)s, date_made = %(date_made)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)


    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 1 or len(data['description']) < 1 or len(data['instructions']) < 1:
            flash('All fields must be filled in to create a recipe.', 'err_recipe_form')
            is_valid = False
        if len(data['name']) < 3 :
            flash('Name must contain at least 3 characters.', 'err_recipe_name')
            is_valid = False
        if len(data['description']) < 3 :
            flash('Description must contain at least 3 characters.', 'err_recipe_description')
            is_valid = False
        if len(data['instructions']) < 3 :
            flash('Instructions must contain at least 3 characters.', 'err_recipe_instructions')
            is_valid = False
        if (data['time']) == "":
            flash('Please enter a date.', 'err_recipe_date_made')
            is_valid = False
        return is_valid
