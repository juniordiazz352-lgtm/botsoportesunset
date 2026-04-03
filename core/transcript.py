def generate_transcript(messages):
    html = """
    <html>
    <head>
    <style>
    body { background:#0f172a; color:white; font-family:sans-serif }
    .msg { margin:10px; padding:10px; background:#1e293b; border-radius:10px }
    </style>
    </head>
    <body>
    <h1>Transcript</h1>
    """

    for m in messages:
        html += f"<div class='msg'><b>{m.author}</b>: {m.content}</div>"

    html += "</body></html>"
    return html
