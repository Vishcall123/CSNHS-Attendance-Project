import random
from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import datetime

db = sqlite3.connect("sheet.db", check_same_thread=False)
c = db.cursor()

c.execute(
  """CREATE TABLE IF NOT EXISTS sheet (time TEXT, name TEXT, date TEXT, action TEXT, reason TEXT ) """
)
db.commit()

app = Flask(
  __name__,
  template_folder='templates',  # Name of html file folder  
)


@app.route('/')
def base_page():
  return render_template("index.html")


@app.route('/student', methods=["POST", "GET"])
def student_page():
  if request.method == "POST":
    print(request.form)
    date = request.form["month"]
    name = request.form["name"]
    action = request.form["action"]
    try:
      reason=request.form["reason"]
    except:
      reason = request.form["reason2"]
    c.execute("INSERT INTO sheet VALUES (?, ?, ?, ?, ?)",
              (datetime.datetime.now().strftime("%H:%M:%S"), name,
               date, action, reason))
    db.commit()
    return redirect(url_for("base_page"))
  if request.method == "GET":
    return render_template("student.html")


@app.route('/admin', methods=["POST", "GET"])
def admin_page():
  #Prototype model has a singular admin login: USER: Admin PW: 12345
  if request.method == "POST":
    username = request.form["Username"]
    password = request.form["Password"]
    if username == "Admin" and password == "12345":
      return redirect(url_for("admin_direct"))
    else:
      return render_template("admin.html", result="Incorrect Password!")
  if request.method == "GET":
    return render_template("admin.html")


@app.route('/adminportal', methods=["POST", "GET"])
def admin_direct():
  if request.method == "GET":
    return render_template("admindirect.html")
  elif request.method == "POST":
    if "actionradio" in request.form:
      action = request.form["actionradio"]
    else:
      action = ""
    name = request.form["Name"]
    date = request.form["Date"]
    print(request.form)
    print(datetime.datetime.now().strftime("%Y-%m-%d"))
    QUERY = f"SELECT * FROM sheet WHERE (name = '{name}' OR '{name}' = '') and (date =   '{date}' OR '{date}' = '') and (action = '{action}' OR '{action}' = '')"
    print(QUERY)
    c.execute(QUERY)
    x = c.fetchall()
    print(x)
    results = []
    for i in x:
      results.append(i)

    return render_template("admindirect.html", ITEMS=results)


@app.route('/templates/<filename>')
def get_image(filename):
  return send_file("templates/" + filename, mimetype='image/gif')


if __name__ == "__main__":  # Makes sure this is the main process
  app.run()