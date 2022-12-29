# Web-App-AWS

A web application that randomly selects an entry from a database, shows it to the user, and allows the user to save contributions of their own, all from a single U.I.

[domdom on AWS](http://randomwisdom.eu-west-2.elasticbeanstalk.com/) (This version runs on an AWS EC2 server)

App runs in **Flask** framework with only 3 dependencies - see `requirements.txt`.

In the repo you will find:

## Front-end
The front-end U.I is built with HTML / CSS and uses Jinja2 templates to display the content.

### index.html / header.html / footer.html
- Returns the initially called information
- Allows one-click reloading
- Contains a form for users’ content

### form.html
- An include in index.html with the form attributes

### submitted.html
- Posts the form and returns the users’ contribution

### large.css
- CSS for a viewport => 1024px.

## Back-end
### application.py
- Launches the application

### database.py
- Interacts with the database using MySQL queries via SQLAlchemy

## Badges
![MIT license](https://badgen.net/badge/license/MIT/blue)
