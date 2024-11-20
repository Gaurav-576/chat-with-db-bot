import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
CREATE TABLE students(
    roll INTEGER PRIMARY KEY,
    name VARCHAR(25),
    branch VARCHAR(10),
    semester INTEGER,
    CGPA REAL
)
"""

try:
    cursor.execute(table_info)
except sqlite3.OperationalError:
    pass

try:
    cursor.execute('''INSERT INTO students VALUES(1,"Rahul","CSE",3,8.5)''')
    cursor.execute('''INSERT INTO students VALUES(2,"Rohit","ECE",3,8.0)''')
    cursor.execute('''INSERT INTO students VALUES(3,"Raj","ME",3,7.5)''')
    cursor.execute('''INSERT INTO students VALUES(4,"Ravi","CSE",3,9.0)''')
    cursor.execute('''INSERT INTO students VALUES(5,"Rajat","CSE",3,8.5)''')
except sqlite3.IntegrityError:
    pass

data=cursor.execute('''SELECT * FROM students''')

print(data)
    
connection.commit()
connection.close()
