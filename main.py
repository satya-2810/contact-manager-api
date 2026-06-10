from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3

app = FastAPI()
class Contact(BaseModel):
    name: str
    phone: str
    email: EmailStr
    
def get_connection():
    con = sqlite3.connect("contacts.db")
    cursor = con.cursor()
    return con, cursor
    
def initialize_db():
    con, cursor = get_connection()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    """)
    con.commit()
    con.close()
        
def normalize_contact(contact: Contact):
    contact_dict = contact.model_dump()
    contact_dict["name"] = contact_dict["name"].strip()
    contact_dict["phone"] = contact_dict["phone"].strip()
    contact_dict["email"] = contact_dict["email"].strip().lower()
    return contact_dict
    
def validate_contact(normalized_contact: dict):
    if not normalized_contact["name"]:
        raise HTTPException(
                status_code=400,
                detail="Name cannot be blank"
            )
    if not normalized_contact["phone"].isdigit():
        raise HTTPException(
                status_code=400,
                detail="Phone number must contain only numbers"
            )
    if len(normalized_contact["phone"])!=10:
        raise HTTPException(
                status_code=400,
                detail="Phone number must be of 10 digits"
            )

def serialize_contact(contact):
    if not contact:
        return None
    contact_dict = {
        "id": contact[0],
        "name": contact[1],
        "phone": contact[2],
        "email": contact[3]
    }
    return contact_dict

initialize_db()

@app.get("/")
def welcome_message():
    return {"message": "Contact Manager API Running"}

@app.get("/contacts")
def display_contacts():
    con, cursor = get_connection()
    try:
        cursor.execute("""
                    SELECT * FROM contacts
                    """)
        contacts = cursor.fetchall()
    finally:
        con.close()
    contacts_list = [serialize_contact(contact) for contact in contacts]
    return contacts_list
    
@app.post("/contacts", status_code=201)
def add_contact(contact: Contact):
    
    new_contact = normalize_contact(contact)
    
    validate_contact(new_contact)
    
    con, cursor = get_connection()
    try:
        cursor.execute("""
            INSERT INTO contacts (name, phone, email) VALUES (?,?,?)""",
            (new_contact["name"], new_contact["phone"], new_contact["email"])
            )
        rowid = cursor.lastrowid
        new_contact["id"] = rowid
        con.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Phone number or email already exists"
        )
    finally:
        con.close()
    return {"message": "Contact added successfully", "data":  new_contact}

@app.delete("/contacts/{phone}")
def delete_contact(phone: str):
    con, cursor = get_connection()
    try:
        cursor.execute("""
                    SELECT * FROM contacts WHERE phone=?
                    """,
                    (phone,))
        deleted_contact = cursor.fetchone()
        if not deleted_contact:
            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )
        cursor.execute("""
                    DELETE FROM contacts WHERE phone=?
                    """,
                    (phone,))
        con.commit()
    finally:
        con.close()
    deleted_contact = serialize_contact(deleted_contact)
    return {"message": "Contact Deleted Successfully", "data": deleted_contact}
    
@app.get("/contacts/{phone}")
def search_contact(phone: str):
    con, cursor = get_connection()
    try:
        cursor.execute("""
                    SELECT * FROM contacts WHERE phone=?
                    """,
                    (phone,))
        contact = cursor.fetchone()
        if not contact:
            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )
    finally:
        con.close()
    contact = serialize_contact(contact)
    return {"message": "Contact Found", "data": contact}

@app.put("/contacts/{phone}")
def update_contact(phone: str, contact: Contact):
    updated_contact = normalize_contact(contact)
    
    validate_contact(updated_contact)
    
    con, cursor = get_connection()
    try:
        cursor.execute("""
                    SELECT * FROM contacts WHERE phone=?   
                    """,
                    (phone,)
                    )
        contact_to_update = cursor.fetchone()
        if not contact_to_update:
            raise HTTPException(
                status_code=404,
                detail="Contact not found"
            )
        updated_contact["id"]=contact_to_update[0]
        try:
            cursor.execute("""
                UPDATE contacts 
                SET 
                    name=?, 
                    phone=?, 
                    email=? 
                WHERE phone=?
                """,
                (updated_contact["name"], updated_contact["phone"], updated_contact["email"], phone)
                )
            con.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Phone number or email already exists"
            )
    finally:
        con.close()
    return {"message": "Contact updated successfully", "data": updated_contact}