"""
	This is an example that sends a plain-text email over the SMTP connection secured with .starttls()
"""

import smtplib, ssl, getpass

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "ericftp2019@gmail.com"
receiver_email = "ndingdw@gmail.com"
password = getpass.getpass(prompt="Type your password and press enter: ")
message = """\
Subject: Hi there

This message is end from python use second method."""

# create a secure SSL context

context = ssl.create_default_context()

# Try to log in to server and send email

try:
	server = smtplib.SMTP(smtp_server, port)
	server.ehlo() # can be ommitted
	server.starttls(context = context) # Secure the connection
	server.ehlo()
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)
except Exception as e:
	# Print any error mesages to stdout
	print(e)
finally:
	server.quit()
