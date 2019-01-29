"""
	this is a code example that use SMTP_SSL() to initiate a TLS-encrypted connection
"""

import smtplib, ssl, getpass

port = 465 # port number for SSL
smtp_server = "smtp.gmail.com" # we use gmail as our test smtp server
sender_email = "ericftp2019@gmail.com"
receiver_email = "ndingdw@gmail.com" # 
#password = input (" Type your password and press enter: ")
password = getpass.getpass(prompt="Type your password and press enter: ")

message = """\
Subject: Hi there

This is sent from python.
	
"""
# create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com",port, context = context) as server:
	server.login("ericftp2019@gmail.com", password)
	server.sendmail(sender_email, receiver_email, message)
