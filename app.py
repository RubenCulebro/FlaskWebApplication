import os
from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
import csv
from forms import UploadRecipeForm, SearchForm
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key' # Change this to a secure key
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')

os.makedirs(app.config['SUBMITTED_DATA'], exist_ok=True)
os.makedirs(app.config['SUBMITTED_IMG'], exist_ok=True)

import os
import csv

@app.route('/remove_recipe')
def remove_recipes():
    recipes = []
    with open(os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            recipes.append({
                'name': row[0],
                'ingredients': row[1],
                'preparation': row[2],
                'serving': row[3],
                'image_path': url_for('static', filename=row[4].replace('static/', ''))
            })
    return render_template('remove_recipe.html', recipes=recipes)

@app.route('/remove_recipe/<recipe_name>', methods=['POST'])
def delete_recipe(recipe_name):
    # Finding the recipe in the CSV file and deleting it
    temp_file_path = os.path.join(app.config['SUBMITTED_DATA'], 'temp.csv')
    with open(os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'), 'r') as file, \
         open(temp_file_path, 'w', newline='') as temp_file:

        reader = csv.reader(file)
        writer = csv.writer(temp_file)
        image_path = None
        for row in reader:
            if row[0] == recipe_name:
                image_path = os.path.join(app.config['SUBMITTED_IMG'], row[4])
                continue
            writer.writerow(row)

    os.rename(temp_file_path, os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'))

    # Delete the image file if found
    if image_path and os.path.exists(image_path):
        os.remove(image_path)

    return redirect(url_for('view_recipes'))

@app.route('/search_recipes', methods=['GET', 'POST'])
def search_recipes():
    form = SearchForm()
    recipes = []
    if form.validate_on_submit():
        search_term = form.search.data
        # Specify header=None since the CSV file doesn't have a header.
        csv_file = pd.read_csv(app.config['SUBMITTED_DATA'] + 'recipes.csv', header=None)
        for index, row in csv_file.iterrows():
            # Assuming the name is in the first column (index 0) and ingredients are in the second column (index 1).
            if search_term.lower() in str(row[0]).lower() or search_term.lower() in str(row[1]).lower():
                recipes.append({'name': row[0]})
    return render_template('search_recipes.html', search_form=form, recipes=recipes)



@app.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    recipe_details = None
    try:
        with open(os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == recipe_name:
                    recipe_details = {
                        'name': row[0],
                        'ingredients': row[1],
                        'preparation_instructions': row[2],
                        'serving_instructions': row[3],
                        'image_path': url_for('static', filename=row[4].replace('static/', ''))
                        # 'image_path': url_for('static', filename=os.path.join('image_dir', row[4]))
                        # 'image_path': os.path.join(app.config['SUBMITTED_IMG'], row[4])
                    }
                    break
    except FileNotFoundError:
        pass

    if recipe_details:
        return render_template('recipe.html', recipe=recipe_details)
    else:
        return redirect(url_for('view_recipes'))  # Redirect back if recipe not found


@app.route('/view_recipes')
def view_recipes():
    recipes = []
    try:
        with open(os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                recipes.append({
                    'name': row[0],
                    'ingredients': row[1],
                    'preparation_instructions': row[2],
                    'serving_instructions': row[3],
                    'image_path': row[4]
                })
    except FileNotFoundError:
        pass

    return render_template('view_recipes.html', recipes=recipes)


# @app.route('/recipe/<int:recipe_id>', methods=['GET'])
# def recipe(recipe_id):
#     recipe_data = []
#     with open(os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'), 'r') as file:
#         reader = csv.reader(file)
#         for index, row in enumerate(reader):
#             if index == recipe_id:
#                 recipe_data = {
#                     'name': row[0],
#                     'ingredients': row[1],
#                     'preparation_instructions': row[2],
#                     'serving_instructions': row[3],
#                     'image_path': os.path.join(app.config['SUBMITTED_IMG'], row[4]), # corrected image path
#                 }
#                 break
#
#     if not recipe_data:
#         flash('Recipe not found!', 'danger')
#         return redirect(url_for('index'))
#
#     return render_template('recipe.html', recipe=recipe_data)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadRecipeForm()
    message = ""
    if form.validate_on_submit():
        # Save the image file
        image_file = form.image_file.data
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['SUBMITTED_IMG'], filename)
        image_file.save(image_path)

        # Save the recipe data to a CSV file
        recipe_data = [
            form.name.data,
            form.ingredients.data,
            form.preparation_instructions.data,
            form.serving_instructions.data,
            image_path
        ]
        with open(os.path.join(app.config['SUBMITTED_DATA'], 'recipes.csv'), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(recipe_data)

        message = "Recipe successfully uploaded!"

    return render_template('upload.html', form=form, message=message)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/')
# def index():
#     return render_template('index.html',
#                            heading_upper1='Section heading upper',
#                            heading_lower1='Section heading lower',
#                            content1='Content',
#                            heading_upper2='Section heading upper',
#                            heading_lower2='Section heading lower',
#                            content2='Content',
#                            button_link='#!',
#                            button_description='Description for intro-button mx-auto')

if __name__ == '__main__':
    app.run(debug=True)