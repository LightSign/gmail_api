import base64
import apiclient
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from gmail_auth import create_Gmail_credential

def send_msg_with_file(sender, to, subject, message_text, file_name):
    """Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.
    Returns:
    An object containing a base64url encoded email object.
    """
    # initialize message object
    message = MIMEMultipart()
    # set each elementes needed
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    try:
        # defie file type
        msg = MIMEBase('text', 'comma-separated-values')
        # define file location and open it
        file_location = os.path.abspath(file_name)
        # make attachment
        attachment = open(file_location, "rb")
        # set attachment
        msg.set_payload((attachment).read())
        encoders.encode_base64(msg)
        msg.add_header(f'Content-Disposition', "attachment; filename={file_location}")
        # attach the file
        message.attach(msg)
    except:
        print("There is no file here")
    # encode bytes string
    byte_msg = message.as_string().encode(encoding="UTF-8")
    byte_msg_b64encoded = base64.urlsafe_b64encode(byte_msg)
    str_msg_b64encoded = byte_msg_b64encoded.decode(encoding="UTF-8")
    return {"raw": str_msg_b64encoded}

def send_message(to, subject, message_text, file_name):
    # "me" means that your email address authorized
    sender = "me"
    # create credentials
    service = create_Gmail_credential()
    try:
        result = service.users().messages().send(
            userId=sender,
            body=send_msg_with_file(sender, to, subject, message_text, file_name)
        ).execute()
        print("Message Id: {}".format(result["id"]))
    except apiclient.errors.HttpError:
        print("------start trace------")
        traceback.print_exc()
        print("------end trace------")

if __name__ == "__main__":
    # set email address you want to send
    to = "xxxxxx@gmail.com"
    # set subject
    subject = "Test sending csv using Gmail api"
    # set message
    message_text = "This is a Gmail API test"
    send_message(to, subject, message_text, file_name)
