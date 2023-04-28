import sqlite3
from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index1")
def index1():
    return render_template("index1.html")


@app.route("/places")
def places():
    return render_template("places.html")


@app.route("/FactsaboutTampa")
def FactsaboutTampa():
    return render_template("FactsaboutTampa.html")


@app.route("/Best")
def Best():
    return render_template("Best.html")


@app.route("/AboutUs")
def AboutUs():
    return render_template("AboutUs.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/form1")
def form1():
    return render_template("form1.html")


@app.route("/db")
def testg_db():
    conn = sqlite3.connect("database.db")
    print("Opened database successfully", flush=True)

    conn.execute("DROP TABLE IF EXISTS newuser")
    conn.execute("DROP TABLE IF EXISTS plan")
    conn.execute("DROP TABLE IF EXISTS book")
    conn.commit()
    conn.execute("create table newuser(fullname TEXT, email TEXT, password TEXT)")
    conn.execute(
        "create table plan(destination TEXT, name TEXT, email TEXT, phone TEXT, date TEXT, gender TEXT)"
    )
    conn.execute("create table book(name TEXT, email TEXT, phone TEXT, date TEXT)")

    print("Tables created successfully", flush=True)
    conn.close()
    return "Tables Created Successfully"


@app.route("/addrec", methods=["POST", "GET"])
def addrec():
    if request.method == "POST":
        try:
            fullname = request.form["name"]
            email = request.form["mail"]
            password = request.form["pass"]

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO newuser(fullname,email,password)VALUES (?,?,?)",
                    (fullname, email, password),
                )
                con.commit()
                msg = "Signup successfully added"
        except:
            con.rollback()
            msg = "error in signup"
        finally:
            con.close()
            return render_template("result.html",msg = msg)


@app.route("/sign", methods=["POST", "GET"])
def sign():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            query = (
                "select email,password from newuser where email = '"
                + email
                + "' and password = '"
                + password
                + "'"
            )
            cur.execute(query)
            row = cur.fetchone()
            if row is not None:
                return render_template("index1.html")
            else:
                error = "Invalid email or password"
                return render_template("login.html", error=error)

@app.route("/addplan", methods=["POST", "GET"])
def addplan():
    if request.method == "POST":
        try:
            dstn = request.form["places"]
            nm = request.form["name"]
            eml = request.form["email"]
            phn = request.form["phone"]
            dt = request.form["date"]
            gdr = request.form["gender"]
            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO plan(destination,name,email,phone,date,gender)VALUES (?,?,?,?,?,?)",
                    (dstn,nm,eml, phn, dt,gdr),
                )
                con.commit()
                msg = "Reservation successfully done"
        except:
            con.rollback()
            msg = "error in reservation"
        finally:
            con.close()
            return render_template("result2.html",msg=msg)


@app.route("/addbook", methods=["POST", "GET"])
def addbook():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            date = request.form["date"]

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO book(name,email,phone,date)VALUES (?,?,?,?)",
                    (name, email, phone, date),
                )
                con.commit()
                msg = "Booking successfully done"
        except:
            con.rollback()
            msg = "error in booking"
        finally:
            con.close()
            return render_template("result3.html",msg=msg)

@app.route('/users')
def users():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM newuser")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("users.html",rows=rows)

@app.route('/plans')
def plans():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM plan")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("plans.html",rows=rows)

@app.route('/bookings')
def bookings():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM book")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("bookings.html",rows=rows)
