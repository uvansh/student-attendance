from flask import Blueprint,render_template,request,flash,redirect,url_for,session,make_response
from models import db,Admin
import os
from werkzeug.security import generate_password_hash,check_password_hash
from models import db,Admin,Student


admin_bp=Blueprint('admin',__name__,url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin.signin'))
    admin_name=session.get('admin_name')
    students=Student.query.all()
    response = make_response(render_template('admin_dashboard.html', admin_name=admin_name,students=students))
    # Add headers to disable caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1
    response.headers['Pragma'] = 'no-cache'  # HTTP 1.0
    response.headers['Expires'] = '0'  # Proxies
    
    return response

ADMIN_KEY = os.getenv('ADMIN_REGISTRATION_KEY', '09075')

@admin_bp.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        unique_key = request.form['unique_key']
        # Validate the unique key
        if unique_key != ADMIN_KEY:
            flash('Invalid unique key. Please contact staff for the correct key.', 'danger')
            return render_template('admin_register.html')
        
        # Hash the password before saving
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Register the admin
        new_admin = Admin(name=name, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        
        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin.signin'))

@admin_bp.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
        if not name or not password:
            flash('Name and password are required', 'danger')
            return render_template('admin_signin.html')  # Always return a response

        # Query the admin from the database
        admin = Admin.query.filter_by(name=name).first()
        
        if admin:
            # Verify the password
            if check_password_hash(admin.password, password):
                # Set session variables to log in the admin
                session['admin_id'] = admin.id
                session['admin_name'] = admin.name
                flash('Successfully logged in as admin', 'success')
                return redirect(url_for('admin.dashboard'))  # Ensure you return the redirect
            else:
                flash('Incorrect password, please try again.', 'danger')
        else:
            flash('Admin with this name does not exist.', 'danger')

        return render_template('admin_signin.html')  # Return a response in case of failure
    
    # For GET requests, render the login form
    return render_template('admin_signin.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin.signin'))

@admin_bp.route('/add_student',methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        name=request.form.get('name')
        roll_no=request.form.get('roll_no')
        course=request.form.get('course')

        if not name or not roll_no or not course:
            flash('All fields are required', 'danger')
            return redirect(url_for('add_student'))
        existing_student= Student.query.filter_by(roll_no=roll_no).first()

        if existing_student:
            flash('Student with this roll number already exists')
            return redirect(url_for('add_student'))
        
        new_student = Student(name=name,roll_no=roll_no,course=course)
        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully','success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin_add_student.html')

@admin_bp.route('/remove_student/<int:student_id>',methods=['GET','POST'])
def remove_student(student_id):
    student = Student.query.get(student_id)

    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(student)
    db.session.commit()

    flash('student removed successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/view_students')
def view_students():
    students=Student.query.all()
    return render_template('admin_dashboard.html',students=students)