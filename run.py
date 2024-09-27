from app import create_app
from flask import render_template,request,redirect,url_for
from admin import admin_bp
from student import student_bp
from models import Student,db


app = create_app()

app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
@app.route('/')
def main():
    return render_template('Home.html')
@app.route('/home')
def home():
    return render_template('Home.html')
@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method =='POST':
        name=request.form['name']
        roll_no=request.form['roll_no']
        course=request.form['course']
        password=request.form['password']

        new_student = Student(name=name,roll_no=roll_no,password=password,course=course)

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('success'))
        except:
            return "You have already Signed Up"
@app.route('/success')        
def success():
    return "<h3>You have Successfully Signed Up</h3>"

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
