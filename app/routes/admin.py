from flask import Blueprint, render_template, request, current_app, send_file, abort, jsonify
from flask_login import login_required
from bson import ObjectId
import os
from app.utils.db import verify_db_connection
from app.utils.gridfs_storage import get_file
import io

admin = Blueprint('admin', __name__)

@admin.route('/dbstatus')
@login_required
def db_status():
    """Check database connection status"""
    return jsonify(verify_db_connection())

@admin.route('/dashboard')
@login_required
def dashboard():
    # Get page number for pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get filter parameters
    search = request.args.get('search', '')
    skill_filter = request.args.get('skill', '')
    
    # Build query
    query = {}
    if search:
        query['$or'] = [
            {'name': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}},
            {'summary': {'$regex': search, '$options': 'i'}}
        ]
    if skill_filter:
        query['skills'] = {'$regex': skill_filter, '$options': 'i'}
    
    # Get total count for pagination
    total = current_app.db.resumes.count_documents(query)
    
    # Get resumes with pagination
    resumes = current_app.db.resumes.find(query) \
        .sort('submission_date', -1) \
        .skip((page - 1) * per_page) \
        .limit(per_page)
    
    # Get unique skills for filter dropdown
    all_skills = current_app.db.resumes.distinct('skills')
    
    # Get database status
    db_info = verify_db_connection()
    
    return render_template('admin/dashboard.html',
                         resumes=resumes,
                         total=total,
                         page=page,
                         per_page=per_page,
                         search=search,
                         skill_filter=skill_filter,
                         all_skills=all_skills,
                         db_info=db_info)

@admin.route('/resume/<resume_id>')
@login_required
def view_resume(resume_id):
    resume = current_app.db.resumes.find_one({'_id': ObjectId(resume_id)})
    if not resume:
        abort(404)
    return render_template('admin/resume_detail.html', resume=resume)

@admin.route('/resume/<resume_id>/download')
@login_required
def download_resume(resume_id):
    resume = current_app.db.resumes.find_one({'_id': ObjectId(resume_id)})
    if not resume or 'resume_file_id' not in resume:
        abort(404)
        
    grid_out = get_file(resume['resume_file_id'])
    if not grid_out:
        abort(404)
        
    # Create in-memory file
    file_data = io.BytesIO(grid_out.read())
    file_data.seek(0)
    
    return send_file(
        file_data,
        download_name=resume['resume_filename'],
        mimetype=grid_out.content_type
    ) 