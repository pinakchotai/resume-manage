# Resume Portal

A Python-based web application for collecting, storing, and managing resumes. Built with Flask and MongoDB.

## Features

- Resume submission with file upload
- Admin dashboard for resume management
- Advanced search and filtering capabilities
- Analytics dashboard
- Email notifications
- Secure authentication system

## Setup

1. Clone the repository
```bash
git clone <repository-url>
cd resumeportal
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file with required environment variables
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
MONGODB_URI=your-mongodb-uri
MAIL_SERVER=your-mail-server
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
```

5. Run the application
```bash
flask run
```

## Project Structure

```
resumeportal/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   ├── templates/
│   └── utils/
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 