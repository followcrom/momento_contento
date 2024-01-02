# RanDOM WisDOM

**RanDOM WisDOM** is a dynamic web application that displays a random quote from a database to the user. In addition, users have the opportunity to contribute their own nuggets of wisdom to enrich our collective database, all accessible through a user-friendly interface.

![GitHub last commit](https://img.shields.io/github/last-commit/followcrom/Momento-Contento) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/followcrom/Momento-Contento)

![RanDOM WisDOM webpage](https://www.followcrom.online/embeds/gh_domdom_readme.jpg "RanDOM WisDOM webpage")

## Usage

### Front-end

UI built with HTML and CSS, leveraging Jinja2 templates to display the data.

**index.html / header.html / footer.html**

- These files handle the display of the initial content.
- They enable one-click refreshing of the random wisdom.
- Includes the form for users to contribute wisdom of their own.

**form.html**

- An include in index.html with the form attributes.

**submitted.html**

- Posts the form and returns the users’ contribution.

**large.css**

- CSS for a viewport => 1024px.

### Back-end

**application.py**

- Launches the app.

**database.py**

- Interacts with the database using MySQL queries via SQLAlchemy.

The application is built with the robust Flask framework and requires just four dependencies, which can be found in the `requirements.txt` file.

## Authors

🌐 followCrom: [followcrom.online](https://followcrom.online/index.html) 🌐

📫 followCrom: [get in touch](https://followcrom.online/contact/contact.php) 📫

[![Static Badge](https://img.shields.io/badge/followcrom-.online-blue?style=for-the-badge)](http://followcrom.online)

## License

This project is open source and available under the MIT License. See the LICENSE file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
