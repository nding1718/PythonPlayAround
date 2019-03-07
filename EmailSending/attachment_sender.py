"""
	In order to send binary file to an email server that is designed to work with textual data, they need to be encoded before transport, we can use base64 to encode binary data into printable ASCII characters
"""

import email, smtplib, ssl,getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "An email with attachment from Python"
body = "This is an email with attachment sent from python"
sender_email = "ericftp2019@gmail.com"
receiver_email = "ndingdw@gmail.com"
password = getpass.getpass(prompt="Type your parssword and press enter: ")

#create a multipart message and set headers

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email

# add body to email
message.attach(MIMEText(body, "plain"))

filename = "document.pdf"

# open PDF file in binary mode
with open(filename, "rb") as attachment:
	# add file as application/octet-stream
	# Email client can usually download this automatically as attachment
	part = MIMEBase("application", "octet-stream")
	part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value part to attachment part
part.add_header(
	"Content-Disposition",
	f"attachment; filename={filename}",
)

# Add attachment to message and convert message to string

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, text)


