#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on April 1 2020 

@author: Chris Parmentier 
The purpose of this file is to call the unittest and test HW09 :)

"""

import unittest
from typing import Tuple
from datetime import datetime, timedelta 

#from typing import List
from HW09_Chris_Parmentier import Repository, Instructor, Student

class date_arithmetic_test(unittest.TestCase):
    "goal of this class is to test date_arithmetic"
    def test_date_arithmetic(self) -> None:
        "date_arithmetic"
        expected: Tuple = (datetime(2020, 3, 1, 0, 0),
                           datetime(2019, 3, 2, 0, 0),
                           timedelta(days=241))
        ctest = date_arithmetic()
        self.assertEqual(ctest, expected)
      
class file_reader_test(unittest.TestCase):
    "goal of this class is to test date_arithmetic"
    def test_file_reader(self) -> None:
        "file_reader"
        self.assertEqual(file_reader("student_majors.txt", 3, sep='|', header=True), ['123', 'Jin He', 'Computer Science'])       

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)                         
