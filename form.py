from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField

class ImageForm(FlaskForm):
    image = FileField('Upload Your Image',validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')