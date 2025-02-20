from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.utils.email import send_confirmation_email
from app.utils.validators import allowed_file
from app.utils.gridfs_storage import save_file, get_file
import io
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage with service information"""
    return render_template('main/index.html')

@main.route('/submit', methods=['GET', 'POST'])
def submit_resume():
    """Resume submission form"""
    if request.method == 'POST':
        # Get form data
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'summary': request.form.get('summary'),
            'skills': request.form.get('skills').split(','),
            'submission_date': datetime.utcnow()
        }
        
        # Handle file upload
        if 'resume' not in request.files:
            flash('No resume file uploaded', 'error')
            return redirect(request.url)
            
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Save file to GridFS
            try:
                file_id = save_file(
                    file.read(),
                    filename=filename,
                    content_type=file.content_type
                )
                data['resume_file_id'] = file_id
                data['resume_filename'] = filename
            except Exception as e:
                current_app.logger.error(f"Failed to save file: {str(e)}")
                flash('Failed to save resume file. Please try again.', 'error')
                return redirect(request.url)
            
            # Save to database
            current_app.db.resumes.insert_one(data)
            
            # Handle email confirmation
            if current_app.config['ENABLE_EMAIL']:
                try:
                    send_confirmation_email(data['email'], data['name'])
                    flash('Resume submitted successfully! A confirmation email has been sent.', 'success')
                except Exception as e:
                    current_app.logger.error(f"Failed to send confirmation email: {str(e)}")
                    flash('Resume submitted successfully! However, we could not send a confirmation email.', 'warning')
            else:
                flash('Resume submitted successfully! Email notifications are currently disabled.', 'success')
            
            return redirect(url_for('main.index'))
        else:
            flash('Invalid file type. Please upload PDF or DOCX files only.', 'error')
            return redirect(request.url)
            
    return render_template('main/submit.html')

@main.route('/resume/<resume_id>/download')
def download_resume(resume_id):
    """Download resume file from GridFS"""
    resume = current_app.db.resumes.find_one({'_id': ObjectId(resume_id)})
    if not resume or 'resume_file_id' not in resume:
        flash('Resume file not found', 'error')
        return redirect(url_for('main.index'))
        
    grid_out = get_file(resume['resume_file_id'])
    if not grid_out:
        flash('Resume file not found', 'error')
        return redirect(url_for('main.index'))
        
    # Create in-memory file
    file_data = io.BytesIO(grid_out.read())
    file_data.seek(0)
    
    return send_file(
        file_data,
        download_name=resume['resume_filename'],
        mimetype=grid_out.content_type
    )

@main.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('main/privacy.html')

@main.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('main/terms.html') 