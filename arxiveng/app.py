import arxiv
from flask import Flask, request, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, SelectField,
RadioField,TextAreaField, IntegerField)
from wtforms.validators import (InputRequired, Email, Length, DataRequired, EqualTo, 
ValidationError, NumberRange)


# module
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = b" '-MB\xa0V\x1f\xdf;&\x11\x13R\xb0\xf5|\xa3\x88\xb8D\xca]A"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# route

# Register Jinja filter
app.jinja_env.filters['zip'] = zip



@app.route('/',methods = ['POST','GET'])
def search():
    form = SearchForm()
    if request.method == 'POST':
        papers = arxiv.query(
            query = form.keyword.data,
            max_results = form.max_results.data,   
        )
        if papers:
            clear_cache()
            build_cache(papers)
            flash('Your search request has been accepted', 'success') 
            return render_template('render_results.html', papers = Paper.query.all(), title ="Search Results")
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
                return render_template('render_results.html', papers = Paper.query.all(), title ="Search Results")
        except:
            flash('Your download failed.','danger')
            return render_template('render_results.html', papers = Paper.query.all(), title ="Search Results")
    else:
        return render_template('render_results.html', papers = Paper.query.all(), title ="Previous Search Results")
        

# form

fields = ['author','title']

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[
                           InputRequired(), Length(max=500)])
    # field = SelectField('field', choices = [field for field in fields])
    max_results = IntegerField('Max Results', validators=[
                            NumberRange(min=0, max=100, message="Do dot exceed 100 results")]) 
    submit = SubmitField('Run')


class DownloadForm(FlaskForm):
    download = SubmitField('Download')

# model 

class Paper(db.Model):
    __tablename__ = "papers"
    id = db.Column(db.Integer, primary_key=True) 
    paper_id = db.Column(db.String(50))
    author = db.Column(db.String(50))
    title = db.Column(db.String(200))
    publish_time = db.Column(db.String(50))
    doi = db.Column(db.String(50))
    pdf_ufl = db.Column(db.String(100))
    affiliation = db.Column(db.String(100))
    summary = db.Column(db.String(500))
    tags = db.Column(db.String(100))

    def readout_tag(self):
        if self.tags:
            return self.tags.split("#")
        else:
            return None


# util

def build_cache(papers):
    if papers:
        for paper in papers:
            paper_cache = Paper(
            paper_id = paper.get("id").split('/')[-1],
            author =  paper.get("author"),
            title = paper.get("title"),
            publish_time = paper.get("published") ,
            doi = paper.get("doi"),
            pdf_ufl = paper.get("pdf_url"),
            affiliation = paper.get("affiliation"),
            summary = paper.get("summary"),
            tags = store_tag_list([tag.get("term") for tag in paper.get("tags")]))
            db.session.add(paper_cache)
        db.session.commit()
    else:
        print(f"no paper fetched!")

def clear_cache():

    Paper.query.delete()
    db.session.commit()

def store_tag_list(tag_list):
    if tag_list:
        tag_list_str = ""
        for tag in tag_list:
            tag_list_str = tag_list_str + tag + "#"
        return tag_list_str   
    else:
        print(f"the tag_list is empty!")