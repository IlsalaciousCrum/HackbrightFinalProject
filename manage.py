#!/usr/bin/kind_env python

'''Launches the app and application tasks'''

import os
from app import create_app, db
from app.models import (User, Profile, Friend, ProfileIntolerance, Intolerance,
                        Diet, Cuisine, Course, IngToAvoid, PartyGuest, Party,
                        RecipeCard, PartyRecipes)
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from jinja2 import StrictUndefined
from flask_mail import Mail

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# StrictUndefined raises an error.

app.jinja_env.undefined = StrictUndefined


def make_shell_context():
    '''This function loads the model into a shell'''

    return dict(app=app, db=db, User=User, Profile=Profile, Friend=Friend,
                ProfileIntolerance=ProfileIntolerance, Intolerance=Intolerance,
                Diet=Diet, Cuisine=Cuisine, Course=Course, IngToAvoid=IngToAvoid,
                PartyGuest=PartyGuest, Party=Party, RecipeCard=RecipeCard,
                PartyRecipes=PartyRecipes)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
PORT = int(os.environ.get("PORT", 5000))
server = Server(host="0.0.0.0", port=PORT, use_debugger=True, use_reloader=True)

manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment tasks."""

    from flask.ext.migrate import upgrade
    from app.seed import LoadSeedData, LoadTestPeople

    # migrate database to latest revision
    upgrade()

    LoadSeedData()
    LoadTestPeople()

if __name__ == '__main__':
    manager.run()
