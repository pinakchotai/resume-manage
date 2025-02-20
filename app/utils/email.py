from flask import current_app
from flask_mail import Message
from app import mail

def send_confirmation_email(email, name):
    """Send confirmation email to applicant"""
    if not current_app.config['ENABLE_EMAIL']:
        current_app.logger.info("Email sending is disabled. Skipping confirmation email.")
        return
        
    msg = Message(
        'Resume Submission Confirmation',
        recipients=[email]
    )
    
    msg.body = f"""Dear {name},

Thank you for submitting your resume to our system. We have received your application and it is now in our database.

We will review your application and contact you if your qualifications match our requirements.

Best regards,
The Resume Portal Team
"""
    
    msg.html = f"""
    <p>Dear {name},</p>
    <p>Thank you for submitting your resume to our system. We have received your application and it is now in our database.</p>
    <p>We will review your application and contact you if your qualifications match our requirements.</p>
    <p>Best regards,<br>The Resume Portal Team</p>
    """
    
    mail.send(msg)

def send_password_reset_email(user):
    """Send password reset email to admin user"""
    if not current_app.config['ENABLE_EMAIL']:
        current_app.logger.info("Email sending is disabled. Skipping password reset email.")
        return
        
    token = user.get_reset_password_token()
    msg = Message(
        'Password Reset Request',
        recipients=[user.email]
    )
    
    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    
    msg.html = f"""
    <p>To reset your password, <a href="{url_for('auth.reset_password', token=token, _external=True)}">click here</a>.</p>
    <p>If you did not make this request then simply ignore this email and no changes will be made.</p>
    """
    
    mail.send(msg) 