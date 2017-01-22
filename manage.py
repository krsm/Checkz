#!/usr/bin/env python
import os
import subprocess
import sys

from checkz_app import db


def db_create_all():

    db.create_all()


def db_drop_all():

    db.drop_all()

if __name__ == "__main__":

    db_create_all()