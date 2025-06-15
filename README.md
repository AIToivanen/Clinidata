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
   - each patient, diagnosis and sample has an details page accessible by clicking a link in the listing (not much content for diagnoses and samples)
   - each entry in the listings can be edited and deleted 
   - each patient details page contains the patient's diagnoses and samples 

The functions (try to) implement the requirements for the submission 2. Namely the patient details page implements a search for diagnoses and samples with the same patient id key.


----------

# Progress update for submission 3

## New features:
 - User page with counts of different data-items posted
 - Free-form comments on patient pages
 - Patient search based on first name, last name, or SSID
 - Pre-determined classes for sample type

Users are able to add new samples and diagnoses to patients added by any user. 

The whole application is designed with a very high-trust philosophy, so users are also able to edit and delete each other's added records.