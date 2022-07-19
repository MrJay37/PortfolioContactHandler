from email.mime.text import MIMEText
import json
import logging
import os
from smtplib import SMTP_SSL


def lambda_handler(event, context):
    # Create email message object
    msg = MIMEText(event['message'] + '\n\nReply back to them at at ' + event['email'])
    # Add subject, customize with name of message sender
    msg['Subject'] = f"Sanket! You have a new message from {event['name']}"
    # Add a custom from name
    msg['From'] = f"{event['name']} <{event['email']}>"
    # Add me to To
    msg['To'] = 'Me'

    try:
        # Create SMTP connection
        with SMTP_SSL(os.environ['SMTPHOST'], int(os.environ['SMTPPORT'])) as server:
            # Log in to server, credentials must be present in environment variables
            server.login(os.environ['SMTPUSER'], os.environ['SMTPPASS'])
            # Send email to self
            server.sendmail(os.environ['SMTPUSER'], [os.environ['SMTPUSER']], msg.as_string())
            # Close server
            server.close()

    except Exception as err:
        logging.error(f"Cannot send email: {err}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message": "Internal server error, cannot send message to user, please try again later"
            })
        }

    # Return response that message has been sent successfully
    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Email sent successfully!"
        })
    }


if __name__ == "__main__":
    lambda_handler(
        {
            "name": "Don Joe",
            "email": "test.email@example.com",
            "message": "How does this look?"
        }
        , None
    )
