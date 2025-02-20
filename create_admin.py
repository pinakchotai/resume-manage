from pymongo import MongoClient
from app.utils.auth import hash_password
import os
from dotenv import load_dotenv

def create_admin_user(email, password):
    # Load environment variables
    load_dotenv()
    
    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/resumeportal'))
    db = client.get_database()
    
    # Check if admin already exists
    existing_admin = db.users.find_one({'email': email})
    if existing_admin:
        print(f"Admin user {email} already exists!")
        return
    
    # Create admin user
    admin_user = {
        'email': email,
        'password_hash': hash_password(password),
        'role': 'admin'
    }
    
    # Insert into database
    result = db.users.insert_one(admin_user)
    
    if result.inserted_id:
        print(f"Admin user {email} created successfully!")
    else:
        print("Failed to create admin user!")

if __name__ == '__main__':
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    create_admin_user(email, password) 