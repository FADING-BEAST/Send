from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import User, db
from werkzeug.security import check_password_hash
from backend.logic.audit import log_action

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_by_role()
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('This account has been deactivated. Contact your administrator.', 'danger')
                return render_template('auth/login.html')
            login_user(user)
            log_action('Login', f'User {user.email} logged in successfully.')
            return redirect_by_role()
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    log_action('Logout', f'User {current_user.email} logged out.')
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # In production: send email. For demo, store a reset token in session.
            import secrets
            token = secrets.token_urlsafe(24)
            session['reset_token'] = token
            session['reset_user_id'] = user.id
            flash(f'Password reset link generated. Use this token to reset: {token}', 'success')
        else:
            flash('If that email exists in the system, a reset link will be sent.', 'info')
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    reset_token = session.get('reset_token')
    user_id = session.get('reset_user_id')

    if request.method == 'POST':
        token = request.form.get('token')
        new_password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if token != reset_token:
            flash('Invalid or expired reset token.', 'danger')
            return redirect(url_for('auth.reset_password'))

        if new_password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.reset_password'))

        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            session.pop('reset_token', None)
            session.pop('reset_user_id', None)
            flash('Password reset successfully. Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')



@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_pass = request.form.get('current_password')
        new_pass = request.form.get('new_password')
        confirm = request.form.get('confirm_password')

        if not current_user.check_password(current_pass):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('auth.profile'))
        if new_pass != confirm:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('auth.profile'))
        if len(new_pass) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('auth.profile'))

        current_user.set_password(new_pass)
        db.session.commit()
        log_action('Password Change', f'User {current_user.email} changed their password.')
        flash('Password updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html')


def redirect_by_role():
    if current_user.role == 'Admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('staff.dashboard'))
