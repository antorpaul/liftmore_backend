# LiftMore Backend
This repository contains all of the code to make up the back-end and API for the LiftMore app.


## Structure
**db/** Contains all the DTO and ORM definitions for the models necessary to work with the front-end. There is no migrations folder because database changes are saved privately & managed through Raw SQL. 

├── db/
│   ├── models
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── connection.py
│   ├── session.py

**api/** Contains all of the routes available from the API. These routes are included via the app object in main.py.

├── api/
│   ├── v1
│   │   ├── __init__.py
|   |   ├── category_routes.py
|   |   ├── exercise_routes.py
|   |   ├── routine_template_router.py
|   |   ├── user_routes.py
│   ├── __init__.py

**core/** Contains utility functions and POCO that are common to different parts of the app (ie. schemas are used in DB and API modules).

├── core/
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── common.py
│   ├── utility
│   │   ├── __init__.py
│   │   ├── auth.py
|   ├── __init__.py
|   ├── config.py

├── __init__.py
├── main.py
