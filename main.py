from peewee import *
from flask import Flask, request, url_for, redirect, render_template


DATABASE = 'userstory.db'
DEBUG = True
SECRET_KEY = 'verysecretkey'


app = Flask(__name__)
app.config.from_object(__name__)
db = SqliteDatabase(DATABASE)


class UserStory(Model):
    story_title = CharField()
    user_story = TextField()
    criteria = TextField()
    b_value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        database = db


def create_tables():
    db.connect()
    db.create_tables([UserStory], safe=True)


@app.before_request
def connect_db():
    db.connect()


@app.after_request
def close_db(respond):
    db.close()
    return respond


@app.route('/')
def homepage():
    return story_list()


@app.route('/list')
def story_list():
    userstories = UserStory.select()
    return render_template('list.html', userstories=userstories)


@app.route('/story/', methods=['GET', 'POST'])
def story_page():
    if request.method == "POST": #executes the query if we want to submit a user story. on the right of the = are the corresponding HTML names
        UserStory.create(story_title = request.form['story_title'], user_story=request.form['user_story'], criteria=request.form['criteria'],
                          b_value=request.form['b_value'], estimation=request.form['estimation'], status=request.form['status'])
        return redirect(url_for('story_list'))
    else: # show the prev. sent data
        return render_template('form.html', prev_data='', submit='Create')


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def update_story(story_id):
    if request.method == 'POST':
        UserStory.update(story_title=request.form['story_title'], user_story=request.form['user_story'], criteria=request.form['criteria'],
                         b_value=request.form['b_value'], estimation=request.form['estimation'],
                         status=request.form['status']).where(UserStory.id == story_id).execute()
        return redirect(url_for('homepage'))
    else:
        prev_data = UserStory.get(UserStory.id == story_id)
        return render_template('form.html', prev_data=prev_data, submit='Update')


@app.route('/delete/<story_id>', methods=['GET'])
def delete_story(story_id):
    UserStory.delete().where(UserStory.id == story_id).execute()
    return redirect(url_for('homepage'))


# Runs the stuff from this module
if  __name__ == '__main__':
    create_tables()
    app.run()
