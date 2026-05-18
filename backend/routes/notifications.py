from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from backend.models import db, Notification, User

notify_bp = Blueprint('notify', __name__, url_prefix='/notifications')


def push_notification(user_id, title, body, category='info'):
    """Create a notification for a user. Category: info | warning | danger"""
    notif = Notification(user_id=user_id, title=title, body=body, category=category)
    db.session.add(notif)
    db.session.commit()


def push_notification_all(title, body, category='info'):
    """Broadcast a notification to every user in the system."""
    for user in User.query.all():
        push_notification(user.id, title, body, category)


@notify_bp.route('/')
@login_required
def index():
    notifs = Notification.query.filter_by(user_id=current_user.id)\
                               .order_by(Notification.timestamp.desc()).all()
    return render_template('notifications/index.html', notifications=notifs)


@notify_bp.route('/mark-read/<int:notif_id>', methods=['POST'])
@login_required
def mark_read(notif_id):
    n = Notification.query.get_or_404(notif_id)
    if n.user_id == current_user.id:
        n.is_read = True
        db.session.commit()
    return redirect(url_for('notify.index'))


@notify_bp.route('/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False)\
                      .update({'is_read': True})
    db.session.commit()
    return redirect(url_for('notify.index'))


@notify_bp.route('/count')
@login_required
def unread_count():
    """JSON endpoint to get unread notification count (for live badge)."""
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})
