from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)


with app.app_context():   #esta funcion es para mac
        db.create_all()

@app.route("/")
def home():
    tasks= Task.query.all()
    return render_template("index.html", list_tasks=tasks)


@app.route("/create_task", methods=["POST"])
def create():
    task = Task(content=request.form["content"], done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("view_task", task_id=task.id))  # Redirigir a la vista de la tarea creada CODIGO AGREGADO


@app.route("/task/<int:task_id>")  # Ruta para ver una tarea específica CODIGO AGREGADO
def view_task(task_id):
    task = Task.query.get(task_id)
    if task:
        search_url = f"https://www.google.com/search?q={task.content}"
        return redirect(search_url)  # Redirije la URL de la busqueda CODIGO AGREGADO
    else:
        return "Tarea no encontrada"
    
@app.route("/done/<id>")
def done(id):
     task = Task.query.filter_by(id=int(id)).first()
     task.done = not(task.done)
     db.session.commit()
     return redirect(url_for("home"))


@app.route("/delete/<id>")
def delete(id):
     task = Task.query.filter_by(id=int(id)).delete() #con esta funcion activara el botan Delete
     db.session.commit()
     return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=8080)
