from app import create_app
from backend.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    if not User.query.filter_by(email='hannatu@nile.edu.ng').first():
        user = User(
            username='hannatu', 
            email='hannatu@nile.edu.ng', 
            password_hash=generate_password_hash('staffpassword123'), 
            role='Academic Staff'
        )
        db.session.add(user)
        db.session.commit()
        print('User Created')
    else:
        print('User already exists')
