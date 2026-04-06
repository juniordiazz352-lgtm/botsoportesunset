import json
from core.db import cursor


def save_form(name, questions, channel_id):
    cursor.execute(
        "INSERT OR REPLACE INTO forms VALUES (?, ?, ?)",
        (name, json.dumps(questions), str(channel_id))
    )
    cursor.connection.commit()


def get_forms():
    cursor.execute("SELECT * FROM forms")
    data = cursor.fetchall()

    forms = {}
    for name, q, ch in data:
        forms[name] = {
            "questions": json.loads(q),
            "channel_id": int(ch)
        }

    return forms


def save_response(user_id, form_name, answers):
    cursor.execute(
        "INSERT INTO form_responses (user_id, form_name, answers) VALUES (?, ?, ?)",
        (user_id, form_name, json.dumps(answers))
    )
    cursor.connection.commit()
