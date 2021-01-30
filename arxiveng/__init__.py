from .app import *
app.config['SECRET_KEY'] = f'-MB\xa0V\x1f\xdf;&\x11\x13R\xb0\xf5|\xa3\x88\xb8D\xca]A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DOWNLOAD_FOLDER'] = u'./instance/download/'