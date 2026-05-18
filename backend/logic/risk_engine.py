import json
from backend.models import db, Student, AcademicRecord, Course, RiskAnalysis, RiskRule

class RiskEvaluator:
    def __init__(self):
        self.load_rules()

    def load_rules(self):
        """Loads thresholds from the database or uses defaults."""
        rules = {r.rule_key: r.value for r in RiskRule.query.all()}
        self.gpa_high = rules.get('gpa_high_threshold', 2.0)
        self.gpa_med = rules.get('gpa_med_threshold', 2.5)
        self.core_fail_limit = int(rules.get('max_core_fails', 1))
        self.total_fail_limit = 3

    def calculate_gpa(self, student_records):
        """Calculates Semester GPA (SGPA) and Cumulative GPA (CGPA)."""
        grade_points = {'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'E': 1.0, 'F': 0.0}
        total_gp = 0
        total_units = 0
        
        for record in student_records:
            # Join with Course to get units
            course = Course.query.get(record.course_id)
            units = course.credit_units if course else 3
            gp = grade_points.get(record.grade, 0.0)
            
            total_gp += (gp * units)
            total_units += units
            
        return total_gp / total_units if total_units > 0 else 0.0

    def evaluate_risk(self, student_id):
        """Main AI Logic: Categorizes student risk and identifies factors."""
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return None

        records = AcademicRecord.query.filter_by(student_db_id=student.id).all()
        gpa = self.calculate_gpa(records)
        
        failures = [r for r in records if r.grade == 'F']
        core_failures = [r for r in failures if Course.query.get(r.course_id).is_core]
        
        factors = []
        category = "Low"
        
        # Rule 1: High Risk (GPA < 2.0 or multiple core failures)
        if gpa < self.gpa_high:
            category = "High"
            factors.append(f"Cumulative GPA ({gpa:.2f}) is below threshold 2.0")
        if len(core_failures) >= self.core_fail_limit:
            category = "High"
            factors.append(f"Student has failed {len(core_failures)} core course(s)")

        # Rule 2: Medium Risk (GPA < 2.5 or any recent failure)
        elif gpa < self.gpa_med or len(failures) > 0:
            category = "Medium"
            if gpa < self.gpa_med:
                factors.append(f"GPA ({gpa:.2f}) is marginal (below 2.5)")
            if len(failures) > 0:
                factors.append(f"Presence of failures ({len(failures)} course(s))")

        # Update or Create RiskAnalysis record
        analysis = RiskAnalysis.query.filter_by(student_db_id=student.id).first()
        if not analysis:
            analysis = RiskAnalysis(student_db_id=student.id)
            db.session.add(analysis)
        
        analysis.risk_score = gpa # Using GPA as score for now
        analysis.risk_category = category
        analysis.factors = json.dumps(factors)
        
        db.session.commit()
        return category, factors
