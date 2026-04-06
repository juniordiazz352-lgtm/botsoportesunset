from core.db import cursor
import json

def save_form(name, questions):
    cursor.execute("INSERT OR REPLACE INTO forms VALUES (?, ?)", (name, json.dumps(questions)))
    cursor.connection.commit()

def get_forms():
    cursor.execute("SELECT * FROM forms")
    import json
    return {name: json.loads(q) for name, q in cursor.fetchall()}

def save_response(user_id, form_name, answers):
    import json
    cursor.execute(
        "INSERT INTO form_responses (user_id, form_name, answers) VALUES (?, ?, ?)",
        (user_id, form_name, json.dumps(answers))
    )
    cursor.connection.commit()
