import subprocess
from datetime import datetime

SENDMAIL = '/usr/sbin/sendmail'

TO_EMAILS = [
    #"shrinivasgond8@gmail.com",
    "shrinivasam@iisc.ac.in",
    "dhyann@iisc.ac.in",
    #"yoginder@iisc.ac.in",
    "naveennayaka@iisc.ac.in",
    #"akhileshku@iisc.ac.in",
    "shivaprasadl@iisc.ac.in",
    "manjulap@iisc.ac.in"
]

FROM_NAME = 'SERC-RDP'
FROM_EMAIL = 'serc.remote.desktop.protocol@gmail.com'


def send_email(subject: str, html_body: str, to_emails=None):

    recipients = to_emails if to_emails else TO_EMAILS
    to_header = ", ".join(recipients)

    print("EMAIL ATTEMPTED TO:", recipients)

    msg = (
        f"From: {FROM_NAME} <{FROM_EMAIL}>\n"
        f"To: {to_header}\n"
        f"Subject: {subject}\n"
        f"MIME-Version: 1.0\n"
        f"Content-Type: text/html; charset=UTF-8\n\n"
        f"{html_body}"
    )

    try:
        subprocess.run(
            [SENDMAIL, "-t"],
            input=msg.encode("utf-8"),
            check=True
        )
        print(f"{datetime.now()} ✔ Email sent")
    except subprocess.CalledProcessError as e:
        print(f"{datetime.now()} ✖ Email send failed: {e}")
