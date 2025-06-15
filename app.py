from flask import Flask
from flask import render_template, request, session, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
import config
import sqlite3
import controller
import db

app= Flask(__name__)
app.secret_key= config.secret_key
try:
    user= session["username"]
except:
    user= "guest"

def requireLogin():
    if "userid" not in session:
        abort(403)

@app.route("/")
def index():
    patients= controller.getPatients()
    diagnoses= controller.getDiagnoses()
    samples= controller.getSamples()

    return render_template("landing.html", user= user, patients= patients, diagnoses= diagnoses, samples= samples)

@app.route("/login/form")
def loginForm():
    return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():

    username= request.form["username"]
    password= request.form["password"]

    passwordHashed= db.query("SELECT passwordHashed FROM users WHERE username = ?", (username,))[0][0]
    if check_password_hash(passwordHashed, password):
  
        session["userid"]=   db.query("SELECT id FROM users WHERE username = ?", (username,))[0][0]
        session["username"]= username
        return redirect("/")
    else:
        "Error: incorrect username or password!"
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["userid"]
    return redirect("/")

@app.route("/create_user/form")
def create_user_form():
    return render_template("create_user_form.html")

@app.route("/search")
def searchPatients():
    query= request.args.get("query")
    results= controller.search(query)
    return render_template("search_results.html", query= query, results= results)

@app.route("/create_user", methods=["POST"])
def create_user():
    username= request.form["username"]
    password= request.form["password"]
    password2= request.form["password2"]
    if password != password2:
        return "Error: the passwords don't match!"
    
    passwordHashed= generate_password_hash(password)
    controller.addUser(username, passwordHashed)
    return redirect("/login/form")

@app.route("/users/<int:userid>")
def showUser(userid):
    user = controller.getUsers(userid)
    patients= controller.getUserPatients(userid)
    diagnoses= controller.getUserDiagnoses(userid)
    samples= controller.getUserSamples(userid)
    comments= controller.getUserComments(userid)
    print(str(patients))
    #if not user:
    #    abort(404)
    return render_template("user_info.html", user=user, userPatients=patients, userDiagnoses= diagnoses, userSamples= samples, userComments= comments)


@app.route("/patients/add/form")
def addPatientForm():
    return render_template("new_patient_form.html")

@app.route("/patients/add", methods= ["POST"])
def addPatient():
    ssid= request.form["ssid"]
    firstName= request.form["firstName"]
    lastName= request.form["lastName"]
    dateOfBirth= request.form["dateOfBirth"]
    userId= session["userid"]
    patientId= controller.addPatient(ssid, firstName, lastName, dateOfBirth, userId)
    return redirect("/patients/"+str(patientId))

@app.route("/patients")
def showPatients():
    patients= controller.getPatients()
    return render_template("patient_list.html", patients= patients)

@app.route("/patients/<int:patientId>")
def showPatient(patientId):
    patient= (controller.getPatients(patientId),)
    diagnoses= controller.getPatientDiagnoses(patientId)
    samples= controller.getPatientSamples(patientId)
    comments= controller.getPatientComments(patientId)
    return render_template("patient_info.html", patients= patient, diagnoses= diagnoses, samples= samples, comments= comments)


@app.route("/patients/<int:patientId>/comment/form")
def commentPatientForm(patientId):
    patient= controller.getPatients(patientId)
    return render_template("new_comment_form.html", patient= patient)

@app.route("/patients/<int:patientId>/comment", methods= ["POST"] )
def commentPatient(patientId):
    userid= session["userid"]
    comment= request.form["content"]
    commentId= controller.addComment(patientId, userid, comment)
    return redirect("/patients/"+str(patientId))

@app.route("/patients/<int:patientId>/edit", methods= ["GET", "POST"] )
def editPatient(patientId):
    patient= controller.getPatients(patientId)
    if request.method == "GET":
        return render_template("edit_patient_form.html", patient= patient)
    if request.method == "POST":
        ssid= request.form["ssid"]
        firstName= request.form["firstName"]
        lastName= request.form["lastName"]
        dateOfBirth= request.form["dateOfBirth"]
        controller.updatePatient(ssid, firstName, lastName, dateOfBirth, patientId)
        return redirect("/patients/"+str(patientId))
        
