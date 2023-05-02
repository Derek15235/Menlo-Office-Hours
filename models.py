"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.

"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# Content Standards: all the table names match with each 
# entity on the most recent ER diagram
class Student(Base):
    __tablename__ = "students"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    first_name = Column("first_name", TEXT, nullable=False)
    last_name = Column("last_name", TEXT, nullable=False)
    email = Column("email", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)

    meetings = relationship("Meeting", back_populates="student")

    # Constructor
    def __init__ (self, first_name, last_name, email, password):
        # id autoincrements
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return self.first_name + " " + self.last_name
    
class Teacher(Base):
    __tablename__ = "teachers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    first_name = Column("first_name", TEXT, nullable=False)
    last_name = Column("last_name", TEXT, nullable=False)
    email = Column("email", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    img_link = Column("img_link", TEXT, nullable=False)
    department = Column("department", TEXT, nullable=False)

    meetings = relationship("Meeting", back_populates="teacher")

    # Constructor
    def __init__ (self, first_name, last_name, email, password, img_link, department):
        # id autoincrements
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.img_link = img_link
        self.department = department

    def __repr__(self):
        return self.first_name + " " + self.last_name

class Meeting(Base):
    __tablename__ = "meetings"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    date = Column("date", TEXT, nullable=False) 
    time = Column("time", TEXT, nullable=False)
    description = Column("description", TEXT)
    teacher_id = Column("teacher_id", ForeignKey("teachers.id"), nullable=False)
    student_id = Column("student_id", ForeignKey("students.id"))

    student = relationship("Student", back_populates="meetings")
    teacher = relationship("Teacher", back_populates="meetings")

    # Constructor
    def __init__(self, date, time, teacher_id, student_id=None, description=""):
        self.date = date
        self.time = time
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.description = description

