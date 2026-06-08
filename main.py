from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import json
import os

app = FastAPI()

class Contact(BaseModel):
    name: str
    phone: str
    email: EmailStr

def load_contacts():
    try:
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r") as file:
                data = json.load(file)
            return data
        else:
            return []
    except json.JSONDecodeError:
        return []
            
def save_contacts(contacts):
    with open("contacts.json", "w") as file:
        json.dump(contacts, file, indent=2)
        
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
    
def duplicate_phone_check(contacts: list, phone: str, ignore_phone=None):
    for con in contacts:
        if con["phone"]!=ignore_phone:
            if con["phone"]==phone:
                raise HTTPException(
                    status_code=409,
                    detail="Phone number already exists"
                )

def duplicate_email_check(contacts: list, email: str, ignore_phone=None):
    for con in contacts:
        if con["phone"]!=ignore_phone:
            if con["email"]==email:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists"
                )

contacts = load_contacts()

@app.get("/")
def welcome_message():
    return {"message": "Contact Manager API Running"}

@app.get("/contacts")
def display_contacts():
    return contacts

@app.post("/contacts", status_code=201)
def add_contact(contact: Contact):
    
    new_contact = normalize_contact(contact)
    
    validate_contact(new_contact)
    
    duplicate_phone_check(contacts, new_contact["phone"])
    duplicate_email_check(contacts, new_contact["email"])
            
    contacts.append(new_contact)
    save_contacts(contacts)
    return {"message": "Contact added successfully", "contact": new_contact}

@app.delete("/contacts/{phone}")
def delete_contact(phone: str):
    for index, contact in enumerate(contacts):
        if contact["phone"] == phone:
            deleted_contact = contacts.pop(index)
            save_contacts(contacts)
            return {"message": "Contact Deleted Successfully", "data": deleted_contact}
    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )
    
@app.get("/contacts/{phone}")
def search_contact(phone: str):
    for contact in contacts:
        if contact["phone"] == phone:
            return {"message": "Contact Found!","data": contact}
    raise HTTPException(
        status_code=404,
        detail="Contact not found!"
    )

@app.put("/contacts/{phone}")
def update_contact(phone: str, contact: Contact):
    updated_contact = normalize_contact(contact)
    
    validate_contact(updated_contact)
    
    duplicate_phone_check(contacts, updated_contact["phone"], ignore_phone=phone)
    duplicate_email_check(contacts, updated_contact["email"], ignore_phone=phone)
    
    for index, con in enumerate(contacts):
        if con["phone"] == phone:
            contacts[index] = updated_contact
            save_contacts(contacts)
            return {"message": "Contact updated successfully", "data": updated_contact}
    raise HTTPException(
        status_code=404,
        detail="Contact not found"
    )
            
            
            
            
        