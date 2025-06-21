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

def entry_exists(email_entry, emails):
    return any(
        entry["email"].lower() == email_entry["email"].lower() and
        entry["category"].lower() == email_entry["category"].lower()
        for entry in emails
    )


def save_email(email_entry):
    emails = load_emails()
    if not entry_exists(email_entry, emails):
        emails.append(email_entry)
        with open(EMAILS_FILE, "w") as f:
            json.dump(emails, f, indent=2)
        return True
    else:
        return False

# Encryption for emails, will fix later

#from email_encryption import load_emails_encrypted, save_emails_encrypted
#
#def save_email(entry):
#    emails = load_emails_encrypted()
#    if not any(
#        e["email"].lower() == entry["email"].lower() and
#        e["category"].lower() == entry["category"].lower()
#        for e in emails
#    ):
#        emails.append(entry)
#        save_emails_encrypted(emails)
#        return True
#    return False


# Form input
with st.form("subscription_form"):
    email = st.text_input("Email Address")
    category = st.selectbox("Select News Category", [
        "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"
    ]).lower()
    submit = st.form_submit_button("Subscribe")

    if submit:
        if not email or "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            entry = {"email": email, "category": category}
            added = save_email(entry)
            if added:
                st.success(f"Subscription saved for {email} with category '{category}'.")
            else:
                st.info(f"{email} is already subscribed to category '{category}'.")
