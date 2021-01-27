from flask import Flask, request, render_template, url_for, flash
import arxiv
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, SelectField,
RadioField,TextAreaField)
from wtforms.validators import (InputRequired, Email, Length, DataRequired, EqualTo, 
ValidationError)





# module
app = Flask(__name__)


# route

@app.route('/',methods = ['POST','GET'])
def search():
    if request.method == 'POST':
        form = SearchForm()
        flash('Your search results has been executed', 'success')
    else:
        return render_template('index.html',form=form)



# form
class SearchForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Sign In')
