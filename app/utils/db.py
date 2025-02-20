from flask import current_app
from pymongo.errors import ConnectionFailure

def verify_db_connection():
    """Verify database connection and return connection info"""
    try:
        # The ismaster command is cheap and does not require auth
        current_app.mongo.admin.command('ismaster')
        db_name = current_app.mongo.get_database().name
        return {
            'status': 'connected',
            'database': db_name,
            'collections': current_app.db.list_collection_names()
        }
    except ConnectionFailure:
        return {
            'status': 'error',
            'message': 'Server not available'
        } 