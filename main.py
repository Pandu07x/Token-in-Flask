from flask import *
from flask_session import Session
import jwt
import datetime
from functools import wraps

app=Flask(__name__)
app.config["SECRET_KEY"]='thisiskey'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=1)
Session(app)
def token_decode(tok):
    return jwt.decode(tok,app.config["SECRET_KEY"],algorithms=["HS256"])
@app.route("/getDetails")




def home():
    source=request.args["APIKEY"]
    #head=request.headers["X-Frame-Options"]
    data={
        "respo":"",
        "stauts":""
    }
    if source=="1234" :
        data["respo"]="Welcome To API KEy"
    else:
        data["respo"]="ISSUE IN HEADER OR API KEY"

    return data
@app.route("/get")

def get():
    return jsonify({'message':"Token Found"})
@app.route("/login")
def login():
    auth=request.authorization
    if auth and auth.password=="password":
        token=jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config["SECRET_KEY"])
        session["token"]=token
        print(jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"]))
        return jsonify({"token":token,"session-token":token_decode(session["token"])})
    app.permanent_session_lifetime=datetime.timedelta(minutes=1)
    return make_response("could verify",401,{'www-Authenticate':"Basic realm='login Required'"})

if __name__=="__main__":
    app.run(debug=True)
