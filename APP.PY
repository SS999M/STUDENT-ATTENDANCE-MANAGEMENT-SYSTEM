from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'  # SQLite database for simplicity
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    present = db.Column(db.Boolean, default=False)

db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/mark_attendance/<int:id>')
def mark_attendance(id):
    student = Student.query.get(id)
    if student:
        student.present = not student.present
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    if name:
        student = Student(name=name)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully', 'success')
    else:
        flash('Invalid input. Please enter a name.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
