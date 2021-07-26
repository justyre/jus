"""A gallery of notes and examples."""

########################
# IMPORT STYLE RULES
#
# use `from package import module_with_no_prefix`, or
# use `import package/module`.
# Use `import pkg/mod as alias` only when alias is a standard abbreviation.
# Never import everything.
# Imports should be on separate lines.
# Within each group (separated by blank lines), imports should be sorted lexico-
# graphically.
# Import groups should be ordered as: Python standard libraries; third-party packages; 
# other modules in the same working package.
# When importing the typing module: `from typing import Any, NoReturn`
#
# WHITESPACE RULES
# If operators with different priorities are used, consider adding whitespace around 
# the operators with the lowest priority(ies), eg. hypot2 = x*x + y*y, c = (a+b) * (a-b)
# Don't use spaces around the = sign when used to indicate a keyword argument, or when 
# used to indicate a default value for an unannotated function parameter.
# Correct:
# def complex(real, imag=0.0):
#     return magic(r=real, i=imag)
# When combining an argument annotation with a default value, however, do use spaces 
# around the = sign.
# Correct:
# def munge(sep: AnyStr = None): ...
# def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ... 
# 
# METHOD ORDER IN A CLASS
# From top to bottom: __init__, __special__, Properties, Public, Private.
#
# Use `pathlib` to operate file paths. 
# Use `dataclass` for a class containing mainly data.
# 
# The preferred way to manage files is using with: `with open("h.txt") as h_file:`
# For file-like objects that do not support the with statement, use contextlib.closing:
# import contextlib 
# with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page: 
#     for line in front_page: 
#         print(line)
#
# INHERITANCE
# When a derived class has __init__() function, explicitly call the base class’s 
# __init__(), because the he base class’s __init__() will not be called by the derived 
# class automatically.
# Correct:
#  class MyDerivedClass(BaseClass): 
#     def __init__(self): 
#         BaseClass.__init__(self)
#
# When calling a method from the base class, do:
# class Base: 
#     ... 
#     def greeting(self): 
#         ... 
# class Derived(Base): 
#     ... 
#     def echo(self): 
#         ... 
#         Base.greeting(self)
#
# When changing the type of the exception, always use 
# `raise <exception> from <original>`


def print_hi(name):
    """Print Hi."""
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


import math 

class Square(object):
    """A square with two properties: a writable area and a read-only perimeter.

    To use: 
     >>> sq = Square(3) 
    >>> sq.area 9 
    >>> sq.perimeter 12 
    >>> sq.area = 16 
    >>> sq.side 4 
    >>> sq.perimeter 16 
    """ 
    
    def __init__(self, side): 
        self.side = side 

    @property 
    def area(self): 
        """Get or set the area of the square.""" 
        return self._get_area() 

    # the following `@method.setter` decorator turns the setter method `area()` into 
    # a setter of the property `Square.area`.
    # Similarly, we also have `@method.deleter`.
    @area.setter 
    def area(self, area_of_square): 
        return self._set_area(area_of_square) 

    def _get_area(self): 
        #Indirect accessor to calculate the `area` property. 
        return self.side ** 2 

    def _set_area(self, area): 
        #Indirect setter to set the `area` property.
        self.side = math.sqrt(area) 

    # the following `@property` decorator turns the getter method `perimeter()` into 
    # a getter of the now-read-only property `Square.perimeter`.
    # note: If for a method, we only define a getter method (by prefixing @property), 
    # but do not define a setter method, then this method is turned read-only.
    @property 
    def perimeter(self):
        """Perimeter of the sqaure.""" 
        return self.side * 4
    
    @perimeter.deleter
    def perimeter(self):
        self.side = 0


class Student(object):
    """A class for student score info."""

    def get_score(self):
        """Get score."""
        return self._score

    def set_score(self, value):
        """Set score."""
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

