from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from flask_login import login_required, current_user
import os
import tempfile
from werkzeug.security import generate_password_hash
from backend.logic.ingestion import CSVProcessor
from backend.logic.risk_engine import RiskEvaluator
from backend.logic.audit import log_action
from backend.models import db, Student, RiskAnalysis, User, AuditLog, Course, ImportLog, RiskRule

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Admin':
        abort(403)
    
    total_students = Student.query.count()
    high_risk = RiskAnalysis.query.filter_by(risk_category='High').count()
    med_risk = RiskAnalysis.query.filter_by(risk_category='Medium').count()
    low_risk = RiskAnalysis.query.filter_by(risk_category='Low').count()
    
    # Calculate percentages
    if total_students > 0:
        high_pct = (high_risk / total_students) * 100
        med_pct = (med_risk / total_students) * 100
        low_pct = (low_risk / total_students) * 100
    else:
        high_pct = med_pct = low_pct = 0

    return render_template('admin/dashboard.html', 
                         total=total_students, 
                         high=high_risk, med=med_risk, low=low_risk,
                         high_pct=round(high_pct, 1), 
                         med_pct=round(med_pct, 1), 
                         low_pct=round(low_pct, 1),
                         recent_imports=ImportLog.query.order_by(ImportLog.timestamp.desc()).limit(5).all())

@admin_bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_data():
    if current_user.role != 'Admin':
        abort(403)
    
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['csv_file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        try:
            # Save to temp file
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"import_{current_user.id}.csv")
            file.save(temp_path)
            
            # Initial validation
            with open(temp_path, 'rb') as f:
                processor = CSVProcessor(f)
                valid, msg = processor.validate_format()
                if not valid:
                    flash(msg, 'danger')
                    return redirect(request.url)
            
            session['temp_import_path'] = temp_path
            return redirect(url_for('admin.import_preview'))
            
        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'danger')
            
    return render_template('admin/import.html')

@admin_bp.route('/import/preview')
@login_required
def import_preview():
    if current_user.role != 'Admin':
        abort(403)
    
    path = session.get('temp_import_path')
    if not path or not os.path.exists(path):
        flash('No import in progress', 'warning')
        return redirect(url_for('admin.import_data'))
    
    with open(path, 'rb') as f:
        processor = CSVProcessor(f)
        rows = processor.get_all_rows()
    
    return render_template('admin/import_preview.html', rows=rows)

@admin_bp.route('/import/confirm', methods=['POST'])
@login_required
def import_confirm():
    if current_user.role != 'Admin':
        abort(403)
    
    path = session.get('temp_import_path')
    if not path or not os.path.exists(path):
        flash('Import session expired', 'danger')
        return redirect(url_for('admin.import_data'))
    
    try:
        with open(path, 'rb') as f:
            processor = CSVProcessor(f)
            count, duplicates = processor.process_import()
        
        # Cleanup
        os.remove(path)
        session.pop('temp_import_path', None)
        
        # Recalculate risk (Asmau's Logic)
        evaluator = RiskEvaluator()
        all_students = Student.query.all()
        for student in all_students:
            evaluator.evaluate_risk(student.student_id)
            
        flash(f'Import Complete. Added {count} records. Skipped {duplicates} duplicates.', 'success')
        log_action('CSV Import', f'Imported {count} records, skipped {duplicates} duplicates.')

        # Save import history
        import_log = ImportLog(
            uploaded_by=current_user.id,
            records_added=count,
            duplicates_skipped=duplicates,
            status='Success'
        )
        db.session.add(import_log)
        db.session.commit()

        # Broadcast import notification
        from backend.routes.notifications import push_notification_all, push_notification
        push_notification_all(
            title='New Data Import',
            body=f'{count} student records imported by {current_user.email}. Risk levels have been recalculated.',
            category='info'
        )
        # Push danger alerts for newly high-risk students
        from backend.models import RiskAnalysis
        high_students = RiskAnalysis.query.filter_by(risk_category='High').all()
        for analysis in high_students[:10]:  # cap at 10 to avoid flood
            s = Student.query.get(analysis.student_db_id)
            if s:
                for user in User.query.all():
                    push_notification(
                        user_id=user.id,
                        title=f'High-Risk Alert: {s.name}',
                        body=f'{s.student_id} ({s.name}) is flagged as HIGH RISK with a score of {analysis.risk_score:.2f}.',
                        category='danger'
                    )

        return redirect(url_for('admin.dashboard'))

    except Exception as e:
        import_log = ImportLog(
            uploaded_by=current_user.id,
            records_added=0,
            status='Failed'
        )
        db.session.add(import_log)
        db.session.commit()
        flash(f'Error finalizing import: {str(e)}', 'danger')
        return redirect(url_for('admin.import_data'))

    return render_template('admin/import.html')

@admin_bp.route('/import/history')
@login_required
def import_history():
    if current_user.role != 'Admin':
        abort(403)
    logs = ImportLog.query.order_by(ImportLog.timestamp.desc()).all()
    return render_template('admin/import_history.html', logs=logs)

