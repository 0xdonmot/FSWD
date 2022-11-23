# Full Stack Web Developer Capstone - Casting Agency

## Project Description

This project sets up the backend API for a Casting Agency. The agency is responsible for creating movies and mananing and assigning actors to those movies. The structure built represents a preliminary API structure to allow the agency to store and access data in a simplified way.

The API currently allows the following calls:

1. Retrieve data on all actors / movies.
2. Delete an actor / movie.
3. Add an actor / movie.
4. Update an actor / movie.

The API implements a role-based-access-control system, which allows certain API calls based on the client's authorization. This was implemented using Auth0 using Json Web Tokens. Currently, unauthorized clients do not any access permissions to make API calls successfully. 

The backend scripts also sets up the required data models, namely a database and tables for actors and movies. In addition, the backend directory contains various tests used to test the API functionality. These were written using the Python unittest library and in Postman.

Finally, the app has been hosted on Heroku. It will be removed on 28 November 2022, when Heroku update their pricing policy.

## Project Motivation

This project serves as the capstone project for the Udacity Full Stack Web Developer nanodegree.

### About the Stack

The project only includes a backend. No frontend is currently configured.

The `./backend` directory contains a completed Flask server which uses the SQLAlchemy module. The folder contains scripts with the completed API endpoints, authentication and testing.

[View the README.md within ./backend for more details.](./backend/README.md)