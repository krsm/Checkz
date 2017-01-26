#!/usr/bin/env python
import os
import subprocess
import sys

from checkz_app import db, create_app

from flask_script import Manager

manager = Manager(create_app)

@manager.command
def createdb(drop_first=False):
    """Creates the database."""
    if drop_first:
        db.drop_all()

if __name__ == '__main__':
    # if sys.argv[1] == 'test' or sys.argv[1] == 'lint':
    #     # small hack, to ensure that Flask-Script uses the testing
    #     # configuration if we are going to run the tests
    #     os.environ['FLACK_CONFIG'] = 'testing'
    manager.run()