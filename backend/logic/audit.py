from flask_login import current_user
from backend.models import db, AuditLog

def log_action(action, details=None):
    """Logs a system action for audit purposes."""
    try:
        user_id = current_user.id if current_user and current_user.is_authenticated else None
        log = AuditLog(
            user_id=user_id,
            action=action,
            details=details
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Failed to log audit action: {e}")
