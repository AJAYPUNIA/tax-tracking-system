import sys
sys.path.insert(0, r'C:\Users\yadav\Mid_term_project')

from flask import Flask
from config import Config
from models import db, Student, Course, Grade


# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Creating tables and adding sample data within the application context
with app.app_context():
    db.create_all()  # Creates all tables

    # Add sample data
    student1 = Student(student_number="S123", name="John Doe")
    course1 = Course(course_number="C101", course_name="Data Science", credit_hours=3)
    grade1 = Grade(student=student1, course=course1, grade="A")

    db.session.add(student1)
    db.session.add(course1)
    db.session.add(grade1)
    db.session.commit()

print("Database initialized and sample data added successfully.")
