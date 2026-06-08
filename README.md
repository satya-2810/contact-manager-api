# Contact Manager API

A simple Contact Manager REST API built with **FastAPI** that supports full CRUD operations with JSON file persistence.

## Features

* Add a contact
* View all contacts
* Search a contact by phone number
* Update contact details
* Delete a contact
* Input validation
* Duplicate phone/email prevention
* Persistent storage using `contacts.json`

## Tech Stack

* Python
* FastAPI
* Pydantic
* JSON (for storage)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd Contact_Manager_API
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Server will run on:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| GET    | `/`                 | Welcome message         |
| GET    | `/contacts`         | Get all contacts        |
| GET    | `/contacts/{phone}` | Search contact by phone |
| POST   | `/contacts`         | Add new contact         |
| PUT    | `/contacts/{phone}` | Update contact          |
| DELETE | `/contacts/{phone}` | Delete contact          |

## Validation Rules

### Name

* Cannot be blank

### Phone Number

* Must contain only digits
* Must be exactly 10 digits
* Must be unique

### Email

* Valid email format required
* Must be unique

## Storage

Contacts are stored in a local:

```text
contacts.json
```

file to persist data even after server restart.

## Example Contact Format

```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "email": "johndoe@gmail.com"
}
```
