from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    complete = db.Column(db.Boolean, default=False)

#route to add todo
@app.route('/add_todo', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    new_todo = ToDo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

#route to delete todo
@app.route('/delete_todo/<int:todo_id>')
def delete_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

#route to update todo
@app.route('/update_todo/<int:todo_id>')
def update_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_todo/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
        todo = ToDo.query.get_or_404(todo_id)
        if request.method == 'POST':
            new_title = request.form.get('title')
            if new_title:
                todo.title = new_title
                db.session.commit()
                return redirect(url_for('index'))
        return render_template('edit_todo.html', todo=todo)

@app.route("/")
def index():
    todos = ToDo.query.all()
    edit_id = request.args.get("edit_id", type=int)
    return render_template("base.html", todos=todos, edit_id=edit_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)