if __name__ == '__main__':
    print_hi('PyCharm')
    print('Hello world!')
    print('Hello Again')
    print('I like typing this.')
    print('This is fun.')
    print('Yay! Printing.')
    # in this case, using double quotes outside is clearer
    print("I'd much rather you 'not'.")
    # either double covers single or the other way round
    print('I "said" do not touch this. Hi # there!')
    name = "World"
    print(f"Hello, {name}!")
    
    # instantiate
    sq = Square(3)
    # sq.area invokes sq._get_area()
    print(sq.area, sq.perimeter)
    sq.area = 16
    print(sq.side, sq.perimeter)
    # if we try to run the next commented line, will throw an AttributeError, 
    # saying `can't set attribute`, coz @property made Square.perimeter read only:
    # sq.perimeter = 90
    del sq.perimeter
    print(sq.side, sq.perimeter)
    
    s = Student()
    s.set_score(60)
    print(s._score, s.get_score())
    
    
    # Initializing list 1 (list is a mutable obj)
    li1 = [1, 2, [3,5], 4] 

    # Shallow copy (actually, this should be called assignment)
    li2 = li1

    # original elements of list 
    print ("The original elements before shallow copying") 
    for i in range(0,len(li1)): 
        print (li1[i],end=" ") 

    # changing an element to new list 
    li2[2][0] = 7 

    # checking if change is reflected (yes, li1 is also changed!)
    print ("\nThe original elements after shallow copying") 
    for i in range(0,len( li1)): 
        print (li1[i],end=" ")
        
    
    # Deep copy, so that we can change the copy without altering the original object
    import copy
    li3 =  copy.deepcopy(li1)
    
    # changing an element to new list 
    li3[2][0] = 8 

    # checking if change is reflected (yes, li1 is also changed!)
    print ("\nThe original elements after deep copying") 
    for i in range(0,len( li1)): 
        print (li1[i],end=" ")
    print ("\nThe new list of elements after deep copying") 
    for i in range(0,len( li3)): 
        print (li3[i],end=" ")
    print()
        
    
    # example of a decorator
    
    from functools import wraps
    
    def a_new_decorator(a_func):
        """Docstring of a_new_decorator."""
        # next `@wraps...` tells Python that the wrapper function should be seen as 
        # a_func
        @wraps(a_func)
        def wrapTheFunction():
            """Docstring of wrapTheFunction."""
            print("I am doing some boring work before executing a_func()")

            a_func()

            print("I am doing some boring work after executing a_func()")
 
        return wrapTheFunction
    
    # the `@a_new_decorator` below is just a short way of saying:
    # a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
    # , so that now a_function_requiring_decoration is wrapped by wrapTheFunction()
    @a_new_decorator
    def a_function_requiring_decoration():
        """Docstring of a_function_requiring_decoration."""
        print("I am the function which needs some decoration to remove my foul smell")
 
    a_function_requiring_decoration()
    # the output of next line will be a_function_requiring_decoration
    # note: w/out the `@wraps...` line, the output would be wrapTheFunction
    print(a_function_requiring_decoration.__name__)
    print(a_function_requiring_decoration.__doc__)
  
    # shows help of a class
    print(help(Square))


####################################
# RETRIEVE DATA FROM BOCIM DATASETS

import cx_Oracle
import pandas as pd
import pyodbc

# # Connect to TianXiang Database (MS SQL)

# # in SSMS, use txnfdb.stock.T_INDEX_WEIGHT
# sql_text = '''select top 5 * from stock.T_INDEX_WEIGHT '''
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=18.1.2.161;DATABASE=txnfdb;UID=invest;PWD=quant-2004()')
# with conn:
#     dftx = pd.read_sql(sql_text, conn)
# # the next line displays the dataframe better
# with pd.option_context("display.max_rows", 10, "display.max_columns", 30):
#     print(dftx)
    


# Connect to Wind Database (Oracle)
# IMPORTANT NOTE: 
# Generally, I suggest the cx_Oracle method for it is simpler to set up, and supports 
# Chinese out of box.
# 1. Prerequisite for the cx_Oracle method to work: Install Oracle Instant Client 
# Basic (cf. https://www.oracle.com/database/technologies/instant-client/downloads.html)
# and extract it to say D:\Prg\instantclient_19_11. Then add this to current user's 
# environmental variable PATH. Restart VSCode.
#
# 2. Prerequisite for the pyodbc method to work: We also need to install the above 
# Oracle Instant Client Basic package, and in addition, we need to install Oracle 
# Instant Client ODBC package too (from the same link). Execute `odbc_install.exe` AS 
# ADMIN (Very important! Or it won't work!) from say D:\Prg\instantclient_19_11.
# Then Win+S, type ODBC, find ODBC Data Sources (64-bit), turn to tab `Drivers`, copy 
# the name `Oracle in instantclient_19_11` to the Driver= part of pyodbc.connect().
# This driver name can also be checked by print(pyodbc.drivers()).
# cf. https://www.oracle.com/database/technologies/releasenote-odbc-ic.html


sql_text = '''
select * from ASHAREEODPRICES WHERE trade_dt=20200122 and S_DQ_TRADESTATUS='停牌' and ROWNUM < 3 order by S_INFO_WINDCODE
'''
conn = cx_Oracle.connect('wind/wind_bocim04@18.1.2.158:1521/zjzxdb')
# Alternatively, can use the line below to replace pyodbc, but the Chinese support may 
# be problematic
# conn = pyodbc.connect('Driver={Oracle in instantclient_19_11};DBQ=18.1.2.158:1521/zjzxdb;Uid=wind;Pwd=wind_bocim04')
with conn:
    dfwd = pd.read_sql(sql_text, conn)
with pd.option_context("display.max_rows", 10, "display.max_columns", 30):
    print(dfwd)