"""Database models"""
import pytz
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

        
class User(UserMixin,db.Model):
    __tablename__ = "users"
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime, nullable=True)
    date_created = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Madrid')), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)