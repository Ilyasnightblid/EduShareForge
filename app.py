from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///madrassat_itzer_raiida.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Forms
class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(list(ALLOWED_EXTENSIONS), 'Invalid file type!')
    ])
    submit = SubmitField('Upload File')

class ApprovalForm(FlaskForm):
    submit = SubmitField('Submit')

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='teacher')  # 'admin' or 'teacher'
    status = db.Column(db.String(20), default='pending')  # 'pending' or 'approved'
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_approved(self):
        return self.status == 'approved'

# File model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('register.html')

        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        
        # Check if this is the first user - make them admin
        if User.query.count() == 0:
            user.role = 'admin'
            user.status = 'approved'
        
        db.session.add(user)
        db.session.commit()

        if user.is_admin():
            flash('Admin account created successfully. You can now log in.', 'success')
        else:
            flash('Registration successful! Your account is pending approval from an administrator.', 'info')
        
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_approved():
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Your account is pending approval. Please wait for an administrator to approve it.', 'warning')
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_approved():
        abort(403)

    files = File.query.all()
    
    if current_user.is_admin():
        pending_users = User.query.filter_by(status='pending').all()
        approval_form = ApprovalForm()
        return render_template('admin_dashboard.html', files=files, pending_users=pending_users, approval_form=approval_form)
    else:
        return render_template('teacher_dashboard.html', files=files)

@app.route('/admin/approve_user/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    if not current_user.is_admin():
        abort(403)

    form = ApprovalForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        user.status = 'approved'
        db.session.commit()
        flash(f'User {user.username} has been approved.', 'success')
    else:
        flash('Invalid request.', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/admin/reject_user/<int:user_id>', methods=['POST'])
@login_required
def reject_user(user_id):
    if not current_user.is_admin():
        abort(403)

    form = ApprovalForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} has been rejected and removed.', 'info')
    else:
        flash('Invalid request.', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if not current_user.is_admin():
        abort(403)

    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if file and file.filename:
            # Get file extension
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            
            # Generate unique filename using UUID
            unique_filename = str(uuid.uuid4()) + file_ext
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(filepath)

            # Save file info to database
            file_record = File()
            file_record.filename = unique_filename
            file_record.original_filename = filename
            file_record.filepath = filepath
            file_record.uploaded_by = current_user.id
            db.session.add(file_record)
            db.session.commit()

            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))

    return render_template('upload.html', form=form)

@app.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    if not current_user.is_approved():
        abort(403)

    file_record = File.query.get_or_404(file_id)
    
    # Security check: ensure file path is within upload folder
    safe_path = os.path.abspath(file_record.filepath)
    upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    
    if os.path.commonpath([safe_path, upload_folder]) != upload_folder:
        abort(403)
    
    # Check if file exists
    if not os.path.exists(safe_path):
        flash('File not found.', 'error')
        return redirect(url_for('dashboard'))
    
    return send_file(safe_path, as_attachment=True, download_name=file_record.original_filename)

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000, debug=True)