# RanDOM WisDOM

**RanDOM WisDOM** is a dynamic web application that displays a random quote from a database to the user. In addition, users have the opportunity to contribute their own nuggets of wisdom to enrich our collective database, all accessible through a user-friendly interface.

## Getting Started

🚀 [RanDOM WisDOM runnng on AWS](http://random-wisdom.eu-west-2.elasticbeanstalk.com/) 🚀

![RanDOM WisDOM webpage](https://www.followcrom.online/embeds/gh_domdom_readme.jpg "RanDOM WisDOM webpage")

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

The application is built with the robust Flask framework and requires just four dependencies, which can be found in the `requirements.txt` file.

## Badges

![MIT license](https://badgen.net/badge/license/MIT/blue)
