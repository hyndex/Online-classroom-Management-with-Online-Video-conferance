# Online classroom Management with Online Video conferance

![Made with Love in India](https://madewithlove.org.in/badge.svg) [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

It is a cloudbased online class management system with video conferancing solution. 
But its only the backend 
Build on Django

  - Build on django
  - Store files in any S3 compitable storage solution(set the creds in settings.py)
  - Magic

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
Python 3 or more
Install According to requirments.txt
[Knowledge] just kidding
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be
Setup These in settings.py
```
SENDGRID_API_KEY = 'dtjfhhhhhhhhhhhhhhhhhhhhhqqqqqqqqqqqqqqqqqqqqqqqq'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 25
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@sg.gotoclass.online'
```
then
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### API REFERANCE  and ENDPOINTS
```
registration http://domain/auth/registration/
{ "username": "", "email": "", "password1": "", "password2": "" }

login http://domain/auth/twitter/
login http://domain/auth/facebook/
login http://domain/auth/login/
{

"username": "admin", "password": "qwerty" }

http://domain/self/ GET for self id
group http://domain/group/ POST GET PUT DELETE
{

"name": "CS601", "description": "SJN" }

add member http://domain/add/ POST GET DELETE
{ "username": "", "groupid": "", "role": "" }

notes http://domain/class/notes/ POST GET PUT DELETE
{ "groupid": 1, #send a dummy groupid for PUT .. "title": "First Note 2 Reviced", "description": "Demo" }

assignment http://domain/class/assignment/ POST GET PUT DELETE
{

"groupid": 1, "title": "diki@238198544", "description": "diki@238198544", "deadline": "05071999" }

/class/notes_upload/int:notesid/ for upload PUT DELETE
/class/notes_upload/int:fileid/ for delete PUT DELETE
/class/assignment_upload/<int:assignment id>/ for upload PUT DELETE
/class/assignment_upload/int:fileid/ for delete PUT DELETE
/class/submit_upload/<int:submit id id>/ for upload PUT DELETE
/class/submit_upload/int:fileid/ for delete PUT DELETE
/class/room POST DELETE
/invoice/
```
