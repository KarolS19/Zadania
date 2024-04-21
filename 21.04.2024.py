import sqlite3
from faker import Faker
import random
import datetime


fake = Faker()

conn = sqlite3.connect('academic_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE Students (
        student_id INTEGER PRIMARY KEY,
        name TEXT,
        group_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE Groups (
        group_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE Lecturers (
        lecturer_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE Subjects (
        subject_id INTEGER PRIMARY KEY,
        name TEXT,
        lecturer_id INTEGER,
        FOREIGN KEY (lecturer_id) REFERENCES Lecturers(lecturer_id)
    )
''')

cursor.execute('''
    CREATE TABLE Grades (
        grade_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject_id INTEGER,
        grade REAL,
        date TEXT,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
    )
''')

groups = [(1, 'Group A'), (2, 'Group B'), (3, 'Group C')]
cursor.executemany('INSERT INTO Groups (group_id, name) VALUES (?, ?)', groups)

students = [(i, fake.name(), random.randint(1, 3)) for i in range(1, 51)]
cursor.executemany('INSERT INTO Students (student_id, name, group_id) VALUES (?, ?, ?)', students)

lecturers = [(1, fake.name()), (2, fake.name()), (3, fake.name())]
cursor.executemany('INSERT INTO Lecturers (lecturer_id, name) VALUES (?, ?)', lecturers)

subjects = [(i, fake.word(), random.randint(1, 3)) for i in range(1, 9)]
cursor.executemany('INSERT INTO Subjects (subject_id, name, lecturer_id) VALUES (?, ?, ?)', subjects)

grades = []
for student_id in range(1, 51):
    for subject_id in range(1, 9):
        for _ in range(random.randint(1, 20)):
            grade = random.uniform(2, 5)
            date = fake.date_between(start_date='-1y', end_date='today')
            grades.append((student_id, subject_id, grade, date))

cursor.executemany('INSERT INTO Grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)', grades)

conn.commit()
conn.close()
