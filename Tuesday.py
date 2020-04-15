import sqlite3
from prettytable import PrettyTable
def Tue():
    try: 
        db: sqlite3.Connection = sqlite3.connect('/Users/Christopher/Desktop/HW11/startup.db')
    except sqlite3.OperationalError as e:
        print(e)
    else: 
        pt: PrettyTable = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])
        for tup in db.execute("""
                    select students.name, students.CWID, grades.course, grades.grade, instructors.Name
                    from students join grades on students.cwid = grades.StudentCWID
                    join instructors on instructors.CWID = grades.InstructorCWID
                    order by students.name"""):
            pt.add_row(tup)
        print(pt)    

if __name__ == "__main__":
    Tue()
