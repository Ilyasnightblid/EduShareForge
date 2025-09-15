# Madrassat Itzer Raiida
## Teacher File Sharing Platform

A secure Flask-based web application designed for teachers to share and access educational files. The platform features role-based access control with admin approval workflow and secure file management.

---

## Description

Madrassat Itzer Raiida is a comprehensive file sharing platform built specifically for educational institutions. It provides a secure environment where:

- **Administrators** can upload files and manage teacher accounts
- **Teachers** can download educational resources after admin approval
- **Security** is maintained through role-based access and approval workflows

---

## Project Structure

```
madrassat-itzer-raiida/
├── app.py                  # Main Flask application
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Landing page
│   ├── login.html         # User login form
│   ├── register.html      # User registration form
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── teacher_dashboard.html # Teacher dashboard
│   └── upload.html        # File upload form (admin only)
├── static/                # Static files
│   ├── css/               # Custom CSS files
│   └── js/                # JavaScript files
├── uploads/               # File storage directory
├── madrassat_itzer_raiida.db  # SQLite database
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Python project configuration
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

---

## Prerequisites

- **Python 3.9+** (recommended: Python 3.11)
- **pip** (Python package installer)
- **Virtual environment** (recommended)

---

## Installation Locale

### 1. Clone the Project

```bash
git clone <repository-url>
cd madrassat-itzer-raiida
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

The database will be created automatically when you first run the application. The first user to register will automatically become an administrator.

### 5. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

---

## Features

### User Management
- **Registration**: New users can register with username, email, and password
- **Admin Approval**: New teacher accounts require admin approval before access
- **Role-based Access**: Separate interfaces for admins and teachers

### File Management
- **Upload**: Administrators can upload files (documents, presentations, etc.)
- **Download**: All approved users can download available files
- **Security**: Secure file handling with type validation

### Security Features
- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask-Login for user sessions
- **Route Protection**: Access control for sensitive operations
- **File Validation**: Allowed file types and size limits

---

## Deployment on PythonAnywhere

### Step 1: Upload Files
1. Upload your project files to PythonAnywhere
2. Extract to your home directory: `/home/yourusername/madrassat-itzer-raiida/`

### Step 2: Install Dependencies
```bash
# In PythonAnywhere console
cd /home/yourusername/madrassat-itzer-raiida
pip3.10 install --user -r requirements.txt
```

### Step 3: Configure WSGI
Create a WSGI configuration file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/madrassat-itzer-raiida'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable for secret key
os.environ['SESSION_SECRET'] = 'your-production-secret-key-here'

from app import app as application

if __name__ == "__main__":
    application.run()
```

### Step 4: Configure Web App
1. Go to the **Web** tab in PythonAnywhere dashboard
2. Create a new web app (Flask/Python 3.10)
3. Set the source code path: `/home/yourusername/madrassat-itzer-raiida`
4. Set the WSGI configuration file path (from Step 3)

### Step 5: Static Files Configuration
1. In the **Static files** section:
   - URL: `/static/`
   - Directory: `/home/yourusername/madrassat-itzer-raiida/static/`

### Step 6: Database Setup
The SQLite database will be created automatically on first run. Ensure the uploads directory has write permissions:

```bash
chmod 755 /home/yourusername/madrassat-itzer-raiida/uploads
```

### Step 7: Environment Variables
Set your production secret key in the WSGI file or use PythonAnywhere's environment variables feature.

---

## Libraries Used

### Core Dependencies
- **Flask** (3.1.2): Web framework
- **Flask-SQLAlchemy** (3.1.1): Database ORM
- **Flask-Login** (0.6.3): User session management
- **Flask-WTF** (1.2.2): Form handling and CSRF protection
- **Werkzeug** (3.1.3): Password hashing and file security
- **SQLAlchemy** (2.0.43): Database toolkit
- **Jinja2** (3.1.6): Template engine

### Frontend Libraries (CDN)
- **Bootstrap 5.1.3**: CSS framework for responsive design
- **Font Awesome 6.0.0**: Icons

### Development Dependencies
- **Blinker**: Signal support
- **Click**: Command line interface creation toolkit
- **ItsDangerous**: Data serialization
- **MarkupSafe**: Safe string handling

---

## Configuration

### Environment Variables
- `SESSION_SECRET`: Secret key for session management (required in production)

### File Upload Settings
- **Maximum file size**: 16MB
- **Allowed file types**: TXT, PDF, PNG, JPG, JPEG, GIF, DOC, DOCX, PPT, PPTX, XLS, XLSX
- **Upload directory**: `uploads/`

### Database
- **Development**: SQLite (`madrassat_itzer_raiida.db`)
- **Production**: SQLite (can be upgraded to PostgreSQL if needed)

---

## Usage

### First Setup
1. Run the application
2. Register the first user (automatically becomes admin)
3. Log in as admin
4. Upload files for teachers
5. Approve teacher registrations

### Admin Workflow
1. Log in to admin dashboard
2. Review and approve/reject pending teacher registrations
3. Upload new files for teachers
4. Manage existing files

### Teacher Workflow
1. Register for an account
2. Wait for admin approval
3. Log in after approval
4. Browse and download available files

---

## Security Considerations

- Change the default secret key in production
- Use HTTPS in production environment
- Regularly update dependencies
- Backup database and uploaded files
- Monitor file upload sizes and types
- Consider implementing file scanning for malware

---

## Support

For technical support or questions about the platform, contact your system administrator.

---

## License

This project is developed for educational purposes. Please ensure compliance with your institution's policies when deploying.

---

**© 2025 Madrassat Itzer Raiida - Teacher File Sharing Platform**