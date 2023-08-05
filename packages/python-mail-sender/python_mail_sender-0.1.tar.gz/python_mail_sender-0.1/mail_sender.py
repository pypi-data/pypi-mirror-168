import smtplib, io, os, logging, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Tuple


logger = logging.getLogger(__name__)

class MailSender:
    def __init__(self):
        """ init the smtp server data"""
        self.sender_address = os.environ.get("SENDER_ADDR")
        self.sender_pass = os.environ.get("SENDER_PASS")
        self.smtp_port = int(os.environ.get("SMTP_PORT"))
        self.smtp_server = os.environ.get("SMTP_SERVER")

    def validate_email(self, field: str, email: str):
        errors = {}
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, email)):
            errors[field] = "Invalid {} Email.".format(field.capitalize())
        return errors

    def parse_file(self, file):
        if isinstance(file, io.BytesIO) or isinstance(file, io.StringIO):
            return file.getvalue()
        return file.read()

    def send_mail(
        self, receiver_address: str, subject: str, content: str,
        content_type: str = "plain", attach_files: Tuple[Tuple[str, io.FileIO]] = ()
    ):
        """ 
        - takes mail data and files and use smtp server data to send mail
        - Note that based on content type the content will be parsed
        """
        try:
            errors = {
                **self.validate_email("sender", self.sender_address),
                **self.validate_email("receiver", receiver_address)
            }

            if errors:
                raise Exception(errors)

            #Setup the MIME
            message = MIMEMultipart()
            message['From'] = self.sender_address
            message['To'] = receiver_address
            message['Subject'] = subject

            #The body and the attachments for the mail
            message.attach(MIMEText(content, content_type))
            for file in attach_files:
                payload = MIMEBase('application', 'octet-stream')
                payload.set_payload(self.parse_file(file[1]))
                encoders.encode_base64(payload) #encode the attachment
                #add payload header with filename
                payload.add_header('Content-Disposition', "attachment; filename= %s" % file[0])
                message.attach(payload)
            
            #Create SMTP session for sending the mail
            session = smtplib.SMTP(self.smtp_server, self.smtp_port)
            session.starttls() #enable security
            session.login(self.sender_address, self.sender_pass)
            text = message.as_string()
            session.sendmail(self.sender_address, receiver_address, text)
            session.quit()
            logger.info('Mail sending succeeded.', extra={"message": message})
            return True, "Mail Sent"
        except Exception as e:
            logger.exception('Mail sending failed.', extra={"error": e})
            return False, e.args[0]

