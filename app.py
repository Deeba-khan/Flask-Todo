from flask import Flask, render_template, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  #so this telling our app where our database is located *test.db* and everything going to store in this test.db file.
db =  SQLAlchemy(app)  #Initializing the database


class TODO(db.Model):    #creating model calling it *todo*
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) 
    '''creating text cloumn and calling it *content*
    set nullable equal to false, cause we dont want this to be blank, we dont want user to create a new task, and then just leave the content of that task empty.'''
    completed = db.Column(db.Integer, default=0)
    data_created =  db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id #It's return the task and "%r" return the id of that task. 


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)