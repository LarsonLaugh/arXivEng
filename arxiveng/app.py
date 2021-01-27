from flask import Flask, request, render_template, url_for, flash, redirect, session, g
import arxiv
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, SelectField,
RadioField,TextAreaField, IntegerField)
from wtforms.validators import (InputRequired, Email, Length, DataRequired, EqualTo, 
ValidationError, NumberRange)




# module
app = Flask(__name__)

app.config['SECRET_KEY'] = b" '-MB\xa0V\x1f\xdf;&\x11\x13R\xb0\xf5|\xa3\x88\xb8D\xca]A"
# route


@app.route('/',methods = ['POST','GET'])
def search():
    form = SearchForm()
    if request.method == 'POST':
        papers = arxiv.query(
            query = form.keyword.data,
            max_results = form.max_results.data,   
        )
        if papers:
            flash('Your search request has been accepted', 'success')    
            return render_template('render_results.html', papers = papers)
        else:
            flash('Your search request has been rejected', 'danger')
            return render_template('index.html',form=form)
    else:
        return render_template('index.html',form=form)


@app.route('/download', methods = ['POST','GET'])
def download():
    if request.method == 'POST':
        try:
            if request.form.getlist('download_list'):
                papers_to_download = arxiv.query(id_list=request.form.getlist('download_list'))
                for paper in papers_to_download:
                    arxiv.download(paper, dirpath ='./instance/download/')
                flash('Your download is completed.','success')
                return redirect(url_for('search'))
        except:
            flash('Your download failed.','danger')
            return redirect(url_for('search'))
    else:
        return redirect(url_for('search'))
        

# form

fields = ['author','title']

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[
                           InputRequired(), Length(max=500)])
    # field = SelectField('field', choices = [field for field in fields])
    max_results = IntegerField('Max Results',validators=[
                           InputRequired(), NumberRange(min=0, max=1000)]) 
    submit = SubmitField('Run')


class DownloadForm(FlaskForm):
    download = SubmitField('Download')
