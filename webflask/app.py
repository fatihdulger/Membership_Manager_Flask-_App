from flask import Flask, render_template, request, url_for, redirect, abort, Response
import sqlite3 as sql

# create an instance object of the flask class

app = Flask(__name__) # main class

# create a function to handle db connection

def leisureCentreCon():
    #conn variable = sql.connectFunction(path/filename.ext)
    conn = sql.connect(r"LeisureCenterManager by Flask\webflask\leisureCentre.db")  ### !!!! is r necessary!!
    # row_factory is used to manipulate/access the db
    conn.row_factory = sql.Row
    return conn

# set the routes for the index.html/home

@app.route("/") # 192.168.0.6/
@app.route("/index") # 192.168.0.6/index.html

def index():
    #returns the index page in the browser on load
    return render_template("index.html", title="Home")

# set the routes for the members.html

@app.route("/members")
def members():
    # read member data from the database
    memberConn = leisureCentreCon()
    cursor = memberConn.cursor()
    cursor.execute("SELECT * FROM members") # selecting everything in db and then  we will passit to fetchall()
    getMembers = cursor.fetchall()
    # returns the members page in the browser when the members text/link clicked on the menu
    return render_template("members.html", title = "Members", membersInDb = getMembers)

"Delete member by MemberID" # 192.168.0.9:23500/MemberID=21

@app.route("/<int:MemberID>/delete", methods=("POST",)) # we set up the route
def delete(MemberID):   # !!!! ask MemberID  ==== we are passing MemberID above
    memberConn = leisureCentreCon()
    cursor = memberConn.cursor()
    cursor.execute("DELETE FROM members WHERE MemberID =?", (MemberID,))   # !!!!ask , it is there? 
    memberConn.commit()
    memberConn.close()
    return redirect(url_for("members")) # redirect to the members page after delete

# now we need to get MemberID to pass it on above function to be able to do that we need another function  - because we cant delte before we get MemberID
# Create a function to get a specific member

def getMember(recordID):
    memberConn = leisureCentreCon()
    cursor = memberConn.cursor()
    #
    aMember = cursor.execute("SELECT* FROM members WHERE MemberID =?", (recordID,)).fetchone()
    memberConn.close()

    if aMember is None:
        abort(Response(f"No Record {aMember} was found in DB"))
    return aMember   # why dont we use else? 

"Update a Member"

@app.route("/<int:MemberID>/update", methods=("GET","POST"))
def update(MemberID):
    aMemberRecord = getMember(MemberID)
    if request.method == "POST":
        fname = request.form["Firstname"]
        lname = request.form["Lastname"]
        dob = request.form["DOB"]
        gender = request.form["Gender"]
        address = request.form["Address"]
        city = request.form["City"]
        tel = request.form["Telephone"]
        email = request.form["Email"]
        startDate = request.form["Startdate"]
        memberShip = request.form["Membership"]

        memberConn= leisureCentreCon()
        cursor = memberConn.cursor()
        cursor.execute("UPDATE members SET Firstname = ?, Lastname = ?, DOB = ?, Gender = ?, Address = ?, City = ?, Telephone = ?, Email = ?, Startdate = ?, Membership = ?" "WHERE MemberID = ?", (fname, lname, dob, gender, address, city, tel, email, startDate, memberShip, MemberID))
        memberConn.commit()
        memberConn.close()
        return redirect(url_for("members"))  # redirect to the members page
    return render_template("updateMember.html", title="Update Members", MemberRecord=aMemberRecord )

########################################

@app.route("/addMember.html", methods=["GET", "POST"])   # .html
def addMember(): # this is what we want to happen in case of adding members
    if request.method == "POST":

        fname = request.form["Firstname"]
        lname = request.form["Lastname"]
        dob = request.form["DOB"]
        gender = request.form["Gender"]
        address = request.form["Address"]
        city = request.form["City"]
        tel = request.form["Telephone"]
        email = request.form["Email"]
        startDate = request.form["Startdate"]
        memberShip = request.form["Membership"]

        memberConn = leisureCentreCon()
        cursor = memberConn.cursor()
        MemberID = cursor.lastrowid   ##### lower case or uppercase is fine?????

        cursor.execute("INSERT INTO members VALUES(?,?,?,?,?,?,?,?,?,?,?)", (MemberID, fname, lname, dob, gender, address, city, tel, email, startDate, memberShip))
        memberConn.commit()
        memberConn.close()
        return redirect(url_for("members")) # redirect back to the members page after adding a member
    
    return render_template("addMember.html", title="Add Member")


########################

# set the routes for the contact.html
@app.route("/contact")
def contact():

 # returns the contact page in the browser when the Contact text/link is clicked on the menu
    return render_template("contact.html", title="Contact")

# set the routes for the about.html

@app.route("/about")
def about():

 # returns the about page in the browser when the about text/link is clicked on the menu
    return render_template("about.html", title="About")

##########################
# you need closing route for every page with url so it will complete circuit becuase it is database application it is like pairs!!!! 

###################################



# invoke /call the main class

if __name__ =="__main__":
    app.run(debug=True, host="0.0.0.0", port=3500) # this port will serve this host local host