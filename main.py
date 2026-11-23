from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT", "5432"),
        sslmode="require"
    )

class UserData(BaseModel):
    name: str
    email: str
    message: str | None = None

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, message FROM kontakter ORDER BY id ASC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": rows}

@app.post("/users")
def add_user(user: UserData):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO kontakter (name, email, message) VALUES (%s, %s, %s)",
        (user.name, user.email, user.message)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Lagret i kontakter!", "data": user}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kontakter WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Kontakt med ID {user_id} ble slettet!"}