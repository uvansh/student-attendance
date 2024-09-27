from flask import flash, Blueprint,render_template,send_file,url_for,request,redirect,session,make_response
from models import Student,Attendance,db
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

@student_bp.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student.signin'))
    student_id=session['student_id']
    student = Student.query.get(student_id)
    response = make_response(render_template('student_dashboard.html',student=student))
    response.headers['Cache-Control'] = 'no-store'
    if student:
        return response
    else:
        flash('Student not found','danger')
        return redirect(url_for('student.signin'))


@student_bp.route('/attendance')
def view_attendance():
    return "view Attendance"

@student_bp.route('/Signup')
def signup():
    return render_template('student_signup.html')

@student_bp.route('/signin',methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        roll_no=request.form['roll_no']
        password = request.form['password']
        student=Student.query.filter_by(roll_no=roll_no).first()
        if student and student.password==password:
            session['student_id']=student.id
            session['student_name']=student.name
            return redirect(url_for('student.dashboard'))
        else:
            flash("Invalid Roll no or Password","danger")
    return render_template('student_signin.html')
@student_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('student.signin'))


@student_bp.route('/mark_attendance',methods=['POST'])
def mark_attendance():
    if 'student_id' not in session:
        return redirect(url_for('student.signin'))
    
    student_id=session['student_id']
    student = Student.query.get(student_id)
    now=datetime.now()
    current_year=now.year
    current_month=now.month
    _, num_days = calendar.monthrange(current_year, current_month)

    total_unrou = Attendance.query.filter_by(student_id=student_id).count()/num_days*100
    total_attendance = round(total_unrou,2)
    
    today=datetime.utcnow().date()
    existing_attendance=Attendance.query.filter_by(student_id=student_id,date=today).first()
    already_marked = existing_attendance is not None
    return render_template('student_dashboard.html',student=student,already_marked=already_marked,total_attendance=total_attendance)
