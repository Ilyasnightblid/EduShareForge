# Madrassat Itzer Raiida

## Overview

Madrassat Itzer Raiida is a complete, secure educational file-sharing platform built with Flask. The application serves as a centralized repository where administrators can upload educational resources and approved teachers can access and download these files. The platform implements a robust role-based access control system with an admin approval workflow to ensure security and proper user management.

**Project Status: COMPLETED**

The application is fully functional and production-ready, featuring:
- Secure user authentication and authorization
- Admin approval workflow for teacher accounts
- File upload and download functionality with security controls
- Modern, responsive web interface
- Comprehensive documentation and deployment guides

## Recent Changes

**September 15, 2025**
- ✅ **Complete Flask Application**: Built from scratch with modular structure
- ✅ **Database Models**: User and File models with SQLAlchemy and SQLite
- ✅ **Authentication System**: Registration, login, logout with Flask-Login
- ✅ **Admin Approval Workflow**: Pending/approved user status management
- ✅ **Secure File Management**: UUID-based unique filenames, CSRF protection
- ✅ **Role-based Access Control**: Admin vs Teacher permissions with server-side enforcement
- ✅ **Web Interface**: Bootstrap-styled templates for all functionality
- ✅ **Security Hardening**: CSRF protection, path traversal prevention, authorization checks
- ✅ **Documentation**: Complete README.md with installation and deployment instructions
- ✅ **Production Configuration**: Environment-based secret management setup

The application has passed comprehensive security review and is ready for deployment.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework Architecture
The application is built using Flask, a lightweight Python web framework, following a monolithic architecture pattern. The entire application logic resides in a single `app.py` file, making it suitable for small to medium-scale educational institutions. This approach simplifies deployment and maintenance while providing all necessary functionality.

### Authentication and Authorization System
The platform implements a multi-layered security model using Flask-Login for session management. User authentication is handled through username/password combinations with secure password hashing using Werkzeug's security utilities. The authorization system distinguishes between three user states:
- **Administrators**: Full access to upload files and manage user accounts
- **Approved Teachers**: Can view and download files after admin approval
- **Pending Teachers**: Limited access until approved by administrators

The first user created automatically becomes an administrator, establishing the initial administrative control.

### Database Design
The application uses SQLite with SQLAlchemy ORM for data persistence. The database schema includes user management tables with status tracking (pending, approved, admin) and file metadata storage. This lightweight database solution is ideal for educational environments with moderate user loads and provides easy backup and migration capabilities.

### File Management System
Files are stored in a local filesystem directory (`uploads/`) with metadata tracked in the database. The system implements secure filename handling using UUID-based naming to prevent conflicts and security issues. File access is controlled through the web application layer, ensuring only authenticated and authorized users can download files.

### Security Measures
- CSRF protection implemented across all forms
- File type validation restricting uploads to educational file formats
- File size limits (16MB maximum) to prevent abuse
- Secure filename handling to prevent directory traversal attacks
- Session-based authentication with secure secret key management

### Template Architecture
The frontend uses Jinja2 templates with Bootstrap 5 for responsive design. A base template provides consistent navigation and styling across all pages, with role-specific dashboards for administrators and teachers. The interface adapts based on user roles, hiding administrative functions from regular teachers.

## External Dependencies

### Core Framework Dependencies
- **Flask 3.1.2**: Primary web framework providing routing, templating, and request handling
- **Flask-SQLAlchemy 3.1.1**: Database ORM integration for simplified database operations
- **Flask-Login 0.6.3**: User session management and authentication framework
- **Flask-WTF 1.2.2**: Form handling with CSRF protection and validation

### Security and Validation
- **Werkzeug 3.1.3**: WSGI utilities including secure password hashing and filename handling
- **WTForms 3.2.1**: Form validation and rendering with file upload support

### Database Layer
- **SQLAlchemy 2.0.43**: Core ORM functionality for database abstraction
- **SQLite**: Embedded database engine (part of Python standard library)

### Frontend Assets
- **Bootstrap 5.1.3**: CSS framework for responsive design and UI components
- **Font Awesome 6.0.0**: Icon library for enhanced user interface elements

### Development and Runtime
- **Python 3.9+**: Runtime environment with modern Python features
- **Jinja2 3.1.6**: Template engine for dynamic HTML generation

The application is designed to run in various environments from development to production, with configuration options for database connections and security settings through environment variables.