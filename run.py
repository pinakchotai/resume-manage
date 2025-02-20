from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG', 'production'))

# This is for Vercel
if __name__ == '__main__':
    app.run() 