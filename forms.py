from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class UploadRecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    preparation_instructions = TextAreaField('Preparation Instructions', validators=[DataRequired()])
    serving_instructions = TextAreaField('Serving Instructions', validators=[DataRequired()])
    image_file = FileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField('Upload Recipe')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, FileField
# from wtforms.validators import InputRequired
# from flask_wtf.file import FileAllowed
#
# class RecipeForm(FlaskForm):
#     name = StringField('Recipe Name', validators=[InputRequired()])
#     ingredients = TextAreaField('Ingredients', validators=[InputRequired()])
#     preparation_instructions = TextAreaField('Preparation Instructions', validators=[InputRequired()])
#     serving_instructions = TextAreaField('Serving Instructions', validators=[InputRequired()])
#     image = FileField('Image File', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
