# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:19:58 2020

@author: Christopher
"""
from typing import Dict, DefaultDict
from collections import defaultdict
from HW08_Chris_Parmentier_Fixed import file_reader
import os
from prettytable import PrettyTable
 
class Student: 
    """ store everythying about a single Student """
    PT_STUDENT_FIELD_NAMES = ['CWID', 'Name', 'Major', 'Courses']
    
    def __init__(self, cwid: str, name: str, major: str)-> None:
        """ student stores an instance for each student on the student.txt file and pulls cwid, name, major """ 
        self.cwid:str = cwid
        self.name:str = name
        self.major:str = major
        self.courses: Dict[str, str] = dict() # courses[course_name] = grade
        #finish me 
        
    def store_course_grade(self, course: str, grade: str) -> None: 
        """Note that this student took course and earned grade """
        self.courses[course] = course
        
        
    def info(self):
        """ return a list of information about me/self needed for pretty table"""
        return[self.cwid, self.name, self.major, sorted(self.courses)]
        
class Instructor: 
    """ store everythying about a single instructor """
    PT_INSTRUCTOR_FIELD_NAMES = ['CWID', 'Name', 'Major', 'Courses', 'Students']
    
    def __init__(self, incwid: str, name: str, dept: str)-> None:
        """add constructor""" 
        self.incwid:str = incwid
        self.name:str = name
        self.dept:str = dept
        self.courses: DefaultDict[str, int] = defaultdict(int)  # courses[course_name] = # of students who have taken that class 
        
    def store_course_student(self, course: str)-> None:
        """ note that instructor taught one more student in course"""
        self.courses[course] +=1
        
    def info(self): # really only used this for the unit test case 
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
        self.students: Dict[str, Student] = dict() #_student[cwid]  = Student()
        self.instructors: Dict[str, Instructor] = dict() #instructor[csid] = Instructor()
        
        
        # read the students file and create instances of class student
        # read the instructors file and create instance of class instructor 
        # read the grades file and process each grade 
        self.read_students(self.path)
        self.read_instructors(self.path)
        self.read_grades(self.path)
        self.student_pretty_table()
        self.instructor_pretty_table()
        

        
    def read_students(self, path: str) -> None: 
        """ read each line from path/students.txt and create an instance of class student for each line"""
        try: 
            #cwid,name,major = file_reader(os.path.join(self.path, 'students.txt'), 3,'\t', False)
            for cwid, name, major in file_reader(os.path.join(self.path, "students.txt"), 3,'\t', False):
                self.students[cwid] = Student(cwid, name, major)
        
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)

    def read_instructors(self, path: str) -> None:  # write me 
        """ read each line from path/students.txt and create an instance of class student for each line"""
        try: 
            #incwid, name, dept = file_reader(os.path.join(self.path, 'instructors.txt'), 3,'\t', False)
            for incwid, name, dept in file_reader(os.path.join(self.path,"instructors.txt"), 3,'\t', False):
                self.instructors[incwid] = Instructor(incwid, name, dept)
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)
        
    
    def read_grades(self, path: str)-> None: 
        #read students_cwid, course, grade, instructor_cwid
        # print errors 
        try: 
            #student_cwid, course, grade, instructor_incwid = file_reader(os.path.join(self.path, 'grades.txt'), 4,'\t', False)
            for student_cwid, course, grade, instructor_incwid  in file_reader(os.path.join(self.path,"grades.txt"), 4,'\t', False):
                if student_cwid in self.students:
                    s: Student = self.students[student_cwid]
                    s.store_course_grade(course, grade)
                else:
                    print("Student not found") #need to include an error message if the student or instructor is not in the students/instructors file 
                    
                if instructor_incwid in self.instructors:
                    inst: Instructor = self.instructors[instructor_incwid]
                    inst.store_course_student(course)
                else: 
                    print("Instructor not found") #need to include an error message if the student or instructor is not in the students/instructors file 
                
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)          

        # tell instructor she taught one more student in course
        
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
        
      
def main (): 
    
    stevens: Repository = Repository("/Users/Christopher/Desktop/Stevens")
    #columbia: Repository = Repository(add directory)
    #NYU: Repository = Repository(add directory)

if __name__ == '__main__':
    main()
    

