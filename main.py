from peewee import *
from model import *
from flask import Flask, request, url_for, redirect, render_template


DATABASE =  'userstory.db'
DEBUG = True
SECRET_KEY = 'verysecretkey'


app = Flask(__name__)
app.config.from_object(__name__)
db = SqliteDatabase(DATABASE)


class UserStory(Model):
    pass
