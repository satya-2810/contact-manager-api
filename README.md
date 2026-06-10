# Contact Manager API

A RESTful Contact Manager API built using **FastAPI** and **SQLite** that supports full CRUD operations with proper validation, database persistence, and duplicate prevention.

## Features

* Add a contact
* View all contacts
* Search a contact by phone number
* Update contact details
* Delete a contact
* Input validation
* Duplicate phone/email prevention using database constraints
* Persistent storage using **SQLite**
* Auto-generated interactive API documentation using Swagger UI

---

## Tech Stack

* Python
* FastAPI
* Pydantic
* SQLite3

---

## Project Structure

```text
Contact_Manager_API/
│── main.py
│── contacts.db
│── requirements.txt
│── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd Contact_Manager_API
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Server will run on:

```text
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

| Method | Endpoint            | Description                    |
| ------ | ------------------- | ------------------------------ |
| GET    | `/`                 | Welcome message                |
| GET    | `/contacts`         | Get all contacts               |
| GET    | `/contacts/{phone}` | Search contact by phone number |
| POST   | `/contacts`         | Add a new contact              |
| PUT    | `/contacts/{phone}` | Update existing contact        |
| DELETE | `/contacts/{phone}` | Delete contact                 |

---

## Validation Rules

### Name

* Cannot be blank

### Phone Number

* Must contain only digits
* Must be exactly **10 digits**
* Must be unique

### Email

* Must be a valid email format
* Must be unique

---

## Database Schema

The API uses a SQLite database (`contacts.db`) with the following schema:

```sql
CREATE TABLE contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);
```

---

## Example Contact Format

### Request Body

```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "email": "johndoe@gmail.com"
}
```

### Response Example

```json
{
  "message": "Contact added successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "phone": "9876543210",
    "email": "johndoe@gmail.com"
  }
}
```

---

## Error Handling

The API returns meaningful HTTP status codes:

| Status Code | Meaning                         |
| ----------- | ------------------------------- |
| 200         | Success                         |
| 201         | Resource created successfully   |
| 400         | Invalid input                   |
| 404         | Contact not found               |
| 409         | Duplicate phone number or email |

---
