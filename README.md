# Clinidata - a clinical database application for medical research
A course project for TKT20019 - Databases and web programming

## Description
The purpose of this application is to provide an easy-to-use interface for clinicians and scientists to store, search and export clinical patient data for the purpose of medical research.

## Planned Features:
 - User login and authentication
 - User summary page
 - Record search with filters
 - Record export as .csv-files
   
## Data objects:
 - Patient: contains basic patient information like name, sex and social security number.
 - Diagnosis: an ICD11 diagnosis code
 - Sample: patient sample with features type and value
 - Comment: a free comment associated with a patient or a sample

# <b> WARNING! This application is for a course project, and it should not be used with real private patient data. There are no guarantees for the security of this application. </b>

----------

# Progress update for submission 2

## Current functions:
   - the user can create a new account
   - the user can log in/out to the created account
   - a logged in user may view listings of patients, diagnoses and samples
   - a logged in user can add items to each listing
   - each patient, diagnosis and sample has an details page accessible by clicking a link in the listing
   - each entry in the listings can be edited and deleted (editing broken as of now due to an unknown bug)
   - each patient details page contains the patient's diagnoses and samples (broken, work in progress)

The functions (try) to implement the requirements for the submission 2. Namely the patient details page implements a search for diagnoses and samples with the same patient id key.

