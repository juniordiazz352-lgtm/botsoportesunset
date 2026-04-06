from core.db import cursor
import json


def create_ticket(channel_id, user_id, ticket_type):
    cursor.execute(
        "INSERT INTO tickets VALUES (?, ?, ?, ?, ?)",
        (channel_id, user_id, ticket_type, None, 0)
    )
    cursor.connection.commit()


def get_ticket(channel_id):
    cursor.execute("SELECT * FROM tickets WHERE channel_id=?", (channel_id,))
    return cursor.fetchone()


def update_claim(channel_id, user_id):
    cursor.execute(
        "UPDATE tickets SET claimed_by=? WHERE channel_id=?",
        (user_id, channel_id)
    )
    cursor.connection.commit()


def close_ticket(channel_id):
    cursor.execute(
        "UPDATE tickets SET closed=1 WHERE channel_id=?",
        (channel_id,)
    )
    cursor.connection.commit()
