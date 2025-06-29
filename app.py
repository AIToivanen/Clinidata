from flask import Flask
from flask import render_template, request, session, redirect, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
import config
import sqlite3
import secrets
import re
import controller
import db

app= Flask(__name__)
app.secret_key= config.secret_key
try:
    user= session["username"]
except:
    user= "guest"

datePattern = r'^\d{4}-\d{2}-\d{2}$'

def requireLogin():
    if "userid" not in session:
        abort(403)

def checkCsrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():

    if "userid" not in session:
        patients= {}
        diagnoses= {}
        samples= {}
    else:
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

    try:
        passwordHashed= db.query("SELECT passwordHashed FROM users WHERE username = ?", (username,))[0][0]
    except:
        flash("Error: incorrect username or password!")
        return redirect("/login/form")
    
    if check_password_hash(passwordHashed, password):
  
        session["userid"]=   db.query("SELECT id FROM users WHERE username = ?", (username,))[0][0]
        session["username"]= username
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/")
    else:
        flash("Error: incorrect username or password!")
        return redirect("/login/form")
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["userid"]
    del session["csrf_token"]
    flash("Logged out successfully")
    return redirect("/")

@app.route("/create_user/form")
def create_user_form():
    return render_template("create_user_form.html", filled={})

@app.route("/search")
def searchPatients():

    requireLogin()

    query= request.args.get("query")
    results= controller.search(query)
    return render_template("search_results.html", query= query, results= results)

@app.route("/create_user", methods=["POST"])
def create_user():
    username= request.form["username"]
    password= request.form["password"]
    password2= request.form["password2"]
    filled= {"username": username,
             "password": password}
    
    if len(username)< 4 or len(username) > 40:
        flash("Error! Please enter a valid username (3-40 characters)")
        return render_template("create_user_form.html", filled= filled)
    
    if len(password)== 0 or len(password) > 100:
        flash("Error! Please enter a valid password (1-100 characters)")
        return render_template("create_user_form.html", filled= filled)
    

    
    if password != password2:
        flash("Error: the passwords don't match!")
        return render_template("create_user_form.html", filled= filled)

    try:
        passwordHashed= generate_password_hash(password)
        controller.addUser(username, passwordHashed)
        flash("User registered successfully!")
    except :
        flash("Error! Username is already taken")
        return render_template("create_user_form.html", filled= filled)
    return redirect("/login/form")
    
    
    
    

@app.route("/users/<int:userid>")
def showUser(userid):

    requireLogin()

    user = controller.getUsers(userid)
    patients= controller.getUserPatients(userid)
    diagnoses= controller.getUserDiagnoses(userid)
    samples= controller.getUserSamples(userid)
    comments= controller.getUserComments(userid)
    #print(str(patients))
    if not user:
        flash("Error: user not found")
    #    abort(404)
    return render_template("user_info.html", user=user, userPatients=patients, userDiagnoses= diagnoses, userSamples= samples, userComments= comments)


@app.route("/patients/add/form")
def addPatientForm():
    return render_template("new_patient_form.html", filled= {})

@app.route("/patients/add", methods= ["POST"])
def addPatient():

    requireLogin()
    checkCsrf()

    ssid= request.form["ssid"]
    firstName= request.form["firstName"]
    lastName= request.form["lastName"]
    dateOfBirth= request.form["dateOfBirth"]
    userId= session["userid"]

    filled= {"ssid":ssid, 
             "firstName": firstName,
             "lastName": lastName,
             "dateOfBirth": dateOfBirth}
    
    if len(ssid) != 11:
        flash("Error! Please enter a valid SSID (11 characters)")
        return render_template("new_patient_form.html", filled= filled)
    
    if len(firstName)< 1 or len(firstName) > 100:
        flash("Error! Please enter a valid first name (1-100 characters)")
        return render_template("new_patient_form.html", filled= filled)
    
    if len(lastName)< 1 or len(lastName) > 100:
        flash("Error! Please enter a valid last name (1-100 characters)")
        return render_template("new_patient_form.html", filled= filled)
    
    if not re.match(datePattern, dateOfBirth):
        flash("Error! Please use yyyy-mm-dd date format")
        return render_template("new_patient_form.html", filled= filled)
   

    try:
        patientId= controller.addPatient(ssid, firstName, lastName, dateOfBirth, userId)
    except :
        flash("Error! Patient could not be added to the database")
        return render_template("new_patient_form.html", filled= filled)
   
    return redirect("/patients/"+str(patientId))

@app.route("/patients")
def showPatients():

    requireLogin()
    
    patients= controller.getPatients()
    return render_template("patient_list.html", patients= patients)

@app.route("/patients/<int:patientId>")
def showPatient(patientId):

    requireLogin()

    patient= controller.getPatients(patientId)
    diagnoses= controller.getPatientDiagnoses(patientId)
    samples= controller.getPatientSamples(patientId)
    comments= controller.getPatientComments(patientId)
    if  len(patient)==0:
        flash("Error: patient not found")
        return redirect("/patients")
    #patient= patient[0]
    return render_template("patient_info.html", patients= patient, diagnoses= diagnoses, samples= samples, comments= comments)


