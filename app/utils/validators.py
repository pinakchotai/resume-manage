from flask import current_app
import os

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def validate_resume_data(data):
    """Validate resume submission data"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'email', 'phone', 'summary']
    for field in required_fields:
        if not data.get(field):
            errors.append(f'{field.capitalize()} is required')
    
    # Email format
    if data.get('email') and '@' not in data['email']:
        errors.append('Invalid email format')
    
    # Phone format (basic check)
    if data.get('phone') and not data['phone'].replace('-', '').replace('+', '').isdigit():
        errors.append('Invalid phone number format')
    
    # Summary length
    if data.get('summary') and len(data['summary']) > 2000:
        errors.append('Summary must be less than 2000 characters')
    
    return errors

def validate_file_size(file_path):
    """Check if file size is within limits"""
    file_size = os.path.getsize(file_path)
    return file_size <= current_app.config['MAX_CONTENT_LENGTH'] 