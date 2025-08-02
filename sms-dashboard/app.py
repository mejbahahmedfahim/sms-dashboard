from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('sms.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    body TEXT,
                    device_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/api/receive_sms", methods=["POST"])
def receive_sms():
    sender = request.form.get("sender")
    body = request.form.get("body")
    device_id = request.form.get("device_id")

    conn = sqlite3.connect('sms.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, body, device_id) VALUES (?, ?, ?)", (sender, body, device_id))
    conn.commit()
    conn.close()
    return "SMS received", 200

@app.route("/admin")
def admin_dashboard():
    conn = sqlite3.connect('sms.db')
    c = conn.cursor()
    c.execute("SELECT sender, body, device_id, timestamp FROM messages ORDER BY timestamp DESC")
    messages = c.fetchall()
    conn.close()
    return render_template("dashboard.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
