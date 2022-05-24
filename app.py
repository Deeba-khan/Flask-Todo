from operator import methodcaller
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  #so this telling our app where our database is located *test.db* and everything going to store in this test.db file. [3 slash for relative path and 4 slash for exact path]
db =  SQLAlchemy(app)  #Initializing the database


class Todo(db.Model):    #creating model calling it *todo*
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) 
    '''creating text cloumn and calling it *content*
    set nullable equal to false, cause we dont want this to be blank, we dont want user to create a new task, and then just leave the content of that task empty.'''
    completed = db.Column(db.Integer, default=0)
    date_created =  db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id #It's return the task and "%r" return the id of that task. 


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that tasks'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that tasks'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    # Create table or any other changes before start
    db.create_all()

    # Start
    app.run(debug=True)
