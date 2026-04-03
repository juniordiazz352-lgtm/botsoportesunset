def generate_transcript(messages):
    html = """<html><body style='background:#0f172a;color:white'>"""

    for m in messages:
        content = m.content.replace("<", "&lt;").replace(">", "&gt;")
        html += f"<p><b>{m.author}</b>: {content}</p>"

    html += "</body></html>"
    return html
