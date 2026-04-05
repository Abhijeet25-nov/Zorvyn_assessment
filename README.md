# Zorvyn_assessment

## Finance Data Processing Backend System
The Finance Data Processing is a backend application designed to efficiently manage and analyze financial data for multiple users. Built using Flask and PostgreSQL, the system provides a structured way to handle user management, financial records, and real-time insights through API endpoints.All APIs were thoroughly tested using Postman, ensuring proper request handling, validation, and response accuracy.

The system supports three roles:
Admin
Analyst
Viewer
Each role has different levels of access to the API endpoints.

## Project Structure
```
Finace_Daashboard/
│── app.py
│── database.py
│── Finance_db.sql
│
├── config/
│   ├── auth.py
│   ├── login.py
│   ├── prefix_id.py
│
├── routes/
│   ├── user_routes.py
│   ├── record_routes.py
│   ├── dashboard_route.py
│   ├── default_salary_route.py
```


