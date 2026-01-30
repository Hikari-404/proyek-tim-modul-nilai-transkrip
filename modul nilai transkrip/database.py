from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, event
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# Model Students
class Student(Base):
    __tablename__ = 'students'
    id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    grades = relationship('Grade', back_populates='student')

# Model Grades
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(20), ForeignKey('students.id'), nullable=False)
    course_id = Column(String(20), nullable=False)
    grade = Column(String(2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    # Tambahan field untuk audit
    changed_by = Column(String(100))
    change_reason = Column(Text)

    student = relationship('Student', back_populates='grades')
    history = relationship('GradeHistory', back_populates='grade')

# Model GradeHistory
class GradeHistory(Base):
    __tablename__ = 'grade_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    grade_id = Column(Integer, ForeignKey('grades.id'), nullable=False)
    old_value = Column(String(2))
    new_value = Column(String(2), nullable=False)
    changed_by = Column(String(100))
    changed_at = Column(DateTime, default=func.now())
    reason = Column(Text)

    grade = relationship('Grade', back_populates='history')

# Event listener untuk audit pada update Grade
@event.listens_for(Grade, 'before_update')
def audit_grade_update(mapper, connection, target):
    # Ambil session
    session = sessionmaker(bind=connection)()
    # Cari old grade
    old_grade = session.query(Grade).filter(Grade.id == target.id).first()
    if old_grade and old_grade.grade != target.grade:
        history = GradeHistory(
            grade_id=target.id,
            old_value=old_grade.grade,
            new_value=target.grade,
            changed_by=target.changed_by,
            reason=target.change_reason
        )
        session.add(history)
        session.commit()

# Engine SQLite
engine = create_engine('sqlite:///transkrip.db', echo=True)

# Buat tabel
Base.metadata.create_all(engine)

# Session
Session = sessionmaker(bind=engine)
session = Session()

# Contoh data
if not session.query(Student).first():
    # Tambah student
    student = Student(id='12345678', name='John Doe')
    session.add(student)

    # Tambah grade
    grade = Grade(student_id='12345678', course_id='TI101', grade='B', changed_by='admin', change_reason='Initial entry')
    session.add(grade)
    session.commit()

    # Update grade untuk test audit
    grade.grade = 'A'
    grade.changed_by = 'lecturer'
    grade.change_reason = 'Improved performance'
    session.commit()

# View-like query: Riwayat perubahan per mahasiswa
def get_student_grade_history(student_id):
    return session.query(
        Student.name,
        Grade.course_id,
        GradeHistory.old_value,
        GradeHistory.new_value,
        GradeHistory.changed_by,
        GradeHistory.changed_at,
        GradeHistory.reason
    ).join(Grade, Student.id == Grade.student_id)\
     .join(GradeHistory, Grade.id == GradeHistory.grade_id)\
     .filter(Student.id == student_id)\
     .order_by(GradeHistory.changed_at.desc())\
     .all()

# Test view
if __name__ == '__main__':
    history = get_student_grade_history('12345678')
    for h in history:
        print(h)