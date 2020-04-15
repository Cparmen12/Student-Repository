# -*- coding: utf-8 -*-
"""
Created on 3/23/2020

@author: Chris 
The homework has multiple purposes. use some date functions, read a file, and ....

"""
from typing import List, Tuple, IO, Iterator, Dict
from collections import defaultdict
from datetime import datetime, timedelta 
import os

from prettytable import PrettyTable



"""
def date_arithmetic() -> Tuple[datetime, datetime, int]:
    # demonstrate some date arithemtic
     
    date1: str = "27 FEB 2020"
    date2: str = "27 FEB 2019"
    date3: str = "1 FEB 2019"
    date4: str = "30 SEP 2019"
    num_days: int = 3
    dt1: datetime = datetime.strptime(date1, "%d %b %Y")
    dt2: datetime = datetime.strptime(date2, "%d %b %Y")
    dt3: datetime = datetime.strptime(date3, "%d %b %Y")
    dt4: datetime = datetime.strptime(date4, "%d %b %Y")
    three_days_after_02272020: datetime = dt1 + timedelta(days=num_days)
    three_days_after_02272019: datetime = dt2 + timedelta(days=num_days)
    days_passed_01012019_10312019: int = dt4 - dt3

    return three_days_after_02272020, three_days_after_02272019, days_passed_01012019_10312019

"""
def file_reader(path: str, num_fields: int, sep: str= ',', header: bool = False) -> Iterator[Tuple[str, ...]]:
     """insert doc string"""
    
     try: 
        fp: IO = open(path, "r")
     except FileNotFoundError:
        raise FileNotFoundError(f"Can't open '{path}' for reading")
     else:
        with fp: 
            for n, line in enumerate(fp,1):
                fields: List[str] = line.rstrip('\n').split(sep)
                if len(fields) != num_fields:
                    raise ValueError(f"'{path}' line: {n}: read {len(fields)} fields but expected {num_fields}")
                elif n ==1 and header: 
                    continue 
                else:
                    yield tuple(fields)

#file_reader("student_majors.txt", 3, '|', True)


"""              
class FileAnalyzer: 
    # comment
    # comment 
    def __init__(self,directory: str) -> None: 
        self.directory: str = directory 
        self.files_summary: Dict[str, Dict[str, int]]  = dict() # this will be populated by self.analyze files
        self.analyze_files() # summerize the python files data

    def analyze_files(self) -> None:
       #This will look through the directory at the files and determine which are python files, then call the file stat function 
       result: Dict[str, int] = dict()
       try: 
           files: List[str] = os.listdir(self.directory)
       except FileNotFoundError: 
           raise FileNotFoundError(f"Direcoty {self.direcory} was not found")
       else: 
           for f in files: 
               if f.lower().endswith('.py'):
                   path: str = os.path.join(self.directory, f)
                   try: 
                       self.files_summary[path] = self.process_files(path) # get the counts from the files and populate self
                   except FileNotFoundError as fnfe:
                       raise fnfe
                       
    def process_files(self, path: str) -> Dict[str, int]:
        
       try: 
            fp: IO = open(path, 'r')
       except FileNotFoundError: 
            raise FileNotFoundError(f"Unable to open '{path}'")
       else: 
            with fp: 
                counts: defaultdict[str, int] = defaultdict(int)
                for line in fp: 
                    counts['char'] += len(line) # calculate total chars before stripping 
                    counts['line'] += 1 # found one more line 
                    line = line.strip() # strip newline and any leading or trailing whitespace 
                    if line.startswith('class '):
                        counts['class'] +=1
                    elif line.startswith('def '):
                        counts['function']+=1
                        
                return counts
    def pretty_print(self) -> PrettyTable: 
        pt: PrettyTable = PrettyTable(field_names= ['File Name', 'Classes', 'Functions', 'Lines', 'Characters'])
        for file in self.files_summary: 
            counts: Dict[str, int] = self.files_summary[file]
            pt.add_row([file, counts['class'], counts['function'], counts['line'], counts['char'],])
            
        return pt

           
#directory = os.getcwd()
#fa: FileAnalyzer = FileAnalyzer(directory)
"""