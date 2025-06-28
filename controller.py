import db
import sqlite3

def search(query):
    sql= """SELECT * FROM patients 
    WHERE patients.ssid LIKE ? OR
    patients.firstName LIKE ? OR
    patients.lastName LIKE ? OR 
    patients.dateOfBirth LIKE ?
    ORDER BY patients.lastName"""
    return db.query(sql, ["%"+ query+ "%"]*4)
    
def addPatient(ssid, firstName, lastName, dateOfBirth, usersId):
    sql= """INSERT INTO patients (ssid, firstName, lastName, dateOfBirth, usersId) 
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [ssid, firstName, lastName, dateOfBirth, usersId])
    patientsId= db.lastInsertId()
    return patientsId

def updatePatient(ssid, firstName, lastName, dateOfBirth, id):
    sql= """UPDATE patients SET (id, ssid, firstName, lastName, dateOfBirth) 
    = (?, ?, ?, ?, ?) WHERE id = ?"""
    db.execute(sql, [id, ssid, firstName, lastName, dateOfBirth, id])
    
    

def deletePatient( id):
    sql= """DELETE FROM diagnoses WHERE patientsId = ?"""
    db.execute(sql, [id])

    sql= """DELETE FROM samples WHERE patientsId = ?"""
    db.execute(sql, [id])
    
    sql= """DELETE FROM comments WHERE patientsId = ?"""
    db.execute(sql, [id])

    sql= """DELETE FROM patients WHERE id = ?"""
    db.execute(sql, [id])
    
def getPatientId(ssid):
    try:
        query= "SELECT id FROM patients WHERE ssid = ?"
        return db.query(query, [ssid])#[0][0]
    except:
        raise KeyError("Patient "+ssid+" not found")

def addSample(ssid, sampleType, sampleMeasurement, sampleValue, sampleDate, usersId):

    patientsId= getPatientId(ssid)
        
    sql= """INSERT INTO samples (patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, usersId) 
    VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, usersId])
    id= db.lastInsertId()
    return id

def updateSample(patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, id):
    sql= """UPDATE samples SET (patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate) 
    VALUES (?, ?, ?, ?, ?) WHERE id = ?"""
    db.execute(sql, [patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, id])
    
def deleteSample( id):
    sql= """DELETE FROM samples WHERE id = ?"""
    db.execute(sql, [id])

def addDiagnosis(ssid, icd11, date, usersId ):
    patientsId= getPatientId(ssid)
    sql= """INSERT INTO diagnoses (patientsId, icd11, diagnosisDate, usersId) 
    VALUES (?, ?, ?, ?)"""
    db.execute(sql, [patientsId, icd11, date , usersId])
    id= db.lastInsertId()
    return id

def updateDiagnosis(patientsId, icd11, diagnosisDate, id):
    sql= """UPDATE diagnoses SET (patientsId, icd11, diagnosisDate) 
    VALUES (?, ?, ?) WHERE id = ?"""
    db.execute(sql, [patientsId, icd11, diagnosisDate, id])
    
def deleteDiagnosis( id):
    sql= """DELETE FROM diagnoses WHERE id = ?"""
    db.execute(sql, [id])

def addUser(username, passwordHashed, ):
    try:
        query= "INSERT INTO users (username, passwordHashed) VALUES (?, ?)"
        db.execute(query, [username, passwordHashed])
    except sqlite3.IntegrityError:
        return "Error: username is already taken!"
    
def getUsers(usersId=None):
    if (usersId is not None):
        
        query= "SELECT * FROM users WHERE id = ?"
        return db.query(query, [usersId])
        
    else:
        query= "SELECT * FROM users"
        return db.query(query)


def deleteUser( id):
    sql= """DELETE FROM patients WHERE id = ?"""
    db.execute(sql, [id])

def getPatients(patientId=None):
    if (patientId is not None):
        
        query= "SELECT * FROM patients WHERE id = ?"
        return db.query(query, [patientId])
        
    else:
        query= "SELECT * FROM patients"
        return db.query(query)
    
def getUserPatients(usersId):
        
    query= "SELECT * FROM patients WHERE usersId = ?"
    return db.query(query, [usersId])
    
def getDiagnoses(diagnosisId=None):
    if (diagnosisId is not None):
        
        query= "SELECT * FROM diagnoses WHERE id = ?"
        return db.query(query, [diagnosisId])
        
    else:
        query= "SELECT * FROM diagnoses"
        return db.query(query)
    
def getUserDiagnoses(usersId):
        
    query= "SELECT * FROM diagnoses WHERE usersId = ?"
    return db.query(query, [usersId])

def getPatientDiagnoses(patientId=None):
    if (patientId is not None):
        
        query= "SELECT * FROM diagnoses WHERE patientsId = ?"
        return db.query(query, [patientId])
        
    else:
        query= "SELECT * FROM diagnoses"
        return db.query(query)
    
def getSamples(sampleId=None):
    if (sampleId is not None):
        
        query= "SELECT * FROM samples where id = ?"
        return db.query(query, [sampleId])
        
    else:
        query= "SELECT * FROM samples"
        return db.query(query)
    
def getUserSamples(usersId):
        
    query= "SELECT * FROM samples WHERE usersId = ?"
    return db.query(query, [usersId])
    
def getPatientSamples(patientId=None):
    if (patientId is not None):
        
        query= "SELECT * FROM samples WHERE patientsId = ?"
        return db.query(query, [patientId])
        
    else:
        query= "SELECT * FROM samples"
        return db.query(query)
    

def addComment(patientsId, usersId, content ):
    
    sql= """INSERT INTO comments (patientsId, usersId, content, commentDate) 
    VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [patientsId, usersId, content])
    id= db.lastInsertId()
    return id

def getUserComments(usersId):
        
    query= "SELECT * FROM comments WHERE usersId = ?"
    return db.query(query, [usersId])

def getPatientComments(patientId=None):
    if (patientId is not None):
        
        query= "SELECT * FROM comments WHERE patientsId = ?"
        return db.query(query, [patientId])
        
    else:
        query= "SELECT * FROM comments"
        return db.query(query)
