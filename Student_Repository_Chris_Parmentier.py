# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:19:58 2020
updated on 04132020 -- fixed homework 10 additions, remaining required courses and remaining elective courses 
updated on 04142020 -- added a new student grade summary table pulled using sqlite3 from a query performed in datagrip
@author: Christopher
"""

from typing import Dict, DefaultDict,Set, List, Tuple 
from collections import defaultdict
from HW08_Chris_Parmentier_Fixed import file_reader
import os
from prettytable import PrettyTable
import sqlite3
import unittest 
 
class Major: 
    """ store everythying about a single major """
    PT_MAJOR_FIELD_NAMES = ['MAJOR', 'REQUIRED COURSES', 'ELECTIVE COURSES']
    
    def __init__(self, major: str)-> None:
        """ major stores an instance for each major on the major.txt file and pulls major, the required/elective, and the course number """ 
        self.major:str = major
        self.required: Set[str] = set() # we want these to be sets because i wasn't storing differing values with a dict in the key and value. so the dict wasn't helping us.
        self.elective: Set[str] = set()      
        
    def add_Rcourse(self, course: str) -> None: 
        """add the course to the required course dictionary """
        self.required.add(course)
        
    def add_Ecourse(self, course: str) -> None: 
        """add the course to the elective course dictionary """
        self.elective.add(course)     
        
    def info(self):
        """ tell us what we need to return for information from this major class"""         
        return[self.major, sorted(self.required), sorted(self.elective)]   

class Student: 
    """ store everythying about a single Student """
    PT_STUDENT_FIELD_NAMES = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Elective', 'GPA']

    def __init__(self, cwid: str, name: str, major: str, required: Set[str], electives: Set[str])-> None:
        """ student stores an instance for each student on the student.txt file and pulls cwid, name, major """ 
        self.cwid:str = cwid
        self.name:str = name
        self.major:str = major
        self.rem_required: Set[str] = set(required)
        self.rem_electives: Set[str] = set(electives)
        self.courses: Dict[str, str] = dict() # courses[course_name] = grade
        self.grades: int= 0
        self.gpa: int = 0
                   
    def store_course_grade(self, course: str, grade: str) -> None: 
        """Note that this student took course and earned grade """
        passing = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'} 
        self.courses[course] = grade
        grades_scale:Dict[str,float] = {'A': 4.0, 'A-': 3.75,
                        'B+': 3.25, 'B': 3.0,'B-': 2.75, 
                        'C+': 2.25,'C': 2.0, 'C-': 0,
                        'D+': 0, 'D': 0,'D-': 0, 'F': 0}
        
        if grade in grades_scale:
            grade_points = grades_scale[grade]
        # working on calculating the GPA here, but if the amount of courses taken is zero this gpa will default to zero

        self.grades += grade_points  
        if len(self.courses)!= 0:
            self.gpa = self.grades/len(self.courses)

        if grade in passing:
            if course in self.rem_required:
                self.rem_required.remove(course)
                # each student only needs one elective
                # if we see one elective then we can set the remaining elective courses to a blank container b/c there will be no electives remaining 
            elif course in self.rem_electives:
                self.rem_electives = set()      
        
    def info(self):
        """ return a list of information about me/self needed for pretty table"""
        return[self.cwid, self.name, self.major, sorted(self.courses), sorted(self.rem_required), sorted(self.rem_electives), round(self.gpa,2)]
        
class Instructor: 
    """ store everythying about a single instructor """
    PT_INSTRUCTOR_FIELD_NAMES = ['CWID', 'Name', 'Major', 'Courses', 'Students']
    
    def __init__(self, incwid: str, name: str, dept: str)-> None:
        """store structor instance class information """ 
        self.incwid:str = incwid
        self.name:str = name
        self.dept:str = dept
        self.courses: DefaultDict[str, int] = defaultdict(int)  # courses[course_name] = # of students who have taken that class 
        
    def store_course_student(self, course: str)-> None:
        """ note that instructor taught one more student in course"""
        self.courses[course] +=1
        
    def info(self): 
        """ return a list of information about me/self needed for pretty table"""
        for courses, numstud in self.courses.items(): # courses is a default dict so we have to define/grab the key and values
            return[self.incwid, self.name, self.dept, courses, numstud] # changed from return to yield to make it into a generator 
            
    def one_instructor(self):
        """Inner loop withing the instructor loop to get all the courses for one instructor"""
        for courses, numstud in self.courses.items(): # courses is a default dict so we have to define/grab the key and values
            yield[self.incwid, self.name, self.dept, courses, numstud]   
        
class Repository: 
    """ store all students, instructors for a university and print pretty tables"""    
    def __init__(self, path: str) -> None: 
        """ store all students, instructors, 
            read students.txt, grades.txt, instructors.txt
            print pretty tables
        """
        self.path: str = path
        self.majors: Dict[str, Major] = dict() # key: name of major value: instance of class Major 
        self.students: Dict[str, Student] = dict() #_student[cwid]  = Student()
        self.instructors: Dict[str, Instructor] = dict() #instructor[csid] = Instructor()
        
        # read the students file and create instances of class student
        # read the instructors file and create instance of class instructor 
        # read the grades file and process each grade 
        self.read_majors(self.path)
        self.read_students(self.path)
        self.read_instructors(self.path)
        self.read_grades(self.path)
        #this cool trick I picked up from your review of HW10. i'm just printing a new line with the title of the pretty table
        # i think this makes it look a lot nicer and more readable
        print("\nMajor Summary")
        self.major_pretty_table()
        print("\nStudent Summary")
        self.student_pretty_table()
        print("\nInstructor Summary")
        self.instructor_pretty_table()
        # this is the new addition for HW11, I am using sqlite3 to grab the data that I querred on datagrip
        print("\nStudent Grade Summary")
        self.student_grades_table_db('/Users/Christopher/Desktop/HW11/startup.db')        

    def read_majors(self, path: str) -> None: 
        """ read each line from path/majors.txt and create an instance of class major for each line"""
       
        try: 

            for major, status, course in file_reader(os.path.join(self.path, "majors.txt"), 3,'\t', True):
                if major not in self.majors:
                    self.majors[major] = Major(major)
                    
                if status == "R": 
                    self.majors[major].add_Rcourse(course)
                    
                else:
                    self.majors[major].add_Ecourse(course)
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)       
        
    def read_students(self, path: str) -> None: 
        """ read each line from path/students.txt and create an instance of class student for each line"""
        try: 
            #cwid,name,major = file_reader(os.path.join(self.path, 'students.txt'), 3,'\t', False)
            for cwid, name, major in file_reader(os.path.join(self.path, "students.txt"), 3,'\t', True):
                              
                if major not in self.majors:
                    print("error")
                else: 
                    self.students[cwid] = Student(cwid, name, major, self.majors[major].required, self.majors[major].elective)
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)

    def read_instructors(self, path: str) -> None:  # write me 
        """ read each line from path/students.txt and create an instance of class student for each line"""
        try: 
            #incwid, name, dept = file_reader(os.path.join(self.path, 'instructors.txt'), 3,'\t', False)
            for incwid, name, dept in file_reader(os.path.join(self.path,"instructors.txt"), 3,'\t', True):
                self.instructors[incwid] = Instructor(incwid, name, dept)
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)
       
    def read_grades(self, path: str)-> None: 
        """ read each line from path/grades.txt and add to student and instructor and major classes based off results """
        #read students_cwid, course, grade, instructor_cwid
        # define the passing grades that we'll use to see if a student gets credit for the class
        
        try: 
            #student_cwid, course, grade, instructor_incwid = file_reader(os.path.join(self.path, 'grades.txt'), 4,'\t', False)
            for student_cwid, course, grade, instructor_incwid  in file_reader(os.path.join(self.path,"grades.txt"), 4,'\t', True):
                if student_cwid in self.students:
                    s: Student = self.students[student_cwid]
                    s.store_course_grade(course, grade)
                else:
                    print("Student not found") #need to include an error message if the student or instructor is not in the students/instructors file 
               
                # we need to take into account if a student takes a course but doesn't pass the course 
                # we will only take the course out of the remaining required if they pass
                     
                    
                # this code is unchanged, we are adding a count to the instructors total students count  
                if instructor_incwid in self.instructors:
                    inst: Instructor = self.instructors[instructor_incwid]
                    inst.store_course_student(course)
                else: 
                    print("Instructor not found") #need to include an error message if the student or instructor is not in the students/instructors file 
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)          

                
    def major_pretty_table(self) -> None: 
        """ gives us our for loop for rows of the major pretty table  """       
        pt = PrettyTable(field_names=Major.PT_MAJOR_FIELD_NAMES)
        for m in self.majors.values():
            pt.add_row(m.info())
            #add a row to the pretty table
        print(pt)     

    def student_pretty_table(self) -> None: 
        """ print a pretty table with student information"""
        pt = PrettyTable(field_names=Student.PT_STUDENT_FIELD_NAMES)
        for stu in self.students.values():
            pt.add_row(stu.info())
            #add a row to the pretty table
            
        print(pt)
        
    def instructor_pretty_table(self) -> None:     
        pt = PrettyTable(field_names=Instructor.PT_INSTRUCTOR_FIELD_NAMES)
        for inst in self.instructors.values():
            for line in inst.one_instructor(): # we only want to add one instructor row to the pretty table row at a time
                pt.add_row(line)  
            
        print(pt)   

    def student_grades_table_db(self, db_path):
        """ using a sqlite3 connection and a query tested first in data grip pull data for a new student grade summary 
            then print the prety table in this function too  """
        try: # see if we're connected 
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e) #tell us to try again
        else: 
            pt: PrettyTable = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])
            # here i took the whole query i typed out in data grip, i'm only calling this function once
            for tup in db.execute("""
                    select students.name, students.CWID, grades.course, grades.grade, instructors.Name
                    from students join grades on students.cwid = grades.StudentCWID
                    join instructors on instructors.CWID = grades.InstructorCWID
                    order by students.name"""):
                pt.add_row(tup)
            print(pt)    
 
def main ():     
    stevens: Repository = Repository("/Users/Christopher/Desktop/HW11")
    #columbia: Repository = Repository(add directory)
    #NYU: Repository = Repository(add directory)

    
if __name__ == '__main__':
    main()
    
 

