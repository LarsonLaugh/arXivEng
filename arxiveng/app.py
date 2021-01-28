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

@app.route('/')
def search():
    form_kw = KSearchForm()
    form_adv = ASearchForm()
    return render_template('index.html',form_kw=form_kw, form_adv = form_adv)



@app.route('/kwsearch',methods = ['POST'])
def kwSearch():
    form = dict(request.form)
    papers = arxiv.query(
        query = form.get('keyword'),
        max_results = max_result_trans(form.get('max_results')),  
        sort_by = form.get('sort_by'),
        sort_order = form.get('sort_order')
    )
    if papers:
        clear_cache()
        build_cache(papers)
        flash('Your keyword engineer is on', 'success') 
        return render_template('render_results.html', papers = Paper.query.all(), title ="Search Results")
    else:
        flash('Sorry. Your search request has been rejected', 'danger')
        return render_template('index.html',form_kw=form_kw, form_adv = form_adv)



@app.route('/advsearch',methods = ['POST'])
def advSearch():
    form = dict(request.form)
    papers = arxiv.query(
        query = render_query(form.get('field1_input'),form.get('field1_choice'),form.get('logic12'),form.get('field2_input'),form.get('field2_choice')),
        max_results = max_result_trans(form.get('max_results')),  
        sort_by = form.get('sort_by'),
        sort_order = form.get('sort_order')
    )
    if papers:
        clear_cache()
        build_cache(papers)
        flash('Your advanced engineer is on', 'success')  
        return render_template('render_results.html', papers = Paper.query.all(), title ="Search Results")
    else:
        flash('Sorry. Your search request has been rejected', 'danger')
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

class KSearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[
                           InputRequired(), Length(max=500)])
    # field = SelectField('field', choices = [field for field in fields])
    max_results = SelectField('max_results', choices=["default","20","50","100","200"])
    sort_by = SelectField('Sorted By', choices=["relevance","lastUpdatedDate","submittedDate"])
    sort_order = SelectField('Sort Order', choices=["ascending","descending"])
    submit = SubmitField('Go')


class ASearchForm(FlaskForm):
    field1_input = StringField('Field1Input', validators=[
                           InputRequired(), Length(max=500)])
    field1_choice = SelectField('Field1Choice', choices=["author","title","abstract","comment","subject"])
    logic12 = SelectField('logic12', choices=["AND","OR","ANDNOT"])
    field2_input = StringField('Field2Input', validators=[
                           InputRequired(), Length(max=500)])
    field2_choice = SelectField('Field2Choice', choices=["author","title","abstract","comment","subject"])

    max_results = SelectField('max_results', choices=["default","20","50","100","200"]) 

    sort_by = SelectField('Sorted By', choices=["relevance","lastUpdatedDate","submittedDate"])
    sort_order = SelectField('Sort Order', choices=["ascending","descending"])
    submit = SubmitField('Go')


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

def shortcut(field):
    if field == "author":
        return "au:"
    elif field == "title":
        return "ti:"
    elif field == "abstract":
        return "abs:"
    elif field == "comment":
        return "co:"
    elif field == "subject":
        return "cat:"
    else:
        return None



def render_query(field1_input,field1_choice,logic12,field2_input,field2_choice):
    return shortcut(field1_choice)+ field1_input +' '+ logic12 + ' '+ shortcut(field2_choice) + field2_input


def max_result_trans(result):
    if result == "default":
        return 10
    else:
        return int(result)