@app.route("/patients/<int:patientId>/comment/form")
def commentPatientForm(patientId):

    requireLogin()

    patient= controller.getPatients(patientId)
    if  len(patient)==0:
        flash("Error: patient not found")
        return redirect("/patients")
    patient= patient[0]
    return render_template("new_comment_form.html", filled= {}, patient= patient)

@app.route("/patients/<int:patientId>/comment", methods= ["POST"] )
def commentPatient(patientId):

    requireLogin()
    checkCsrf()

    userid= session["userid"]
    comment= request.form["content"]

    patient= controller.getPatients(patientId)
    if  len(patient)==0:
        flash("Error: patient not found")
        return redirect("/patients")
    patient= patient[0]

    filled= {"content": comment}

    if len(comment)< 1 or len(comment) > 500:
        flash("Error! Please enter a valid comment (1-500 characters). Current length: "+str(len(comment)))
        return render_template("new_comment_form.html", filled= filled, patient= patient)
    commentId= controller.addComment(patientId, userid, comment)
    return redirect("/patients/"+str(patientId))

@app.route("/patients/<int:patientId>/edit", methods= ["GET", "POST"] )
def editPatient(patientId):

    requireLogin()
    

    patient= controller.getPatients(patientId)
    
    if  len(patient)==0:
        flash("Error: patient not found")
        return redirect("/patients")
    patient= patient[0]

    if request.method == "GET":
        return render_template("edit_patient_form.html", patient= patient)
    if request.method == "POST":
        checkCsrf()
        ssid= request.form["ssid"]
        firstName= request.form["firstName"]
        lastName= request.form["lastName"]
        dateOfBirth= request.form["dateOfBirth"]

        if not re.match(datePattern, dateOfBirth):
            flash("Error! Please use yyyy-mm-dd date format")
            return render_template("edit_patient_form.html", patient= patient)
        
        controller.updatePatient(ssid, firstName, lastName, dateOfBirth, patientId)
        return redirect("/patients/"+str(patientId))
        
@app.route("/patients/<int:patientId>/delete", methods= ["GET", "POST"] )
def deletePatient(patientId):

    requireLogin()
    

    patient= controller.getPatients(patientId)
    if request.method == "GET":
        return render_template("delete_patient_form.html", patient= patient)
    if request.method == "POST":
        checkCsrf()
        if "delete" in request.form:
            controller.deletePatient(patientId)
        return redirect("/patients")
    
@app.route("/diagnoses/add/form" )
def addDiagnosisForm():
    return render_template("new_diagnosis_form.html", filled= {})
    
@app.route("/diagnoses/add", methods= ["POST"] )
def addDiagnosis():

    requireLogin()
    checkCsrf()

    ssid= request.form["ssid"]
    icd11= request.form["icd11"]
    dateOfDiagnosis= request.form["dateOfDiagnosis"]
    userId= session["userid"]
    filled= {"ssid":ssid, 
             "icd11": icd11,
             "date": dateOfDiagnosis}
    
    if len(icd11)< 1 or len(icd11) > 20:
        flash("Error! Please enter a valid ICD11 code (1-20 characters)")
        return render_template("new_diagnosis_form.html", filled= filled)

    if not re.match(datePattern, dateOfDiagnosis):
        flash("Error! Please use yyyy-mm-dd date format")
        return render_template("new_diagnosis_form.html", filled= filled)
    try:
        diagnosisId= controller.addDiagnosis(ssid, icd11, dateOfDiagnosis, userId)
    except KeyError:
        flash("Error! The provided SSID matches no patient")
        return render_template("new_diagnosis_form.html", filled= filled)
    
    return redirect("/diagnoses/"+str(diagnosisId))
    
        
@app.route("/diagnoses/<int:diagnosisId>")
def showDiagnosis(diagnosisId):

    requireLogin()

    diagnoses= controller.getDiagnoses(diagnosisId)
    if len(diagnoses)== 0: 
        flash("Error! Diagnosis not found!")
        return redirect("/diagnoses")
    return render_template("diagnosis_list.html", diagnoses= diagnoses)

@app.route("/diagnoses")
def showDiagnoses():

    requireLogin()

    diagnoses= controller.getDiagnoses()
    return render_template("diagnosis_list.html", diagnoses= diagnoses)

@app.route("/diagnoses/<int:diagnosisId>/edit", methods= ["GET", "POST"] )
def editDiagnosis(diagnosisId):

    requireLogin()
    #checkCsrf()

    diagnosis= controller.getDiagnoses(diagnosisId)

    if len(diagnosis)== 0: 
        flash("Error! Diagnosis not found!")
        return redirect("/diagnoses")
    diagnosis= diagnosis[0]

    if request.method == "GET":
        return render_template("edit_diagnosis_form.html", diagnosis= diagnosis)
    if request.method == "POST":
        checkCsrf()
        patientId= request.form["patientId"]
        icd11= request.form["icd11"]
        dateOfDiagnosis= request.form["dateOfDiagnosis"] 
        if not re.match(datePattern, dateOfDiagnosis):
            flash("Error! Please use yyyy-mm-dd date format")
            return render_template("edit_diagnosis_form.html", diagnosis= diagnosis)
        
        controller.updateDiagnosis(patientId, icd11, dateOfDiagnosis, diagnosisId)
        return redirect("/diagnoses/"+str(diagnosisId))
    
