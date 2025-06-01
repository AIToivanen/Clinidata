import db
import sqlite3

def addPatient(ssid, firstName, lastName, dateOfBirth):
    sql= """INSERT INTO patients (ssid, firstName, lastName, dateOfBirth) 
    VALUES (?, ?, ?, ?)"""
    db.execute(sql, [ssid, firstName, lastName, dateOfBirth])
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
    
    sql= """DELETE FROM patients WHERE id = ?"""
    db.execute(sql, [id])
    
def getPatientId(ssid):
    try:
        query= "SELECT id FROM patients WHERE ssid = ?"
        return db.query(query, [ssid])[0][0]
    except:
        raise KeyError("Patient "+ssid+" not found")

def addSample(ssid, sampleType, sampleMeasurement, sampleValue, sampleDate):

    patientsId= getPatientId(ssid)
        
    sql= """INSERT INTO samples (patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate) 
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate])
    id= db.lastInsertId()
    return id

def updateSample(patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, id):
    sql= """UPDATE samples SET (patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate) 
    VALUES (?, ?, ?, ?, ?) WHERE id = ?"""
    db.execute(sql, [patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, id])
    
def deleteSample( id):
    sql= """DELETE FROM samples WHERE id = ?"""
    db.execute(sql, [id])

def addDiagnosis(ssid, icd11, date ):
    patientsId= getPatientId(ssid)
    sql= """INSERT INTO diagnoses (patientsId, icd11, diagnosisDate) 
    VALUES (?, ?, ?)"""
    db.execute(sql, [patientsId, icd11, date ])
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

    

def deleteUser( id):
    sql= """DELETE FROM patients WHERE id = ?"""
    db.execute(sql, [id])

def getPatients(patientId=None):
    if (patientId is not None):
        
        query= "SELECT * FROM patients WHERE id = ?"
        return db.query(query, [patientId])[0]
        
    else:
        query= "SELECT * FROM patients"
        return db.query(query)
    
def getDiagnoses(diagnosisId=None):
    if (diagnosisId is not None):
        
        query= "SELECT * FROM diagnoses WHERE id = ?"
        return db.query(query, [diagnosisId])[0]
        
    else:
        query= "SELECT * FROM diagnoses"
        return db.query(query)

def getSamples(sampleId=None):
    if (sampleId is not None):
        
        query= "SELECT * FROM samples where id = ?"
        return db.query(query, [sampleId])[0]
        
    else:
        query= "SELECT * FROM samples"
        return db.query(query)