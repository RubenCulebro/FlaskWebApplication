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