@admin_bp.route('/download/cohort-report')
@login_required
def download_cohort_report():
    if current_user.role not in ['Admin', 'Staff']:
        abort(403)
    from backend.logic.reporting import generate_cohort_report
    pdf_buffer = generate_cohort_report()
    log_action('PDF Download', 'Downloaded cohort risk summary report.')
    from flask import send_file
    return send_file(pdf_buffer, as_attachment=True,
                     download_name='Cohort_Risk_Report.pdf', mimetype='application/pdf')

@admin_bp.route('/users')
@login_required
def users():
    if current_user.role != 'Admin':
        abort(403)
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/users/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'Admin':
        abort(403)
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'danger')
        return redirect(url_for('admin.users'))

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    
    log_action('User Created', f'Created new {role}: {email}')
    flash(f'User {email} created successfully as {role}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if current_user.role != 'Admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('admin.users'))
    user.is_active = not user.is_active
    db.session.commit()
    status = 'Activated' if user.is_active else 'Deactivated'
    log_action('User Status Changed', f'{status} user {user.email}')
    flash(f'User {user.email} has been {status.lower()}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@login_required
def change_user_role(user_id):
    if current_user.role != 'Admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ['Admin', 'Staff']:
        old_role = user.role
        user.role = new_role
        db.session.commit()
        log_action('Role Change', f'Changed {user.email} from {old_role} to {new_role}')
        flash(f'{user.email} is now a {new_role}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/risk-rules')
@login_required
def risk_rules():
    if current_user.role != 'Admin':
        abort(403)
    rules = RiskRule.query.all()
    return render_template('admin/risk_rules.html', rules=rules)

@admin_bp.route('/risk-rules/update', methods=['POST'])
@login_required
def update_risk_rules():
    if current_user.role != 'Admin':
        abort(403)
    
    for key, value in request.form.items():
        if key.startswith('rule_'):
            rule_key = key.replace('rule_', '')
            rule = RiskRule.query.filter_by(rule_key=rule_key).first()
            if rule:
                rule.value = float(value)
    
    db.session.commit()
    log_action('Risk Rules Update', 'Updated GPA thresholds and/or core failure limits.')
    flash('Risk calculation thresholds updated successfully.', 'success')
    return redirect(url_for('admin.risk_rules'))

@admin_bp.route('/audit-logs')
@login_required
def audit_logs():
    if current_user.role != 'Admin':
        abort(403)
    # Filtering
    action_filter = request.args.get('action', '')
    user_filter = request.args.get('username', '')
    date_filter = request.args.get('date', '')

    query = AuditLog.query
    if action_filter:
        query = query.filter(AuditLog.action.ilike(f'%{action_filter}%'))
    if user_filter:
        matching_users = User.query.filter(User.email.ilike(f'%{user_filter}%')).all()
        ids = [u.id for u in matching_users]
        query = query.filter(AuditLog.user_id.in_(ids))
    if date_filter:
        from datetime import datetime as dt
        try:
            day = dt.strptime(date_filter, '%Y-%m-%d')
            next_day = day.replace(hour=23, minute=59, second=59)
            query = query.filter(AuditLog.timestamp.between(day, next_day))
        except ValueError:
            pass

    logs = query.order_by(AuditLog.timestamp.desc()).limit(200).all()
    all_actions = db.session.query(AuditLog.action).distinct().all()
    return render_template('admin/audit_logs.html', logs=logs,
                           action_filter=action_filter, user_filter=user_filter,
                           date_filter=date_filter,
                           all_actions=[a[0] for a in all_actions])

@admin_bp.route('/audit-logs/export')
@login_required
def export_audit_logs():
    if current_user.role != 'Admin':
        abort(403)
    import csv
    import io
    from flask import Response
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['Timestamp', 'User', 'Action', 'Details'])
    for log in logs:
        user = User.query.get(log.user_id)
        writer.writerow([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            user.email if user else 'Unknown',
            log.action,
            log.details
        ])
    output = si.getvalue()
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=audit_log.csv'})

@admin_bp.route('/courses')
@login_required
def courses():
    if current_user.role != 'Admin':
        abort(403)
    all_courses = Course.query.all()
    return render_template('admin/courses.html', courses=all_courses)

@admin_bp.route('/courses/add', methods=['POST'])
@login_required
def add_course():
    if current_user.role != 'Admin':
        abort(403)
    
    code = request.form.get('course_code')
    title = request.form.get('title')
    units = request.form.get('credit_units')
    is_core = 'is_core' in request.form

    if Course.query.filter_by(course_code=code).first():
        flash('Course code already exists', 'danger')
        return redirect(url_for('admin.courses'))

    new_course = Course(
        course_code=code,
        title=title,
        credit_units=int(units),
        is_core=is_core
    )
    db.session.add(new_course)
    db.session.commit()
    
    log_action('Course Created', f'Added course {code}: {title}')
    flash(f'Course {code} added successfully.', 'success')
    return redirect(url_for('admin.courses'))

@admin_bp.route('/courses/toggle-core/<int:course_id>')
@login_required
def toggle_course_core(course_id):
    if current_user.role != 'Admin':
        abort(403)
    
    course = Course.query.get(course_id)
    if course:
        course.is_core = not course.is_core
        db.session.commit()
        log_action('Course Edited', f'Toggled core status for {course.course_code}')
        flash(f'Updated core status for {course.course_code}.', 'success')
    
    return redirect(url_for('admin.courses'))
