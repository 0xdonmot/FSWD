Fyyur
-----

## Overview

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

This project involved building the backend data model and controller structure for the Fyyur music app.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
The app uses the following tech stack:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** as the ORM library of choice
 * **PostgreSQL** as the database of choice
 * **Python3** and **Flask** server language and server framework
 * **Flask-Migrate** for creating and running schema migrations


### 2. Frontend Dependencies
* **HTML**
* **CSS**
* **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/)


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py
  ├── config.py
  ├── error.log
  ├── forms.py
  ├── requirements.txt
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in `models.py`.
* Controllers are located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`
