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
        return render_template("student_meetings.html")
    elif request.method == "GET" and session["role"] == "teacher":
        return render_template("teacher_meetings.html")
    
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


    
    

@app.before_first_request
def setup():
    init_db()



if __name__ == "__main__":
    app.run(debug=True)

