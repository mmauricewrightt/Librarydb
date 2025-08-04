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

@app.route("/deleteAccount", methods=["DELETE"])
def DeleteAccount():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        data = request.json
        email = data["Email"]

        accountType = getCurrentRole()

        print(email, accountType, 1)

        cursor.execute(f"SELECT * FROM ACCOUNT WHERE email='{email}';")

        account = cursor.fetchone()

        if account is None:
            return make_response({"Message": f"No record of this email: {email}"}, 500)

        if accountType in ("librarian", "admin") and account[-1] == "visitor":
            cursor.execute(f"DELETE FROM ACCOUNT WHERE email='{email}';")
            print(100000)

        elif accountType in ("admin") and account[-1] in("admin", "librarian"):
            cursor.execute(f"DELETE FROM ACCOUNT WHERE email='{email}';")
            print(200000)
        else:
            print(300000)
            return make_response({"Message": "Please consult an admin"}, 500)
            

        cnx.commit()
        return make_response({"Message": f"Account with email: {email} was deleted"}, 200)

    except Exception as e:
        return make_response({"Message": str(e)}, 500)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

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

@app.route("/editAccount", methods=['PUT'])
def editAccount():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        data = request.json

        sessionRole = getCurrentRole()

        email = data["Email"]
        column_to_be_changed = data["Column"]
        new_data = data["New Data"]

        print(111111111111, email)

        if sessionRole not in ("admin", "librarian"):
            return make_response({"Message": "Only admin or librarian can make edits"}, 500)
        
        
        cursor.execute(f"SELECT * FROM ACCOUNT WHERE email = '{email}';")
        
        data_from_email = cursor.fetchone()

        print(22222222222222, data_from_email)

        if data_from_email == None:
            return make_response({"Message": "Email not found"}, 500)
        
        cursor.execute(f"UPDATE ACCOUNT SET {column_to_be_changed} = '{new_data}' WHERE email = '{email}';")

        cnx.commit()
        return make_response({"Message": "%s changed to %s" % (column_to_be_changed, new_data)}, 200)

    except Exception as e:
        return make_response({"Messsage": str(e)}, 500)
    finally:
        if cursor:
            cursor.close()
        if cnx: 
            cnx.close()

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

@app.route("/deleteEvent", methods=["DELETE"])
def DeleteEvent():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        data = request.json
        eventName = data["Event's Name"]

        accountType = getCurrentRole()

        print(eventName, accountType, 1)

        cursor.execute(f"SELECT * FROM CALENDAROFEVENTS WHERE EventName='{eventName}';")

        event = cursor.fetchone()

        if event is None:
            return make_response({"Message": f"No record of this event: {eventName}"}, 500)

        if accountType in ("librarian", "admin"):
            cursor.execute(f"DELETE FROM CALENDAROFEVENTS WHERE EventName='{eventName}';")
            print(100000)
            cnx.commit()
            return make_response({"Message": f"Event: {event} was deleted"}, 200)     

        return make_response({"Message": f"Failed to delete this event: {event}"})       

    except Exception as e:
        return make_response({"Message": str(e)}, 500)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

@app.route("/getEvents", methods=['GET'])
def getEvents():
    try:
        cnx = getDbConnection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM CalendarOfEvents;")

        events = []
        for event_id, event_name, event_date, event_venue in cursor:
            event = {}
            event['id'] = event_id
            event['name'] = event_name
            event['date'] = event_date
            event['venue'] = event_venue

            events.append(event)
    
        cursor.close()
        cnx.close() 
        return make_response(events, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 400)


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)

