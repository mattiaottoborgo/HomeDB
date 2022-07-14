from urllib.robotparser import RequestRate
from flask import Flask, redirect, render_template, request
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
app = Flask(__name__)
@app.route("/")
def index():
    dialect = "mysql"
    username = "root"
    psw = ""
    host="127.0.0.1"
    dbname = "HomeDB"
    engine = create_engine(f"{dialect}://{username}:{psw}@{host}/{dbname}")
    
    try:
        return render_template("index.html")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return render_template('error.html')
@app.route("/insertBox",methods=["GET","POST"])
def insertBox():
    if(request.method =='GET'):
        BoxNumber=request.args.get('BoxNumber')
        Position=request.args.get('Position')
        Room=request.args.get('Room')
    else:
        BoxNumber=request.form['BoxNumber']
        Position=request.form['Position']
        Room=request.form['Room']
    ######
    print(BoxNumber,Position,Room)
    return render_template("success.html",text="Box inserted successfully!",buttmsg=" return to insertBox",url="insertBox.html")
@app.route("/selectAction",methods=["GET","POST"])
def selectAct():
    if(request.method =='GET'):
        action=request.args.get('act')
    else:
        action=request.form['act']
    if (action=="0"):
        return render_template("search.html")
    elif (action=="1"):
        return render_template("insertBox.html")
    elif (action=="2"):
        return render_template("insertRoom.html")
@app.route("/redirect",methods=["GET","POST"])
def redirect():
    if(request.method =='GET'):
        redirect=request.args.get('redirect')
    else:
        redirect=request.form['redirect']
    return render_template(redirect)
app.run(debug=True)