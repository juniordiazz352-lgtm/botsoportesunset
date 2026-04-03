from fastapi import FastAPI
from core.db import load, create_form, add_question

app = FastAPI()

@app.get("/")
def home():
    return load()

@app.post("/create_form/{name}")
def create(name: str):
    create_form(name)
    return {"ok": True}

@app.post("/add_question/{form}")
def add_q(form: str, q: str):
    add_question(form, q)
    return {"ok": True}
