import csv
import json
from pathlib import Path

class DataIngestor:
    def __init__(self, db_path=None):
        self.records = []
        self.students = {}

    def parse_csv(self, file_path):
        """Parses a CSV file of student records."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append(row)
                student_id = row['StudentID']
                if student_id not in self.students:
                    self.students[student_id] = {
                        'name': row['Name'],
                        'records': []
                    }
                self.students[student_id]['records'].append(row)
        
        return self.students

    def get_student_summary(self, student_id):
        """Returns a summary of a student's performance."""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        total_courses = len(student['records'])
        failures = [r for r in student['records'] if r['Grade'] == 'F']
        
        return {
            'student_id': student_id,
            'name': student['name'],
            'total_courses': total_courses,
            'failures_count': len(failures),
            'latest_semester': student['records'][-1]['Semester'] if student['records'] else None
        }

if __name__ == "__main__":
    # Quick test
    ingestor = DataIngestor()
    try:
        data = ingestor.parse_csv('data/samples/student_records.csv')
        print(f"Parsed {len(data)} students.")
        for sid in data:
            print(ingestor.get_student_summary(sid))
    except Exception as e:
        print(f"Error: {e}")
