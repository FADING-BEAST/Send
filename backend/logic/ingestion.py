import csv
import io
import pandas as pd
from backend.models import db, Student, Course, AcademicRecord

class CSVProcessor:
    def __init__(self, file_stream):
        # Convert stream to dataframe
        self.df = pd.read_csv(io.StringIO(file_stream.read().decode('utf-8')))
        self.required_columns = ['StudentID', 'Name', 'CourseCode', 'CourseTitle', 'Grade', 'Score', 'Semester', 'Session']

    def validate_format(self):
        """Checks if all required columns are present."""
        missing = [col for col in self.required_columns if col not in self.df.columns]
        if missing:
            return False, f"Missing columns: {', '.join(missing)}"
        return True, "Check successful"

    def get_all_rows(self):
        """Returns all rows for the preview table."""
        return self.df.to_dict(orient='records')

    def process_import(self):
        """Saves CSV data to the database."""
        count = 0
        duplicates = 0
        for _, row in self.df.iterrows():
            # 1. Handle Student
            student = Student.query.filter_by(student_id=row['StudentID']).first()
            if not student:
                student = Student(student_id=row['StudentID'], name=row['Name'])
                db.session.add(student)
                db.session.flush()

            # 2. Handle Course
            course = Course.query.filter_by(course_code=row['CourseCode']).first()
            if not course:
                course = Course(course_code=row['CourseCode'], title=row['CourseTitle'])
                db.session.add(course)
                db.session.flush()

            # 3. Duplicate Detection & Record Insertion
            existing_record = AcademicRecord.query.filter_by(
                student_db_id=student.id, 
                course_id=course.id,
                semester=row['Semester'],
                session=row['Session']
            ).first()

            if not existing_record:
                record = AcademicRecord(
                    student_db_id=student.id,
                    course_id=course.id,
                    grade=row['Grade'],
                    score=float(row['Score']),
                    semester=row['Semester'],
                    session=row['Session']
                )
                db.session.add(record)
                count += 1
            else:
                duplicates += 1
        
        db.session.commit()
        return count, duplicates
