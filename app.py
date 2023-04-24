from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

app.secret_key = "l655TiS4OGaxoO17Fg=="

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("sign_in.html")
    
@app.route("/sign-up")
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html") 


if __name__ == "__main__":
    app.run()

