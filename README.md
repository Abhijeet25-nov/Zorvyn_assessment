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

## Tech Stack
- **Backend:** Flask (Python)
- **API Testing Tool:** Postman
- **Database:** PostgreSQL
- **Library:** psycopg2

## Authentication & Authorization
- **Role-based access is implemented using request headers:**
-  Role: admin / analyst / viewer
- **Middleware:** check_role(allowed_roles)

## API Endpoints
### User APIs
1.Create User
- POST /users
- Access: Admin

- Body:
```
{
  "name": "Abhijeet",
  "email": "test@gmail.com",
  "passcode": "1234",
  "role": "analyst"
}
```

### Validations:
- Email format check
- Passcode must be numeric and ≤ 4 digits
- Unique name & email

2.Delete User
- DELETE /users
- Access: Admin
  
- Body:
```
{
  "user_id": "AN12345",
  "passcode": "1234"
}
```
--------------------------------------------

### Login API
3.Login
- POST /login
- Access: Admin, Analyst

- Body:
```
{
  "email": "test@gmail.com",
  "passcode": "1234"
}
```
------------------------------------------------

### Record APIs
4.Create Record
- POST /records
- Access: Admin
```
{
  "user_id": "AN12345",
  "amount": 5000,
  "type": "income",
  "category": "salary",
  "date": "2026-04-01",
  "notes": "Monthly salary"
}
```
5.Get All Records
- GET /records
- Access: Admin, Analyst

6.Delete Record
- DELETE /records
- Access: Admin
```
{
  "user_id": "AN12345",
  "category": "salary",
  "date": "2026-04-01"
}
```
------
### Dashboard API
7.User Dashboard
- GET /dashboard?user_id=AN12345
- Access: Admin, Analyst, Viewer
- Response:
```
Output :
{
  "total_income": 10000,
  "total_expense": 2000,
  "net_balance": 8000
}
```
-------

### Default Salary API
8.Add Default Salary to All Users
- POST /df_sal
- Access: Admin
```
{
  "amount": "5000",
  "date": "2026-04-01"
}
Adds salary entry for all users
```
--------

## Database Schema

### Users Table
| Column Name | Data Type   | Constraints                              | Description            |
|------------|------------|------------------------------------------|------------------------|
| user_id    | VARCHAR    | PRIMARY KEY                              | Unique user ID         |
| name       | VARCHAR    | NOT NULL                                 | User's name            |
| email      | VARCHAR    | UNIQUE, NOT NULL                         | User's email           |
| passcode   | VARCHAR(4) | NOT NULL                                 | 4-digit passcode       |
| role       | VARCHAR    | CHECK ('admin', 'analyst', 'viewer')     | User role              |
| is_active  | BOOLEAN    | DEFAULT TRUE                             | Active status          |
---
### Records Table
| Column Name | Data Type | Constraints                              | Description              |
|------------|----------|------------------------------------------|--------------------------|
| id         | SERIAL   | PRIMARY KEY                              | Record ID                |
| user_id    | VARCHAR  | FOREIGN KEY → users(user_id)             | Linked user              |
| amount     | NUMERIC  | NOT NULL                                 | Transaction amount       |
| type       | VARCHAR  | CHECK ('income', 'expense')              | Transaction type         |
| category   | VARCHAR  | NOT NULL                                 | Category of transaction  |
| date       | DATE     | NOT NULL                                 | Transaction date         |
| notes      | TEXT     | OPTIONAL                                 | Additional notes         |
---
## Relationships
- One **User** can have multiple **Records**
- `user_id` in `records` references `users(user_id)`

---
##  Setup Instructions
Follow these steps to run the **Finance Data Processing** locally:
---
###  1. Clone the Repository
```bash
git clone <your-repo-link>
cd FD_Final
```
#### Create virtual environment
```python -m venv venv```
#### Activate venv (Windows)
```venv\Scripts\activate```
#### Activate venv (Mac/Linux)
```source venv/bin/activate```

### 2.Install Dependencies
```pip install flask psycopg2```

-----------------------
### 3.Setup Database
```Create a PostgreSQL database named:
Finance_db
```
Run the SQL file:
-- Run Finance_db.sql

----------------------------------------------------
### 4.Configure Database
Update credentials in database.py:
```
host="localhost"
database="Finance_db"
user="postgres"
password="your_password"
```
--------------------------------------------------------------
### 5. Run Application
```python app.py```

-------

## API Testing
All APIs were tested using **Postman**:
- Used headers for role-based access
- Sent JSON payloads for POST/DELETE
- Verified responses and status codes

## Key Features
- Role-Based Access Control (RBAC)
- Modular Flask Architecture (Blueprints)
- PostgreSQL Integration
- Input Validation (Email & Passcode)
- Bulk Salary Update Feature
