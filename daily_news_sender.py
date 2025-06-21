import smtplib
from email.message import EmailMessage
import requests
import os
import json

api_key = os.getenv("NEWSAPI_API_KEY")  # Must be set in environment
EMAILS_FILE = "emails.json"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "daily.news.ai.agent@gmail.com"
SENDER_PASSWORD = "eppkppdojwpbtpis "  # Use app password for Gmail accounts with 2FA

def load_subscribers():
    if not os.path.exists(EMAILS_FILE):
        return []
    with open(EMAILS_FILE, "r") as f:
        try:
            data = f.read().strip()
            if not data:
                return []  # Empty file → treat as empty list
            return json.loads(data)
        except json.JSONDecodeError:
            return []

from main import get_article_summaries

def fetch_news(category):
    return get_article_summaries(category)

def format_articles(articles, urls):
    lines = []
    for key in articles:
        lines.append(f"<b>{key}</b><br>")
        lines.append(f"{articles[key]}<br>")
        lines.append(f"<a href='{urls[key]}'>Read more</a><br><br>")
    return "\n".join(lines)

def send_email(recipient, category, articles_html):
    msg = EmailMessage()
    msg["Subject"] = f"Daily {category.title()} News"
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg.set_content("Your email client does not support HTML.")
    msg.add_alternative(f"""\
    <html>
      <body>
        <h3>Here are today's top {category.title()} stories:</h3>
        {articles_html}
      </body>
    </html>
    """, subtype="html")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)

def main():
    subscribers = load_subscribers()
    grouped = {}
    for sub in subscribers:
        key = (sub["email"].lower(), sub["category"].lower())
        grouped.setdefault(key, None)

    for (email, category) in grouped:
        articles, urls = fetch_news(category)
        if not articles:
            continue
        html = format_articles(articles, urls)
        send_email(email, category, html)

if __name__ == "__main__":
    main()
