This application uses the Flask framework to build a backed server for the Habit Tracker application.

The database used is a postgres db.

To run unit tests, a docker container is created with the postgres db. Tests are run against the db inside the container. This way the actual db is not affected either in the dev or production environments.

Run the run_unit_tests.sh script to kick off the unit tests. (The unittest package from python is used for the unit tests.)