
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
    dateOfBirth TEXT,
    usersId INTEGER,
    FOREIGN KEY (usersId) REFERENCES users (id)

);

CREATE TABLE diagnoses (
    id INTEGER PRIMARY KEY,
    patientsId INTEGER,
    icd11 TEXT,
    diagnosisDate TEXT, 
    usersId INTEGER,
    FOREIGN KEY (patientsId) REFERENCES patients (id),
    FOREIGN KEY (usersId) REFERENCES users (id)
);

CREATE TABLE samples (
    id INTEGER PRIMARY KEY,
    patientsId INTEGER,
    sampleType TEXT,
    sampleMeasurement TEXT,
    sampleValue FLOAT,
    sampleDate TEXT,
    usersId INTEGER,
    FOREIGN KEY (patientsId) REFERENCES patients (id),
    FOREIGN KEY (usersId) REFERENCES users (id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    usersId INTEGER,
    patientsId INTEGER,
    content TEXT,
    commentDate TEXT,
    FOREIGN KEY (usersId) REFERENCES users (id),
    FOREIGN KEY (patientsId) REFERENCES patients (id)
)
