from checkz_app.server import db


def db_create_all():

    db.create_all()


def db_drop_all():

    db.drop_all()