from flask import current_app
from gridfs import GridFS
from bson import ObjectId
import io

def get_gridfs():
    """Get GridFS instance"""
    return GridFS(current_app.db)

def save_file(file_data, filename, content_type):
    """Save file to GridFS"""
    fs = get_gridfs()
    file_id = fs.put(
        file_data,
        filename=filename,
        content_type=content_type
    )
    return file_id

def get_file(file_id):
    """Get file from GridFS"""
    fs = get_gridfs()
    try:
        grid_out = fs.get(ObjectId(file_id))
        return grid_out
    except:
        return None

def delete_file(file_id):
    """Delete file from GridFS"""
    fs = get_gridfs()
    try:
        fs.delete(ObjectId(file_id))
        return True
    except:
        return False 