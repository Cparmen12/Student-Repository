# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:19:58 2020

@author: Christopher
"""
from typing import Dict, DefaultDict,Set, List
from collections import defaultdict
from HW08_Chris_Parmentier_Fixed import file_reader
import os
from prettytable import PrettyTable
 

class Major: 
    """ store everythying about a single major """
    PT_MAJOR_FIELD_NAMES = ['MAJOR', 'REQUIRED COURSES', 'ELECTIVE COURSES']
    
    def __init__(self, major: str)-> None:
        """ major stores an instance for each major on the major.txt file and pulls major, the required/elective, and the course number """ 
        self.major:str = major
        self.required: Set = set() # we want these to be sets because i wasn't storing differing values with a dict in the key and value. so the dict wasn't helping us.
        self.elective: Set = set()
       
        
    def add_Rcourse(self, course: str) -> None: 
        """add the course to the required course dictioanry """
        self.required.add(course)
        
    def add_Ecourse(self, course: str) -> None: 
        """add the course to the elective course dictioanry """
        self.elective.add(course)
        
    def get_required(self):
        """make a copy of the required courses for the major """
        return self.required.copy() 
     
    def get_elective(self):
        """make a copy of the elective courses for the major """
        return self.elective.copy() 
        
        
    def info(self):
         
        return[self.major, sorted(self.required), sorted(self.elective)]   

class Student: 
    """ store everythying about a single Student """
    PT_STUDENT_FIELD_NAMES = ['CWID', 'Name', 'Major', 'Completed Courses', 'GPA']
    
    def __init__(self, cwid: str, name: str, major: str)-> None:
        """ student stores an instance for each student on the student.txt file and pulls cwid, name, major """ 
        self.cwid:str = cwid
        self.name:str = name
        self.major:str = major
        self.courses: Dict[str, str] = dict() # courses[course_name] = grade
        self.grades: int= 0
        self.gpa: int = 0
        #finish me 
        
    def store_required(self, required: set):
        self.required = required
        
    def store_electives(self, elective: set):
        self.elective = elective 
        
    def store_course_grade(self, course: str, grade: str) -> None: 
        """Note that this student took course and earned grade """
        self.courses[course] = course
        grades_scale = {'A': 4.0, 'A-': 3.75,'B+': 3.25, 'B': 3.0,'B-': 2.75, 'C+': 2.25,'C': 2.0, 'C-': 0,'D+': 0, 'D': 0,'D-': 0, 'F': 0}
        for letter, points in  grades_scale.items():
            if grade in letter:
                grade_points = points
        # working on calculating the GPA here, but if the amount of courses taken is zero this gpa will default to zero

        self.grades += grade_points  
        if len(self.courses)!= 0:
            self.gpa = self.grades/len(self.courses)
        
    def info(self):
        """ return a list of information about me/self needed for pretty table"""
        return[self.cwid, self.name, self.major, sorted(self.courses), self.required, self.elective, self.gpa]
        
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
        self.majors: Dict[str, Major] = dict() 
        self.students: Dict[str, Student] = dict() #_student[cwid]  = Student()
        self.instructors: Dict[str, Instructor] = dict() #instructor[csid] = Instructor()

        
        # read the students file and create instances of class student
        # read the instructors file and create instance of class instructor 
        # read the grades file and process each grade 
        self.read_majors(self.path)
        self.read_students(self.path)
        self.read_instructors(self.path)
        self.read_grades(self.path)
        self.major_pretty_table()
        self.student_pretty_table()
        self.instructor_pretty_table()
        

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
            for cwid, name, major in file_reader(os.path.join(self.path, "students.txt"), 3,';', True):
                self.students[cwid] = Student(cwid, name, major)
                if major in self.majors: #You need to get the specific instance of class Major for each student.
                    #what i'm trying to do here is for each student use their major I got from the file_reader
                    # to then search for that major in the Majors class, to pull the required and electives for that major
                    self.req = Major[major].get_required()
                    self.store_required(self.req)
                    self.ele = Major[major].get_elective()
                    self.store_elective(self.ele)                 
        
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)

    def read_instructors(self, path: str) -> None:  # write me 
        """ read each line from path/students.txt and create an instance of class student for each line"""
        try: 
            #incwid, name, dept = file_reader(os.path.join(self.path, 'instructors.txt'), 3,'\t', False)
            for incwid, name, dept in file_reader(os.path.join(self.path,"instructors.txt"), 3,'|', True):
                self.instructors[incwid] = Instructor(incwid, name, dept)
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)
            

        
    
    def read_grades(self, path: str)-> None: 
        """ read each line from path/grades.txt and add to student and instructor and major classes based off results """
        #read students_cwid, course, grade, instructor_cwid
        # define the passing grades that we'll use to see if a student gets credit for the class
        passing = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'} 
        try: 
            #student_cwid, course, grade, instructor_incwid = file_reader(os.path.join(self.path, 'grades.txt'), 4,'\t', False)
            for student_cwid, course, grade, instructor_incwid  in file_reader(os.path.join(self.path,"grades.txt"), 4,'|', True):
                if student_cwid in self.students:
                    s: Student = self.students[student_cwid]
                    s.store_course_grade(course, grade)
                else:
                    print("Student not found") #need to include an error message if the student or instructor is not in the students/instructors file 
               
                # we need to take into account if a student takes a course but doesn't pass the course 
                # we will only take the course out of the remaining required if they pass
                if grade in passing:
                    if course in self.required:
                        self.required = self.required - course 
                        # each student only needs one elective
                        # if we see one elective then we can set the remaining elective courses to a blank container b/c there will be no electives remaining 
                    elif course in self.elective:
                        self.elective = []                       
                    
                # this code is unchanged, we are adding a count to the instructors total students count  
                if instructor_incwid in self.instructors:
                    inst: Instructor = self.instructors[instructor_incwid]
                    inst.store_course_student(course)
                else: 
                    print("Instructor not found") #need to include an error message if the student or instructor is not in the students/instructors file 
                
            
        except (FileNotFoundError, ValueError) as e: 
            print(e)          

                
    def major_pretty_table(self) -> None: 
       
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
        

            
            
        
      
def main (): 
    
    stevens: Repository = Repository("/Users/Christopher/Desktop/Stevens")
    #columbia: Repository = Repository(add directory)
    #NYU: Repository = Repository(add directory)

if __name__ == '__main__':
    main()
    

