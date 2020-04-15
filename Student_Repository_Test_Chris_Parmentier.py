#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 1 2020 

@author: Chris Parmentier 
The purpose of this file is to call the unittest and test HW11 :)

"""

import unittest
from typing import Tuple
from datetime import datetime, timedelta 

#from typing import List
from Student_Repository_Chris_Parmentier import Repository, student_grades_table_db


      
class Repository_Test(unittest.TestCase):
    "goal of this class is to test date_arithmetic"
    def test_Repository(self) -> None:
        "Test entire repository by ensuring students file is accurate"
            
        expected_students: List = [
        ('10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38)
        ('10115', 'Bezos, J', 'SFEN', ['CS 546', 'SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 2.0)
        ('10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0)
        ('11714', 'Gates, B', 'CS', ['CS 546', 'CS 570' 'SSW 810'], [], [], 3.5)
        ]
    self.stevens: Repository = Repository("/Users/Christopher/Desktop/HW11")
    self.assertEqual(stevens.students(), expected_students)   

    def test_student_grades_table_db(self) -> None:
        "Test entire repository by ensuring students file is accurate"
            
        expected_table_db: List = [
        ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J')
        ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S')
        ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J')
        ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R')
        ('Gates, B', '11714', 'cs 570', 'A-', 'Hawking, S')
        ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J')
        ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S')
        ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J')
        ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')

        ]
    self.assertEqual(student_grades_table_db('/Users/Christopher/Desktop/HW11/startup.db'), table_db)      

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)                         
