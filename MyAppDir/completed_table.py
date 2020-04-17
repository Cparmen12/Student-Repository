from flask import Flask, render_template
import sqlite3
from typing import Dict 

DB_FILE: str = '/Users/Christopher/Desktop/HW11/startup.db'

app: Flask = Flask(__name__)

@app.route('/completed')
def completed_courses()-> str:
    query = """ select students.name, students.CWID, grades.course, grades.grade, instructors.Name
                from students join grades on students.cwid = grades.StudentCWID
                join instructors on instructors.CWID = grades.InstructorCWID
                order by students.name"""
    db: sqlite3.Connection = sqlite3.connect(DB_FILE)                

    # convert the query results into al ist of dictionaries to pass to the template 
    data: Dict[str,str] = \
        [{'student': student, 'CWID': cwid, 'Course': course, 'Grade': grade, 'Instructor': instructor}
        for student, cwid, course, grade, instructor in db.execute(query)]

    db.close() # close the connection to close the database 

    return render_template('student_courses.html',
                            title = 'Stevens Repository',
                            table_title = "Studnet, Course, Grade, and Instructor ",
                            students = data)

app.run(debug=True)

