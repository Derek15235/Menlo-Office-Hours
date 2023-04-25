from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

app.secret_key = "l655TiS4OGaxoO17Fg=="

@app.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in.html")
    
    else:
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
        if db_session.query(Student).where(Student.email == request.form["email"]).first() is not None:
            flash("This Email is Already Taken! Try again", )
            return render_template("sign_up.html")
        elif request.form["password"] != request.form["confirm"]:
            flash("Passwords Do Not Match! Try again", "error")
            return render_template("sign_up.html")
        session["role"] = "student"
        db_session.add(Student(request.form["fname"], request.form["lname"], request.form["email"], request.form["password"]))
        db_session.commit()
        # Try to find simpler way
        session["id"] = db_session.query(Student).where(Student.email == request.form["email"]).first().id
        return redirect(url_for("meetings"))
            
    

@app.route("/meetings", methods=["GET", "POST"])
def meetings():
    if request.method == "GET" and session["role"] == "student":
        dict = {}
        meetings = db_session.query(Meeting).where(Meeting.student_id == session["id"]).all()
        for meeting in meetings:
            teacher = db_session.query(Teacher).where(Teacher.id == meeting.teacher_id).first()
            dict[meeting] = [teacher, meeting.date, meeting.time]
        return render_template("student_meetings.html", meetings=dict)
    elif request.method == "GET" and session["role"] == "teacher":
        dict = {}
        meetings = db_session.query(Meeting).where((Meeting.teacher_id == session["id"]) & (Meeting.student_id != None)).all()
        print(meetings)
        for meeting in meetings:
            student = db_session.query(Student).where(Student.id == meeting.student_id).first()
            dict[meeting] = [student, meeting.date, meeting.time]
        return render_template("teacher_meetings.html", meetings=dict)
    
@app.route("/availble", methods=["GET", "POST"])
def availble():
    if request.method == "GET":
        return render_template("availble.html")
    else:
        time = request.form["time"] + " " + request.form["indicator"]
        db_session.add(Meeting(request.form["date"], time, session["id"]))
        db_session.commit()
        flash("Meeting Time Successfully Submitted!", "info")
        return render_template("availble.html")

@app.route("/scheduling", methods=["GET", "POST"])
def schedule():
    if request.method == "GET":
        return render_template("schedule_options.html", teachers=db_session.query(Teacher).all())
    else:
        return redirect(url_for("times",teacher=request.form["teacher_id"]))
    

@app.route("/times/<teacher>", methods=["GET", "POST"])
def times(teacher):
    if request.method == "GET":
        dict = {}
        meetings = db_session.query(Meeting).where((Meeting.teacher_id == teacher)).order_by(Meeting.date.asc()).all()
        for meeting in meetings:
            availble = []
            times = db_session.query(Meeting).where((Meeting.teacher_id == teacher) & (Meeting.date == meeting.date) & (Meeting.student_id == None)).all()
            for time in times:
                availble.append(time)
            dict[meeting.date] = availble
        
        return render_template("meeting_times.html",dates=dict,teacher=teacher)
    else:
        meeting = db_session.query(Meeting).where(Meeting.id == request.form["meeting_id"]).first()
        meeting.student_id = session["id"]
        meeting.description = request.form["description"]
        db_session.commit()
        return redirect(url_for("meetings"))



    


    
    

@app.before_first_request
def setup():
    init_db()



if __name__ == "__main__":
    app.run(debug=True)

