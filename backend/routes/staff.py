from flask import Blueprint, render_template, abort, send_file, request, redirect, url_for, flash
from flask_login import login_required, current_user
import json
from collections import defaultdict
from backend.models import Student, RiskAnalysis, AcademicRecord, Course, db
from backend.logic.reporting import generate_student_report
from backend.logic.audit import log_action

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()
    student_data = []
    high_alerts = []
    high_count = med_count = low_count = 0

    for s in students:
        analysis = RiskAnalysis.query.filter_by(student_db_id=s.id).first()
        category = analysis.risk_category if analysis else 'Low'
        score = round(analysis.risk_score, 2) if analysis else 'N/A'

        student_data.append({
            'name': s.name,
            'student_id': s.student_id,
            'level': s.level or 'N/A',
            'category': category,
            'score': score
        })

        if category == 'High':
            high_count += 1
            high_alerts.append({'name': s.name, 'student_id': s.student_id})
        elif category == 'Medium':
            med_count += 1
        else:
            low_count += 1

    return render_template('staff/dashboard.html',
                           students=student_data,
                           high_alerts=high_alerts,
                           high_count=high_count,
                           med_count=med_count,
                           low_count=low_count)

@staff_bp.route('/student/<path:student_id>')
@login_required
def student_detail(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        abort(404)

    analysis = RiskAnalysis.query.filter_by(student_db_id=student.id).first()
    records = AcademicRecord.query.filter_by(student_db_id=student.id).order_by(
        AcademicRecord.session, AcademicRecord.semester).all()

    detailed_records = []
    # Build per-semester GPA averages for chart
    semester_scores = defaultdict(list)
    for r in records:
        course = Course.query.get(r.course_id)
        label = f"Sem {r.semester} {r.session}"
        if r.score:
            semester_scores[label].append(float(r.score))
        detailed_records.append({
            'code': course.course_code if course else 'N/A',
            'title': course.title if course else 'N/A',
            'grade': r.grade,
            'score': r.score,
            'semester': r.semester,
            'session': r.session
        })

    chart_labels = list(semester_scores.keys())
    chart_data = [round(sum(v)/len(v), 2) for v in semester_scores.values()]

    factors = json.loads(analysis.factors) if analysis and analysis.factors else []

    return render_template('staff/student_profile.html',
                           student=student,
                           analysis=analysis,
                           records=detailed_records,
                           factors=factors,
                           chart_labels=json.dumps(chart_labels),
                           chart_data=json.dumps(chart_data))

@staff_bp.route('/student/<path:student_id>/save-notes', methods=['POST'])
@login_required
def save_notes(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        abort(404)
    notes = request.form.get('advisor_notes', '')
    student.notes = notes
    db.session.commit()
    log_action('Advisor Note', f'Updated notes for student {student_id}')
    flash('Notes saved successfully.', 'success')
    return redirect(url_for('staff.student_detail', student_id=student_id))

@staff_bp.route('/at-risk')
@login_required
def at_risk_alerts():
    high_risk_analyses = RiskAnalysis.query.filter_by(risk_category='High').all()
    med_risk_analyses = RiskAnalysis.query.filter_by(risk_category='Medium').all()

    def enrich(analyses):
        result = []
        for a in analyses:
            s = Student.query.get(a.student_db_id)
            if s:
                result.append({
                    'name': s.name,
                    'student_id': s.student_id,
                    'level': s.level or 'N/A',
                    'category': a.risk_category,
                    'score': round(a.risk_score, 2)
                })
        return result

    high_students = enrich(high_risk_analyses)
    med_students = enrich(med_risk_analyses)

    return render_template('staff/at_risk.html',
                           high_students=high_students,
                           med_students=med_students)

@staff_bp.route('/download/report/<path:student_id>')
@login_required
def download_student_report(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        abort(404)

    analysis = RiskAnalysis.query.filter_by(student_db_id=student.id).first()
    records = AcademicRecord.query.filter_by(student_db_id=student.id).all()

    processed_records = []
    for r in records:
        course = Course.query.get(r.course_id)
        processed_records.append({
            'session': r.session,
            'semester': r.semester,
            'code': course.course_code if course else 'N/A',
            'grade': r.grade,
            'score': r.score
        })

    factors = json.loads(analysis.factors) if analysis and analysis.factors else []
    pdf_buffer = generate_student_report(student, analysis, processed_records, factors)
    log_action('PDF Download', f'Downloaded individual report for student {student.student_id}')

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Report_{student.student_id}.pdf",
        mimetype='application/pdf'
    )
