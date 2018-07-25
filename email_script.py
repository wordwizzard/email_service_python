import os
import smtplib
import json
from datetime import datetime
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email import encoders

class FileManager:
    def __init__(self):
        self.filePathStorage = None
        self.filePathSrc = None
        self.host = None
        self.port = None
        self.host_usr = None
        self.host_psw = None
        self.adr1 = None
        self.adr2 = None
        self.adr3 = None
        self.message = None
        self.subject = None
        self.fileName1 = None
        self.fileName2 = None
        self.fileName3 = None
        self.current_date = None

    def loadconfig(self):

        self.current_date = datetime.now().date()
        # TODO:

        # Change directory to where the config.json file is located.
        os.chdir(self.filePathSrc)

        # Open the config.json file and save the relevant variables
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)

        server = data["emailServer"]
        details = data["emailDetails"]
        paths = data["filePaths"]
        self.host = server["host"]
        self.port = server["port"]
        self.host_usr = server["host_user"]
        self.host_psw = server["host_password"]

        self.adr1 = details["address1"]
        self.adr2 = details["address2"]
        self.adr3 = details["address3"]

        self.message = details["message"]
        self.subject = details["subject"]

        self.fileName1 = details["filename1"]
        self.fileName2 = details["filename2"]
        self.fileName3 = details["filename3"]

        self.filePathSrc = os.path.abspath(paths["source"])
        self.filePathStorage = os.path.abspath(paths["storage"])

    def email_files(self):
        # We should be in the directory where the file we want to attach are located.
        if os.getcwd() != self.filePathStorage:
            os.chdir(self.filePathStorage)

        try:
            # Changeable from the json object
            to_address = self.adr1 + ',' + self.adr2 + ',' + self.adr3
            message = self.message
            subject = self.subject + " @" + str(self.current_date)      # Added the date here since I needed it.
            files = [self.fileName1, self.fileName2, self.fileName3]

            server = smtplib.SMTP(str(self.host) + ":" + str(self.port))
            server.starttls()
            server.login(self.host_usr, self.host_psw)

            # Setup the email header details
            msg = MIMEMultipart(
                From=self.host_usr,
                To=self.adr1 + ',' + self.adr2 + ',' + self.adr3,
                Date=formatdate(localtime=True),
                Subject=subject
            )

            # Setup backend email details
            msg['Subject'] =subject
            msg['To'] = self.adr1 + ',' + self.adr2 + ',' + self.adr3
            msg.attach(MIMEText(message.replace('\\n','\n')))

            # Loop to attach all files in the files array
            for f in files:
                attachment = MIMENonMultipart('text', 'csv', charset='utf-8')
                attachment.set_payload(open(f, "rb").read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename=f)
                msg.attach(attachment)

            server.sendmail(self.host_usr, to_address, msg.as_string())
        except smtplib.SMTPRecipientsRefused as refused:
            print("Invalid address - {to_address}".format(to_address=self.adr1 + ',' + self.adr2 + ',' + self.adr3))
        finally:
            print('Done')
            if server:
                server.quit()


def main():

    fm = FileManager()
    fm.loadconfig()
    fm.email_files()


if __name__ == '__main__':
    main()