from flask import Flask, request, make_response, send_from_directory
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import os

# ---------------- FLASK APP ----------------
app = Flask(__name__, static_folder="static")

# ---------------- GOOGLE SHEETS SETUP ----------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Read credentials from Render Environment Variable
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)

client = gspread.authorize(creds)

# Google Sheet name (must already exist)
SHEET_NAME = "ByteMatrix Client Enquiries"
sheet = client.open(SHEET_NAME).sheet1

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# ---------------- CONTACT FORM ----------------
@app.route("/contact", methods=["POST"])
def contact():
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        request.form.get("name", ""),
        request.form.get("email", ""),
        request.form.get("phone", ""),
        request.form.get("projectType", ""),
        request.form.get("budget", ""),
        request.form.get("message", ""),
        request.remote_addr,
        request.headers.get("User-Agent", "")
    ])

    # Thank-you page (inline HTML – safe & works on Render)
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Thank you | ByteMatrix Solutions</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="
      background:#020617;
      color:#e5e7eb;
      font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
      display:flex;
      align-items:center;
      justify-content:center;
      min-height:100vh;
      margin:0;
    ">
      <div style="text-align:center;max-width:480px;padding:1.5rem;">
        <h2 style="margin-bottom:0.8rem;">✅ Thank you for contacting ByteMatrix Solutions</h2>
        <p style="margin-bottom:1rem;">
          Your project details were received successfully.
          We’ll get back to you shortly.
        </p>
        <a href="/" style="color:#22d3ee;text-decoration:none;font-weight:500;">
          ← Back to portfolio
        </a>
      </div>
    </body>
    </html>
    """
    return make_response(html)

# ---------------- START APP ----------------
if __name__ == "__main__":
    app.run()