@app.route("/diagnoses/<int:diagnosisId>/delete", methods= ["GET", "POST"] )
def deleteDiagnosis(diagnosisId):

    requireLogin()
    

    diagnosis= controller.getDiagnoses(diagnosisId)
    if len(diagnosis)== 0: 
        flash("Error! Diagnosis not found!")
        return redirect("/diagnoses")
    
    if request.method == "GET":
        return render_template("delete_diagnosis_form.html", diagnosis= diagnosis)
    if request.method == "POST":
        checkCsrf()

        if "delete" in request.form:
            controller.deleteDiagnosis(diagnosisId)
        return redirect("/diagnoses")
    
@app.route("/samples/add/form" )
def addSampleForm():
    return render_template("new_sample_form.html", filled= {})
    
@app.route("/samples/add", methods= ["POST"] )
def addSample():

    requireLogin()
    checkCsrf()

    ssid= request.form["ssid"]
    sampleType= request.form["sampleType"]
    sampleMeasurement= request.form["sampleMeasurement"]
    sampleValue= request.form["sampleValue"]
    sampleDate= request.form["sampleDate"]
    userId= session["userid"]

    filled= {"ssid":ssid, 
             "sampleType": sampleType,
             "sampleMeasurement": sampleMeasurement,
             "sampleValue": sampleValue,
             "sampleDate": sampleDate}
    
    if len(sampleType)< 1 or len(sampleType) > 20:
        flash("Error! Please enter a valid sample type from the list")
        return render_template("new_sample_form.html", filled= filled)
    
    if len(sampleMeasurement)< 1 or len(sampleMeasurement) > 100:
        flash("Error! Please enter a valid sample measurement (1-100 characters)")
        return render_template("new_sample_form.html", filled= filled)
    
    if len(sampleValue)< 1 or len(sampleValue) > 100:
        flash("Error! Please enter a valid sample value (1-100 characters)")
        return render_template("new_sample_form.html", filled= filled)
    
    if not re.match(datePattern, sampleDate):
            flash("Error! Please use yyyy-mm-dd date format")
            return render_template("new_sample_form.html", filled= filled)

    try:
        sampleId= controller.addSample(ssid, sampleType, sampleMeasurement, sampleValue, sampleDate, userId)
    except KeyError:
        flash("Error! The provided SSID matches no patient")
        return render_template("new_sample_form.html", filled= filled)
    
    
    return redirect("/samples/"+str(sampleId))
    
         
@app.route("/samples/<int:sampleId>")
def showSample(sampleId):

    requireLogin()

    samples= controller.getSamples(sampleId)
    if len(samples)== 0: 
        flash("Error! Sample not found!")
        return redirect("/samples")
    
    return render_template("sample_list.html", samples= samples)

@app.route("/samples")
def showSamples():

    requireLogin()

    samples= controller.getSamples()
    return render_template("sample_list.html", samples= samples)

@app.route("/samples/<int:sampleId>/edit", methods= ["GET", "POST"] )
def editSample(sampleId):

    requireLogin()
    

    sample= controller.getSamples(sampleId)
    if len(sample)== 0: 
        flash("Error! Sample not found!")
        return redirect("/samples")
    sample= sample[0]
    if request.method == "GET":
        return render_template("edit_sample_form.html", sample= sample)
    if request.method == "POST":
        checkCsrf()
        patientId= request.form["patientId"]
        sampleType= request.form["sampleType"]
        sampleMeasurement= request.form["sampleMeasurement"]
        sampleValue= request.form["sampleValue"]
        sampleDate= request.form["sampleDate"]

        if not re.match(datePattern, sampleDate):
            flash("Error! Please use yyyy-mm-dd date format")
            return render_template("edit_sample_form.html", sample= sample)
        
        controller.updateSample(patientId, sampleType, sampleMeasurement, sampleValue, sampleDate, sampleId)
        return redirect("/samples/"+str(sampleId))
    
@app.route("/samples/<int:sampleId>/delete", methods= ["GET", "POST"] )
def deleteSample(sampleId):

    requireLogin()
    

    sample= controller.getSamples(sampleId)
    if len(sample)== 0: 
        flash("Error! Sample not found!")
        return redirect("/samples")
    sample= sample[0]
    if request.method == "GET":
        return render_template("delete_sample_form.html", sample= sample)
    if request.method == "POST":
        checkCsrf()
        if "delete" in request.form:
            controller.deleteSample(sampleId)
        return redirect("/samples")
    