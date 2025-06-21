import streamlit as st
import json
import os

st.title("Daily News Subscription")
st.write("Enter your email and preferred news category to subscribe.")

EMAILS_FILE = "emails.json"

def load_emails():
    if not os.path.exists(EMAILS_FILE):
        return []
    with open(EMAILS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # Return empty list if file is empty or malformed


def save_email(email_entry):
    emails = load_emails()
    emails.append(email_entry)
    with open(EMAILS_FILE, "w") as f:
        json.dump(emails, f, indent=2)

# Form input
with st.form("subscription_form"):
    email = st.text_input("Email Address")
    category = st.selectbox("Select News Category", [
        "business", "entertainment", "general", "health", "science", "sports", "technology"
    ])
    submit = st.form_submit_button("Subscribe")

    if submit:
        if not email or "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            entry = {"email": email, "category": category}
            save_email(entry)
            st.success(f"Subscription saved for {email} with category '{category}'.")
