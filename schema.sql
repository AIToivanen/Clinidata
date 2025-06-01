
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    passwordHashed TEXT
);

CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    ssid TEXT UNIQUE,
    dateOfBirth TEXT

);

CREATE TABLE diagnoses (
    id INTEGER PRIMARY KEY,
    patientsId INTEGER,
    icd11 TEXT,
    diagnosisDate TEXT, 
    FOREIGN KEY (patientsId) REFERENCES patients (id)
);

CREATE TABLE samples (
    id INTEGER PRIMARY KEY,
    patientsId INTEGER,
    sampleType TEXT,
    sampleMeasurement TEXT,
    sampleValue FLOAT,
    sampleDate TEXT,
    FOREIGN KEY (patientsId) REFERENCES patients (id)
);