@app.route("/patients/<int:patientId>/delete", methods= ["GET", "POST"] )
def deletePatient(patientId):
    patient= controller.getPatients(patientId)
    if request.method == "GET":
        return render_template("delete_patient_form.html", patient= patient)
    if request.method == "POST":
        if "delete" in request.form:
            controller.deletePatient(patientId)
        return redirect("/patients")
    
@app.route("/diagnoses/add/form" )
def addDiagnosisForm():
    return render_template("new_diagnosis_form.html")
    
@app.route("/diagnoses/add", methods= ["POST"] )
def addDiagnosis():
    ssid= request.form["ssid"]
    icd11= request.form["icd11"]
    dateOfDiagnosis= request.form["dateOfDiagnosis"]
    userId= session["userid"]
    diagnosisId= controller.addDiagnosis(ssid, icd11, dateOfDiagnosis, userId)
    return redirect("/diagnoses/"+str(diagnosisId))
    
        
@app.route("/diagnoses/<int:diagnosisId>")
def showDiagnosis(diagnosisId):
    diagnoses= controller.getDiagnoses(diagnosisId)
    return render_template("diagnosis_list.html", diagnoses= diagnoses)

@app.route("/diagnoses")
def showDiagnoses():
    diagnoses= controller.getDiagnoses()
    return render_template("diagnosis_list.html", diagnoses= diagnoses)

@app.route("/diagnoses/<int:diagnosisId>/edit", methods= ["GET", "POST"] )
def editDiagnosis(diagnosisId):
    diagnosis= controller.getDiagnoses(diagnosisId)

    #if diagnosis
    
    if request.method == "GET":
        return render_template("edit_diagnosis_form.html", diagnosis= diagnosis)
    if request.method == "POST":
        patientId= request.form["patientId"]
        icd11= request.form["icd11"]
        dateOfDiagnosis= request.form["dateOfDiagnosis"]
        controller.updateDiagnosis(patientId, icd11, dateOfDiagnosis, diagnosisId)
        return redirect("/diagnoses/"+str(diagnosisId))
    
@app.route("/diagnoses/<int:diagnosisId>/delete", methods= ["GET", "POST"] )
def deleteDiagnosis(diagnosisId):
    diagnosis= controller.getDiagnoses(diagnosisId)
    if request.method == "GET":
        return render_template("delete_diagnosis_form.html", diagnosis= diagnosis)
    if request.method == "POST":
        if "delete" in request.form:
            controller.deleteDiagnosis(diagnosisId)
        return redirect("/diagnoses")
    
@app.route("/samples/add/form" )
def addSampleForm():
    return render_template("new_sample_form.html")
    
@app.route("/samples/add", methods= ["POST"] )
def addSample():
    ssid= request.form["ssid"]
    sampleType= request.form["sampleType"]
    sampleMeasurement= request.form["sampleMeasurement"]
    sampleValue= request.form["sampleValue"]
    sampleDate= request.form["sampleDate"]
    userId= session["userid"]
    sampleId= controller.addSample(ssid, sampleType, sampleMeasurement, sampleValue, sampleDate, userId)
    return redirect("/samples/"+str(sampleId))
    
         
@app.route("/samples/<int:sampleId>")
def showSample(sampleId):
    samples= controller.getSamples(sampleId)
    return render_template("sample_list.html", samples= samples)

@app.route("/samples")
def showSamples():
    samples= controller.getSamples()
    return render_template("sample_list.html", samples= samples)

@app.route("/samples/<int:sampleId>/edit", methods= ["GET", "POST"] )
def editSample(sampleId):
    sample= controller.getSamples(sampleId)
    if request.method == "GET":
        return render_template("edit_sample_form.html", sample= sample)
    if request.method == "POST":
        patientId= request.form["patientId"]
        sampleType= request.form["sampleType"]
        sampleMeasurement= request.form["sampleMeasurement"]
        sampleValue= request.form["sampleValue"]
        sampleDate= request.form["sampleDate"]
        controller.updateDiagnosis(patientId, sampleType, sampleMeasurement, sampleValue, sampleDate, sampleId)
        return redirect("/samples/"+str(sampleId))
    
@app.route("/samples/<int:sampleId>/delete", methods= ["GET", "POST"] )
def deleteSample(sampleId):
    sample= controller.getDiagnoses(sampleId)
    if request.method == "GET":
        return render_template("delete_sample_form.html", sample= sample)
    if request.method == "POST":
        if "delete" in request.form:
            controller.deleteSample(sampleId)
        return redirect("/samples")
    