from urllib.robotparser import RequestRate
from flask import Flask, redirect, render_template, request
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import json
from sqlalchemy import create_engine
app = Flask(__name__)
dialect = "mysql"
username = "root"
psw = ""
host="127.0.0.1"
dbname = "HomeDB"
engine = create_engine(f"{dialect}://{username}:{psw}@{host}/{dbname}")


def load_insert_box():
    query_list=[]
    page="insertBox.html"
    query="SELECT RoomID,RoomName from Room"
    query_list.append(query)
    return page,query_list
def load_insert_object():
    page="insertObject.html"
    query_list=[]
    query= "SELECT ObjectId,ObjectName from Objects"
    query_list.append(query)
    query="SELECT ROOMID, COUNT(DISTINCT BOXID)\
           FROM BOXES\
           GROUP BY ROOMID"
    query_list.append(query)
    query="SELECT RoomID,RoomName from Room"
    query_list.append(query)
    return page,query_list
def load_search():
    page="search.html"
    query_list=[]
    query="SELECT ObjectId,ObjectName\
           FROM objects"
    query_list.append(query)
    return page,query_list



@app.route("/")
def index():    
    try:
        return render_template("index.html")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return render_template('error.html')

@app.route("/createObject",methods=["GET","POST"])
def createObject():
    if(request.method =='GET'):
        ObjectName=request.args.get('ObjectName')
        ObjectID=request.args.get('ObjectID')
        PathImage=request.args.get('PathImage')
    else:
        ObjectName=request.form['ObjectName']
        ObjectID=request.form['ObjectID']
        PathImage=request.form['PathImage']
    con = engine.connect()
    try:
        query=f"START TRANSACTION;\
                INSERT INTO Objects(ObjectName,ObjectID,PathImage)\
                VALUES('{ObjectName}','{ObjectID}','{PathImage}');\
                COMMIT;"
        result=con.execute(query)
        con.close()
    except (SQLAlchemyError) as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render_template('error.html', error_message=error)

    ######
    return render_template("success.html",text="Object created successfully!",buttmsg=" return to createObject",url="createObject.html")

@app.route("/insertObject",methods=["GET","POST"])
def insertObject():
    if(request.method =='GET'):
        BoxID=request.args.get('BoxID')
        ObjectID=request.args.get('ObjectID')
        RoomID=request.args.get('RoomID')
    else:
        BoxID=request.form['BoxID']
        ObjectID=request.form['ObjectID']
        RoomID=request.form['RoomID']
    con = engine.connect()
    try:
        query=f"START TRANSACTION;\
                INSERT INTO INSIDE(BoxId,ObjectID,RoomID)\
                VALUES('{BoxID}','{ObjectID}','{RoomID}');\
                COMMIT;"
        result=con.execute(query)
        con.close()
    except (SQLAlchemyError) as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render_template('error.html', error_message=error)

    ######
    print(BoxID,ObjectID,RoomID)
    return render_template("success.html",text="Object inserted successfully!",buttmsg=" return to insertObject",url="insertObject.html")
@app.route("/insertBox",methods=["GET","POST"])
def insertBox():
    if(request.method =='GET'):
        BoxID=request.args.get('BoxID')
        Position=request.args.get('Position')
        RoomID=request.args.get('RoomID')
    else:
        BoxID=request.form['BoxID']
        Position=request.form['Position']
        RoomID=request.form['RoomID']
    con = engine.connect()
    try:
        query=f"START TRANSACTION;\
                INSERT INTO BOXES(BoxId,Position,RoomID)\
                VALUES('{BoxID}','{Position}','{RoomID}');\
                COMMIT;"
        result=con.execute(query)
        con.close()
    except (SQLAlchemyError) as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render_template('error.html', error_message=error)

    ######

    return render_template("success.html",text="Box inserted successfully!",buttmsg=" return to insertBox",url="insertBox.html")
@app.route("/insertRoom",methods=["GET","POST"])
def insertRoom():
    if(request.method =='GET'):
        RoomID=request.args.get('RoomID')
        RoomName=request.args.get('RoomName')
    else:
        RoomID=request.form['RoomID']
        RoomName=request.form['RoomName']
    con = engine.connect()
    try:
        query=f"START TRANSACTION;\
                INSERT INTO Room(RoomID,RoomName)\
                VALUES('{RoomID}','{RoomName}');\
                COMMIT;"
        result=con.execute(query)
        con.close()
    except (SQLAlchemyError) as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render_template('error.html', error_message=error)

    return render_template("success.html",text="Room inserted successfully!",buttmsg=" return to insertRoom",url="insertRoom.html")

@app.route("/selectAction",methods=["GET","POST"])
def selectAct():
    page=""
    query=""
    query_list=[]
    result_query_list=[]
    if(request.method =='GET'):
        action=request.args.get('act')
    else:
        action=request.form['act']
    con=engine.connect()
    if(int(action)<5 or int(action) >7):
        if (action=="0"):
            page,query_list=load_search()
        elif (action=="1"):
            page,query_list=load_insert_box()
        elif (action=="2"):
            page="insertRoom.html"
        elif (action=="3"):
            page,query_list=load_insert_object()
        elif (action=="4"):
            page="createObject.html"
        if (len(query_list)>0):
            result_query_list=[]
            for q in query_list:
                result=con.execute(q)
                result_query_list.append(result)
        #print(result_query_list[0].keys())
        
        return render_template(page,results=result_query_list) 
    else:
        if (action=="5"):
            tableName="Objects"
        elif (action=="6"):
            tableName="Boxes"
        elif (action=="7"):
            tableName="Room"
        try:
            query=f"SELECT *\
                    FROM {tableName};"
            table=con.execute(query)
            columns=table.keys()
            con.close()
            return render_template("displayAll.html",table=table,title=tableName,columns=columns)
        except (SQLAlchemyError) as e:
            error = str(e.__dict__['orig'])
            print(error)
            return render_template('error.html', error_message=error)

@app.route("/redirect",methods=["GET","POST"])
def redirect():
    if(request.method =='GET'):
        redirect=request.args.get('redirect')
    else:
        redirect=request.form['redirect']
    if(redirect=="insertBox.html"):
        page,query_list=load_insert_box()
    elif (redirect=="insertObject.html"):
        page,query_list=load_insert_object()
    con=engine.connect()
    result_query_list=[]
    for q in query_list:
                result=con.execute(q)
                result_query_list.append(result)
    return render_template(redirect,results=result_query_list)
@app.route("/sendBoxOption",methods=["GET","POST"])
def test():
    if request.method == "POST":
        jsonData = request.get_json()
        print("RoomID:",jsonData['RoomID'])
        con=engine.connect()
        query=f"SELECT BoxId,Position\
                 FROM BOXES\
                 WHERE ROOMID={jsonData['RoomID']}"
        boxes=con.execute(query)
        boxes_headers=boxes.keys()
        con.close()
        json_data=[]
        for result in boxes:
            print(dict(result))
            json_data.append(dict(result))
        return json.dumps(json_data)
@app.route("/searchObject",methods=["GET","POST"])
def searchObject():
    if(request.method =='POST'):
        jsonData = request.get_json()
        ObjectID=jsonData['ObjectID']
    con=engine.connect()
    query=f"SELECT boxes.BoxId,Position,RoomName\
            FROM boxes,inside,room\
            WHERE boxes.RoomID=room.RoomID and boxes.BoxId=inside.BoxId and ObjectId={ObjectID}"
    results=con.execute(query)
    con.close()
    json_data=[]
    for result in results:
        print(dict(result))
        json_data.append(dict(result))
    return json.dumps(json_data)
app.run(debug=True)

