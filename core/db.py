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
            "responses": []
        }

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

# TICKETS
def create_ticket(channel, user):
    data = load()
    data["tickets"][str(channel)] = {
        "user": user,
        "status": "open"
    }
    save(data)

def close_ticket(channel):
    data = load()
    if str(channel) in data["tickets"]:
        data["tickets"][str(channel)]["status"] = "closed"
        save(data)

# FORMULARIOS
def create_form(name):
    data = load()
    data["forms"][name] = []
    save(data)

def add_question(form, q):
    data = load()
    data["forms"][form].append(q)
    save(data)

def get_forms():
    return load()["forms"]

def save_response(user, form, answers):
    data = load()

    form_id = len(data["responses"]) + 1

    data["responses"].append({
        "id": form_id,
        "user": user,
        "form": form,
        "answers": answers,
        "status": "pending"
    })

    save(data)
    return form_id

def update_form_status(form_id, status):
    data = load()
    if "responses" in data:
        for f in data["responses"]:
            if str(f["id"]) == str(form_id):
                f["status"] = status
    save(data)
