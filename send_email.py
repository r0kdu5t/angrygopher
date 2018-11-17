#! /usr/bin/python
'''
# send_email.py - a program to send email using smtplib
#
# See here: https://linuxhint.com/sending-email-python/
'''
import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_FROM = 'SEND_FROM'
EMAIL_PWD = 'EMAIL_PWD'

def get_users_data(file_name):
    user_name = []
    user_email = []
    with open(file_name, mode='r', encoding='utf-8') as user_file:
        for user_info in user_file:
            user_name.append(user_info.split()[0])
            user_email.append(user_info.split()[1])
    return user_name, user_email

def read_template(file_name):
    with open(file_name, 'r', encoding='utf-8') as msg_template:
        msg_template_content = msg_template.read()
    return Template(msg_template_content)

def main():
    user_name, user_email = get_users_data('users.txt') # read user details
    message_template = read_template('message.txt')

    # set up the SMTP server
    smtplib_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtplib_server.starttls()
    smtplib_server.login(SEND_FROM, EMAIL_PWD)

    # Get each user detail and send the email:
    for name, email in zip(user_name, user_email):
        multipart_message = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        msg = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(msg)

        # setup the parameters of the message
        multipart_message['From']=SEND_FROM
        multipart_message['To']=email
        multipart_message['Subject']="LinuxHint Email"
        
        # add in the message body
        multipart_message.attach(MIMEText(msg, 'plain'))
        
        # send the message via the server set up earlier.
        smtplib_server.send_message(multipart_message)
        del multipart_message
        
    # Terminate the SMTP session and close the connection
    smtplib_server.quit()
    
if __name__ == '__main__':
    main()