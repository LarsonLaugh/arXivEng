from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from arxiveng import app, db


# Load the default configuration
# app.config.from_object('config.default')

# Load the configuration from the instance folder
# app.config.from_pyfile('config.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cache.db'

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
# app.config.from_envvar('APP_CONFIG_FILE')


# Create database
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()