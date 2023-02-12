import pandas as pd
import smtplib

def send_email(emails,company_name,message_text):
    your_email = "screenit183@gmail.com"
    your_password = "netaeupsaldaeqvx"

    # establishing connection with gmail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(your_email, your_password)

    # iterate through the records
    for i in range(len(emails)):
        # for every record get the name and the email addresses

        email = emails[i]

        # the message to be emailed
        message = """Congratulations!
        You have been shortlisted by {}
        
        {}""".format(company_name,message_text)

        message = 'Subject: {}\n\n{}'.format("Shortlisted for next round", message)

        # sending the email
        server.sendmail(your_email, [email], message)

    # close the smtp server
    server.close()
    print("message sent")

