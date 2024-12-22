from flask import flash, Blueprint,render_template,send_file,url_for,request,redirect,session,make_response
from models import Student, Attendance, Contact, db
from datetime import datetime
import calendar


student_bp=Blueprint('student',__name__,url_prefix='/student')

@student_bp.before_request
def require_login():
    protected_routes = ['dashboard', 'view_attendance', 'apply_attendance']
    
    # Check if the current request's endpoint is protected and the user is not logged in
    if request.endpoint in protected_routes and 'student_id' not in session:
        flash('You need to sign in to access this page.', 'danger')
        return redirect(url_for('student.signin'))

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.before_request
def require_login():

    protected_routes = ['dashboard', 'view_attendance', 'apply_attendance']
    
    if request.endpoint in protected_routes and 'student_id' not in session:
        flash('You need to sign in to access this page.', 'danger')
        return redirect(url_for('student.signin'))
@student_bp.route('/signin',methods=['GET', 'POST'])
def signin():

    if request.method == 'POST':
        roll_no=request.form.get('roll_no')
        password = request.form.get('password')

        student=Student.query.filter_by(roll_no=roll_no).first()
        if student and student.password==password:
            session['student_id']=student.id
            session['student_name']=student.name
            return redirect(url_for('student.dashboard'))
        else:
            flash("Invalid Roll no or Password","danger")
    return render_template('student_signin.html')
@student_bp.route('/Signup')
def signup():
    return render_template('student_signup.html')

@student_bp.route('/dashboard')
def dashboard():

    if 'student_id' not in session:
        return redirect(url_for('student.signin'))
    student_id = session['student_id']
    student = Student.query.get(student_id)
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    _, num_days = calendar.monthrange(current_year, current_month)

    total_days = Attendance.query.filter_by(student_id=student_id).count()
    total_attendance = round((total_days / num_days) * 100, 2) if num_days > 0 else 0

    today = now.date()
    existing_attendance = Attendance.query.filter_by(student_id=student_id, date=today).first()
    already_marked = existing_attendance is not None
    
    response = make_response(render_template(
        'student_dashboard.html',
        student=student,
        already_marked=already_marked,
        total_attendance=total_attendance
    ))
    response.headers['Cache-Control'] = 'no-store'
    if student:
        return response
    else:
        flash('Student not found', 'danger')
        return redirect(url_for('student.signin'))


@student_bp.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'student_id' not in session:
        return redirect(url_for('student.signin'))
    
    student_id = session['student_id']
    now = datetime.now()
    today = now.date()
    
    # Check if attendance is already marked for today
    existing_attendance = Attendance.query.filter_by(student_id=student_id, date=today).first()
    if not existing_attendance:

        # Add attendance record
        new_attendance = Attendance(student_id=student_id, date=today)
        db.session.add(new_attendance)
        db.session.commit()
        flash('Attendance marked successfully!', 'success')
    else:
        flash('You have already marked attendance for today.', 'info')
    
    return redirect(url_for('student.dashboard'))


@student_bp.route('/attendance')
def view_attendance():
    return "view Attendance"


@student_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('student.signin'))

@student_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Send email to admin with the contact details
        
        db.session.add(Contact(name=name, email=email, message=message))
        db.session.commit()
        # Example: send_email('Contact Form', f'Name: {name}\nEmail: {email}\nMessage: {message}')
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('student.contact'))
    return render_template('contact.html')
# 