import pytz
from datetime import datetime

from app.extensions import db
from app.models import User
from app.services.pushover_alerts import send_alert

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        try:    
            send_alert(f'<b>{username}</b> ha iniciado sesión.', 0) # Send login alert
            # Update last login
            User.query.filter_by(username=username).update(dict(last_login=datetime.now(pytz.timezone('Europe/Madrid'))))
            db.session.commit()
        except:
            pass
        return True  
    return False


def register(username, password):
    # Check if a user with the same username existing_user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 409
     
    try:
        # Creates the new user instance and set password
        new_user = User(username=username)
        new_user.set_password(password)

        # Add new user to database
        db.session.add(new_user)
        db.session.commit()
    except:
        return 500
    
    try:
        send_alert(f'<b>{username}</b> se ha registrado', 1)
    except:
        pass
    return 200