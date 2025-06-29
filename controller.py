import db
import sqlite3


def search(query):
    sql= """SELECT id, firstName, lastName, ssid, dateOfBirth, usersId FROM patients 
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
    query= "SELECT id FROM patients WHERE ssid = ?"
    ids= db.query(query, [ssid])#[0][0]
    if len(ids)== 0:
        raise KeyError
    return ids[0][0]
        
    
    

def addSample(ssid, sampleType, sampleMeasurement, sampleValue, sampleDate, usersId):

    patientsId= getPatientId(ssid)
        
    sql= """INSERT INTO samples (patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, usersId) 
    VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, usersId])
    id= db.lastInsertId()
    return id

def updateSample(patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate, id):
    sql= """UPDATE samples SET (patientsId, sampleType, sampleMeasurement, sampleValue, sampleDate) 
    = (?, ?, ?, ?, ?) WHERE id = ?"""
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
    = (?, ?, ?) WHERE id = ?"""
    db.execute(sql, [patientsId, icd11, diagnosisDate, id])
    
def deleteDiagnosis( id):
    sql= """DELETE FROM diagnoses WHERE id = ?"""
    db.execute(sql, [id])

def addUser(username, passwordHashed, ):
    
    query= "INSERT INTO users (username, passwordHashed) VALUES (?, ?)"
    db.execute(query, [username, passwordHashed])
    
    
def getUsers(usersId=None):
    if (usersId is not None):
        
        query= "SELECT id, username, passwordHashed FROM users WHERE id = ?"
        return db.query(query, [usersId])
        
    else:
        query= "SELECT id, username, passwordHashed FROM users"
        return db.query(query)


def deleteUser( id):
    sql= """DELETE FROM patients WHERE id = ?"""
    db.execute(sql, [id])

def getPatients(patientId=None):
    if (patientId is not None):
        
        query= """SELECT patients.id, patients.firstName, patients.lastName, patients.ssid, patients.dateOfBirth, patients.usersId, users.username
                FROM patients 
                JOIN users ON patients.usersId = users.id
                WHERE patients.id = ?"""
        return db.query(query, [patientId])
        
    else:
        query= """SELECT patients.id, patients.firstName, patients.lastName, patients.ssid, patients.dateOfBirth, patients.usersId, users.username
                FROM patients 
                JOIN users ON patients.usersId = users.id
                """
        return db.query(query)
    
def getUserPatients(usersId):
        
    query= "SELECT id, firstName, lastName, ssid, dateOfBirth, usersId FROM patients WHERE usersId = ?"
    return db.query(query, [usersId])
    
def getDiagnoses(diagnosisId=None):
    if (diagnosisId is not None):
        
        query= """SELECT diagnoses.id, diagnoses.patientsId, diagnoses.icd11, diagnoses.diagnosisDate, diagnoses.usersId, users.username
                FROM diagnoses 
                JOIN users ON diagnoses.usersId = users.id
                WHERE diagnoses.id = ?"""
        return db.query(query, [diagnosisId])
        
    else:
        query= """SELECT diagnoses.id, diagnoses.patientsId, diagnoses.icd11, diagnoses.diagnosisDate, diagnoses.usersId,  users.username
                FROM diagnoses 
                JOIN users ON diagnoses.usersId = users.id
                """ 
        return db.query(query)
    
def getUserDiagnoses(usersId):
        
    query= "SELECT id, patientsId, icd11, diagnosisDate, usersId FROM diagnoses WHERE usersId = ?"
    return db.query(query, [usersId])

def getPatientDiagnoses(patientId=None):
    if (patientId is not None):
        
        query= """SELECT diagnoses.id, diagnoses.patientsId, diagnoses.icd11, diagnoses.diagnosisDate, diagnoses.usersId,  users.username
                FROM diagnoses 
                JOIN users ON diagnoses.usersId = users.id
                WHERE diagnoses.patientsId = ?"""
        return db.query(query, [patientId])
        
    else:
        query= "SELECT id, patientsId, icd11, diagnosisDate, usersId FROM diagnoses"
        return db.query(query)
    
def getSamples(sampleId=None):
    if (sampleId is not None):
        
        query= """SELECT samples.id, samples.patientsId, samples.sampleType, samples.sampleMeasurement, samples.sampleValue, 
                samples.sampleDate, samples.usersId, users.username
                FROM samples
                JOIN users ON samples.usersId = users.id
                WHERE samples.id = ?"""
        return db.query(query, [sampleId])
        
    else:
        query= """SELECT samples.id, samples.patientsId, samples.sampleType, samples.sampleMeasurement, samples.sampleValue, 
                samples.sampleDate, samples.usersId, users.username
                FROM samples
                JOIN users ON samples.usersId = users.id"""
        return db.query(query)
    
def getUserSamples(usersId):
        
    query= """SELECT samples.id, samples.patientsId, samples.sampleType, samples.sampleMeasurement, samples.sampleValue, 
                samples.sampleDate, samples.usersId, users.username
                FROM samples
                JOIN users ON samples.usersId = users.id
                WHERE samples.usersId = ?"""
    return db.query(query, [usersId])
    
def getPatientSamples(patientId=None):
    if (patientId is not None):
        
        query= """SELECT samples.id, samples.patientsId, samples.sampleType, samples.sampleMeasurement, samples.sampleValue, 
                samples.sampleDate, samples.usersId, users.username
                FROM samples
                JOIN users ON samples.usersId = users.id
                WHERE samples.patientsId = ?"""
        return db.query(query, [patientId])
        
    else:
        query= """SELECT samples.id, samples.patientsId, samples.sampleType, samples.sampleMeasurement, samples.sampleValue, 
                samples.sampleDate, samples.usersId, users.username
                FROM samples
                JOIN users ON samples.usersId = users.id
                """
        return db.query(query)
    

def addComment(patientsId, usersId, content ):
    
    sql= """INSERT INTO comments (patientsId, usersId, content, commentDate) 
    VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [patientsId, usersId, content])
    id= db.lastInsertId()
    return id

def getUserComments(usersId):
        
    query= """SELECT comments.id, comments.usersId, comments.patientsId, comments.content, comments.commentDate, users.username 
    FROM comments 
    JOIN users ON comments.usersId = users.id
    WHERE comments.usersId = ?"""
    return db.query(query, [usersId])

def getPatientComments(patientId=None):
    if (patientId is not None):
        
        query= """SELECT comments.id, comments.usersId, comments.patientsId, comments.content, comments.commentDate, users.username 
        FROM comments 
        JOIN users ON comments.usersId = users.id
        WHERE comments.patientsId = ?"""
        return db.query(query, [patientId])
        
    else:
        query= "SELECT id, usersId, patientsId, content, commentDate FROM comments"
        return db.query(query)
