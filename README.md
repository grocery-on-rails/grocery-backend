# Grocery On Rails Backend

This repository is the backend code of grocery-on-rails, a online grocery platform that supports mobile app and admin panel website. The backend is based on flask, a lightweight Python framework for handling http RESTful requests and connects to the MongoDB database.

## Features

Password hashing using *flask_bcrypt* library

User session management using JSON Web Token with *flask_JWT_extended* library

RESTful requests handling enhanced by *flask_restful* library

Connect to the MongoDB and convert documents into Python class with *mongoengine* library

## Deployment

First install the required libraries listed in the requirements.txt

Then run the app.py, which is the driver file of the backend service

The application is also configured to run on Heroku, the *Procfile* specifies relevant configurations in order to run on the Heroku

You can change the database address, password, and the port in *.env* file.