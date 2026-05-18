import os
import csv
from enum import Enum

# Standard absolute imports for standalone testing
try:
    from ingestion import DataIngestor
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ingestion import DataIngestor

class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class RiskEngine:
    def __init__(self, gpa_threshold=2.0, core_failure_threshold=1):
        self.gpa_threshold = gpa_threshold
        self.core_failure_threshold = core_failure_threshold
        self.core_courses = ['CSC101', 'CSC102', 'CSC201', 'CSC202', 'MAT101', 'MAT102']

    def calculate_gpa(self, records):
        """Calculates temporary GPA based on grades (A=5, B=4, C=3, D=2, E=1, F=0)."""
        grade_points = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        total_points = 0
        valid_records = 0
        for record in records:
            grade = record.get('Grade')
            if grade in grade_points:
                total_points += grade_points[grade]
                valid_records += 1
        return total_points / valid_records if valid_records > 0 else 0.0

    def analyze_student(self, student_records):
        """Analyzes a student's records and assigns a risk level."""
        gpa = self.calculate_gpa(student_records)
        failures = [r for r in student_records if r['Grade'] == 'F']
        core_failures = [r for r in failures if r['CourseCode'] in self.core_courses]
        
        # Risk Logic (simplified version from implementation plan)
        if gpa < self.gpa_threshold or len(core_failures) >= self.core_failure_threshold:
            return RiskLevel.HIGH, gpa, core_failures
        elif gpa < 2.5 or len(failures) > 0:
            return RiskLevel.MEDIUM, gpa, core_failures
        else:
            return RiskLevel.LOW, gpa, core_failures

if __name__ == "__main__":
    # Integration test
    ingestor = DataIngestor()
    # Assuming we are running from project root
    csv_path = 'data/samples/student_records.csv'
    if not os.path.exists(csv_path):
        # Try relative to script
        csv_path = os.path.join(os.path.dirname(__file__), '../../data/samples/student_records.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        exit(1)

    students_data = ingestor.parse_csv(csv_path)
    engine = RiskEngine()
    
    print("\n" + "="*50)
    print("      ACADEMIC RISK ANALYSIS REPORT (POC)")
    print("="*50)
    for sid, data in students_data.items():
        level, gpa, core_fails = engine.analyze_student(data['records'])
        print(f"Student: {data['name']:<15} | ID: {sid:<6}")
        print(f"  GPA: {gpa:.2f} | Risk Level: {level.value}")
        if core_fails:
            print(f"  Alerts: Core Failures in {[f['CourseCode'] for f in core_fails]}")
        print("-" * 50)
