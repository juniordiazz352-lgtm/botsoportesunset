import json

DB = "db.json"

def load():
    try:
        with open(DB) as f:
            return json.load(f)
    except:
        return {
            "tickets": {},
            "forms": {},
            "panels": {"tickets": [], "forms": []},
            "responses": []
        }

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

# FORM BUILDER
def create_form(name):
    data = load()
    data["forms"][name] = []
    save(data)

def add_question(form, question):
    data = load()
    data["forms"][form].append(question)
    save(data)

def get_forms():
    return load()["forms"]

def save_response(user, form, answers):
    data = load()
    data["responses"].append({
        "user": user,
        "form": form,
        "answers": answers
    })
    save(data)
