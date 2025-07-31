from flask import Flask, jsonify, request, make_response, session
import mysql.connector

app = Flask(__name__)

app.secret_key = "librarydbproject"

def getDbConnection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='maurice',
        password='mauricesystems',
        database='Librarydb'
    )
    return connection

def getCurrentRole():
    return session.get("accountType")

@app.route("/addMember", methods=["POST"])
def AddMember():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        data = request.json

        sessionRole = session.get('accountType')

        fname = data["First Name"]
        lname = data["Last Name"]
        email = data["Email Address"]
        accountType = data["Account Type"]

        if accountType.lower() not in ('admin', 'librarian', 'visitor'):
            return make_response({"Meaasge": "Please ensure that you account is ont of thte following (admin, librarian, visitor)"})

        if accountType in ("admin", "librarian") and sessionRole != "admin":
            return make_response({"Message": "Only Admin can add a member of staff"})

        if accountType == "visitor" and sessionRole not in ("admin", "librarian"):
            return make_response({"Message": "only a member of staff can add new members"})
        
        if not all([fname, lname, email, accountType]):
            return make_response({"Message": "Information Missing"}, 400)

        if sessionRole not in ("admin", "librarian"):
            return make_response({"Message": "Only admin or librarian can add new members"}, 400)

        cursor.execute(f"INSERT INTO ACCOUNT(firstName, lastName, email, accountType) VALUES ('{fname}', '{lname}', '{email}', '{accountType}');")

        cnx.commit()
        return make_response({"Message": "Member added"})
    except Exception as e:
        return make_response({"Message": "Error adding neew user"}, 400)
    finally:
        if cursor:
            cursor.close
        if cnx:
            cnx.close

@app.route("/addBorrower", methods=["POST"])


@app.route("/addEvent", methods=["POST"])
def AddEvent():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        data = request.json

        sessionRole = session.get('accountType')

        eName = data["Name of Event"]
        eDate = data["Date of Event"]
        eVenue = data["Venue of Event"]

      
        if not all([eName, eDate, eVenue]):
            return make_response({"Message": "Information Missing"}, 400)

        if sessionRole not in ("admin", "librarian"):
            return make_response({"Message": "Only admin or librarian can add new Event"}, 400)

        print(8)
        cursor.execute(f"INSERT INTO calendarofevents(eventName, eventDate, eventVenue) VALUES ('{eName}', '{eDate}', '{eVenue}');")
        print(9)
        cnx.commit()
        return make_response({"Message": "Event added"})
    except Exception as e:
        return make_response({"Message": "Error adding new Event"}, 400)
    finally:
        if cursor:
            cursor.close
        if cnx:
            cnx.close



@app.route("/login", methods=["POST"])
def userLogin():
    try:
        if session.get('role') is not None:
            return make_response({"Message": "Cannot login concurrently"}, 400)
        
        cnx = getDbConnection()
        cursor = cnx.cursor()
        data = request.json
        email = data["email"]
        password = data["password"]

        cursor.execute(f"SELECT * FROM Account WHERE email='{email}';")
        user = cursor.fetchone()

        if user is None:
            return make_response({"Error": "Access denied. Re-check login information"}, 401)
        if user[-1] not in ('admin', 'librarian'):
            return make_response({"Message": "Unauthorized attempt"})
        if password == (user[1]+user[-1]).lower():
            session["accountType"] = user[-1]
            return make_response({"Message": f"Welcome {user[1]}"})
        
    except Exception as e:
        return make_response({"Error": str(e)}, 500)
    
@app.route("/test", methods=['GET'])
def test():
    return "connected"

@app.route("/getLibrarians", methods=['GET'])
def getLibrarians():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM Account WHERE accountType = 'librarian';")

        librarians = []
        for id, fname, lname, email, account in cursor:
            librarian = {}
            librarian['ID'] = id
            librarian['firstName'] = fname
            librarian['lastName'] = lname
            librarian['email'] = email
            librarian['accountType'] = account

            librarians.append(librarian)
    
        cursor.close()
        cnx.close() 
        return make_response(librarians, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 400)
    

@app.route("/getVisitors", methods=['GET'])
def getVisitors():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM Account WHERE accountType = 'visitor';")

        visitors = []
        for id, fname, lname, email, account in cursor:
            visitor = {}
            visitor['ID'] = id
            visitor['firstName'] = fname
            visitor['lastName'] = lname
            visitor['email'] = email
            visitor['accountType'] = account

            visitors.append(visitor)
    
        cursor.close()
        cnx.close() 
        return make_response(visitors, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 400)


@app.route("/getAdmins", methods=['GET'])
def getAdmins():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM Account WHERE accountType = 'admin';")

        admins = []
        for id, fname, lname, email, account in cursor:
            admin = {}
            admin['ID'] = id
            admin['firstName'] = fname
            admin['lastName'] = lname
            admin['email'] = email
            admin['accountType'] = account

            admins.append(admin)
    
        cursor.close()
        cnx.close() 
        return make_response(admins, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 400)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

