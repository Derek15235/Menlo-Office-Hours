"""
A universal Menlo website that lets students and teachers 
create/schedule one on one meetings

Created by: Derek Jain
Date: April 2023
"""

from flask import *
from database import init_db, db_session
from models import *
from datetime import datetime

app = Flask(__name__)

app.secret_key = "l655TiS4OGaxoO17Fg=="

@app.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html")
    else:
        # If the email is in one of these databases, continue the site with the corresponding base files
        if db_session.query(Student).where((Student.email == request.form["email"]) & (Student.password == request.form["password"])).first() is not None:
            session["role"] = "student"
            session["id"] = db_session.query(Student).where((Student.email == request.form["email"]) & (Student.password == request.form["password"])).first().id
            return redirect(url_for("meetings"))
        elif db_session.query(Teacher).where((Teacher.email == request.form["email"]) & (Teacher.password == request.form["password"])).first() is not None:
            session["role"] = "teacher"
            session["id"] = db_session.query(Teacher).where((Teacher.email == request.form["email"]) & (Teacher.password == request.form["password"])).first().id
            return redirect(url_for("meetings"))
        
        flash("Incorrect Password or Email! Try Again", "error")
        return render_template("sign_in.html")
        


    
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html") 
    else:
        # Make sure email is not already taken
        if db_session.query(Student).where(Student.email == request.form["email"]).first() is not None:
            flash("This Email is Already Taken! Try again", )
            return render_template("sign_up.html")
        # Make sure passwords match
        elif request.form["password"] != request.form["confirm"]:
            flash("Passwords Do Not Match! Try again", "error")
            return render_template("sign_up.html")
        # Contnue sign in with updating session info on current user and enter them into database
        session["role"] = "student"
        # Get current date in the form mm/dd
        db_session.add(Student(request.form["fname"], request.form["lname"], request.form["email"], request.form["password"]))
        db_session.commit()
        session["id"] = db_session.query(Student).where(Student.email == request.form["email"]).first().id
        return redirect(url_for("meetings"))
            
    

@app.route("/meetings", methods=["GET", "POST"])
def meetings():
    if request.method == "GET":
        # Ensure that person had logged in
        if session["id"] is None:
                return redirect(url_for("sign_in"))
    else:
        canceled_meeting = db_session.query(Meeting).where(Meeting.id == request.form["meeting_id"]).first()
        if session["role"] == "student":
            canceled_meeting.student_id = None
            canceled_meeting.description = None
        else:
            db_session.delete(canceled_meeting)
        db_session.commit()
    # Show the meetings the user has schedule
    if session["role"] == "student":
        dict = {}
        meetings = db_session.query(Meeting).where((Meeting.student_id == session["id"]) & (Meeting.date >= session["date"])).all()
        for meeting in meetings:
            teacher = db_session.query(Teacher).where(Teacher.id == meeting.teacher_id).first()
            dict[meeting] = [teacher, meeting.date, meeting.time, meeting.description]
        return render_template("student_meetings.html", meetings=dict)
    elif session["role"] == "teacher":
        dict = {}
        meetings = db_session.query(Meeting).where((Meeting.teacher_id == session["id"]) & (Meeting.student_id != None) & (Meeting.date >= session["date"])).all()
        print(meetings)
        for meeting in meetings:
            student = db_session.query(Student).where(Student.id == meeting.student_id).first()
            dict[meeting] = [student, meeting.date, meeting.time, meeting.description]
        return render_template("teacher_meetings.html", meetings=dict)
    
@app.route("/availble", methods=["GET", "POST"])
def availble():
    if request.method == "GET":
        # Ensure that person had logged in
        if session["id"] is None:
            return redirect(url_for("sign_in"))
    else:
        # Create the meeting with the inputted time and the teacher's id
        time = request.form["time"] + " " + request.form["indicator"]
        date = request.form["date"]
        meeting = db_session.query(Meeting).where((Meeting.time == time) & (Meeting.date == date) & (Meeting.student_id == None) & (Meeting.teacher_id == session["id"])).first()
        # If the user puts in an already existing time, cancel that meeting, otherwise schedule a new meeting
        if meeting is not None:
            db_session.delete(meeting)
            db_session.commit()
            flash("Meeting Time Successfully Canceled!")
        else: 
            db_session.add(Meeting(request.form["date"], time, session["id"]))
            db_session.commit()
            flash("Meeting Time Successfully Submitted!", "info")
    # Show all empty meetings that are scheduled for future dates
    dict = {}
    meetings = db_session.query(Meeting).where((Meeting.teacher_id == session["id"]) & (Meeting.date >= session["date"])).order_by(Meeting.date.asc()).all()
    for meeting in meetings:
        availble = []
        times = db_session.query(Meeting).where((Meeting.teacher_id == session["id"]) & (Meeting.date == meeting.date) & (Meeting.student_id == None)).order_by(Meeting.time.asc()).all()
        for time in times:
            availble.append(time)
        dict[meeting.date] = availble
    return render_template("availble.html", dates=dict)

@app.route("/scheduling", methods=["GET", "POST"])
def schedule():
    if request.method == "GET":
        # Ensure that person had logged in
        if session["id"] is None:
            return redirect(url_for("sign_in"))
        # Filter which teachers are shown, and default is all of them
        department = request.args.get("department")
        if department is None or department == "All":
            selected_teachers = db_session.query(Teacher).all()
        else:
            selected_teachers = db_session.query(Teacher).where(Teacher.department == department).all()
        return render_template("schedule_options.html", teachers=selected_teachers)
    else:
        # Redirect to page to finalize scheduling meeting
        return redirect(url_for("times",teacher=request.form["teacher_id"]))
    

@app.route("/times/<teacher>", methods=["GET", "POST"])
def times(teacher):
    if request.method == "GET":
        # Ensure that person had logged in
        if session["id"] is None:
            return redirect(url_for("sign_in"))
        # Create a dictionary where each (future or current) date has a list of meetings attached to it
        dict = {}
        meetings = db_session.query(Meeting).where((Meeting.teacher_id == teacher) & (Meeting.date >= session["date"])).order_by(Meeting.date.asc()).all()
        for meeting in meetings:
            availble = []
            times = db_session.query(Meeting).where((Meeting.teacher_id == teacher) & (Meeting.date == meeting.date) & (Meeting.student_id == None)).order_by(Meeting.time.asc()).all()
            for time in times:
                availble.append(time)
            dict[meeting.date] = availble  
        return render_template("meeting_times.html",dates=dict,teacher=teacher)
    else:
        # When student selects a time, fill in required fields to attach them to the meeting
        meeting = db_session.query(Meeting).where(Meeting.id == request.form["meeting_id"]).first()
        meeting.student_id = session["id"]
        meeting.description = request.form["description"]
        db_session.commit()
        return redirect(url_for("meetings")) 

@app.route("/cancel/<meeting_id>/<function>")
def cancel(meeting_id,function):
    db_session.delete(db_session.query(Meeting).where(Meeting.id == meeting_id).first())
    db_session.commit()
    return redirect(url_for(function))


@app.before_first_request
def setup():
    init_db()
    session["date"] = str(datetime.now())[5:10].replace("-", "/")
    



if __name__ == "__main__":
    app.run(debug=True)

