import os
import imaplib
import email
import re
from email.header import decode_header
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path, override=True)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "zoho").lower()

IMAP_SERVERS = {
    "gmail": "imap.gmail.com",
    "outlook": "outlook.office365.com",
    "zoho": "imap.zoho.in"
}

imap_server = IMAP_SERVERS[EMAIL_PROVIDER]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9@\.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def decode_text(value):
    if not value:
        return ""

    result = ""
    for part, encoding in decode_header(value):
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="ignore")
        else:
            result += part
    return result


def get_email_body(msg):
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            if content_type == "text/plain":
                body += payload.decode(errors="ignore")

            elif content_type == "text/html":
                html = payload.decode(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                body += soup.get_text(separator=" ")

    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore")

    return body


training_data = pd.DataFrame({
    "text": [
        "winner lottery claim your prize now free money",
        "urgent verify your bank account password immediately",
        "congratulations you won cash reward click here",
        "free gift offer limited time claim now",
        "meeting scheduled tomorrow project discussion",
        "please find attached monthly report",
        "your interview is scheduled for monday",
        "team lunch planned for friday",
        "invoice attached for last month payment",
        "project status update and action items"
    ],
    "label": [
        "Spam", "Spam", "Spam", "Spam",
        "Ham", "Ham", "Ham", "Ham", "Ham", "Ham"
    ]
})

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_data["text"])
y = training_data["label"]

model = LogisticRegression()
model.fit(X, y)


def predict_spam(sender, subject, body):
    combined_text = f"{sender} {subject} {body}"
    cleaned = clean_text(combined_text)

    features = vectorizer.transform([cleaned])
    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0]
    spam_index = list(model.classes_).index("Spam")
    spam_score = probability[spam_index]

    return prediction, spam_score


print("EMAIL_PROVIDER:", EMAIL_PROVIDER)
print("IMAP SERVER:", imap_server)
print("USER:", EMAIL_USER)

try:
    mail = imaplib.IMAP4_SSL(imap_server, 993)
    print(mail.welcome)

    mail.login(EMAIL_USER, EMAIL_PASSWORD)
    print("IMAP Login Successful")

    mail.select("INBOX")

    status, messages = mail.search(None, "ALL")

    if status != "OK":
        print("No emails found")
        mail.logout()
        exit()

    email_ids = messages[0].split()
    latest_emails = email_ids[-10:]

    print("\nLIVE EMAIL SPAM DETECTION RESULT\n")

    for email_id in reversed(latest_emails):
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                sender = decode_text(msg.get("From"))
                subject = decode_text(msg.get("Subject"))
                body = get_email_body(msg)

                prediction, spam_score = predict_spam(sender, subject, body)

                print("=" * 80)
                print("From:", sender)
                print("Subject:", subject)
                print("Prediction:", prediction)
                print("Spam Score:", round(spam_score * 100, 2), "%")

    mail.logout()

except Exception as e:
    print("Error:", e)