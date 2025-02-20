from flask_login import UserMixin
from flask import current_app
from bson.objectid import ObjectId
from app.utils.auth import check_password

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password_hash')
        
    @staticmethod
    def get(user_id):
        """Get user by ID"""
        try:
            user_data = current_app.db.users.find_one({'_id': ObjectId(user_id)})
            return User(user_data) if user_data else None
        except:
            return None
            
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        user_data = current_app.db.users.find_one({'email': email})
        return User(user_data) if user_data else None
        
    def check_password(self, password):
        """Check password"""
        return check_password(password, self.password_hash) 