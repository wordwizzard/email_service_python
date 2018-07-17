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

        self.filePathMaster = None
        self.filePathSrc = None

        self.host = None
        self.port = None
        self.host_usr = None
        self.host_psw = None

        self.adr1 = None
        self.adr2 = None
        self.adr3 = None

        self.current_date = None

    def loadconfig(self):

        self.current_date = datetime.now().date()

        self.filePathSrc = os.path.abspath('YOUR SOURCE FILEPATH - WHERE CODE IS LOCATED')
        self.filePathMaster = os.path.abspath('YOUR MASTER FOLDER - WHERE CSV FILES ARE LOCATED')

        # Change directory to where the config.json file is located.
        os.chdir(self.filePathSrc)

        # Open the config.json file and save the relevant variables
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)

        eS = data["emailServer"]
        self.host = eS["host"]
        self.port = eS["port"]
        self.host_usr = eS["host_user"]
        self.host_psw = eS["host_password"]

        self.adr1 = eS["address1"]
        self.adr2 = eS["address2"]
        self.adr3 = eS["address3"]


    def email_files(self):
        # We should be in the directory where the file we want to attach are located.
        if os.getcwd() != self.filePathMaster:
            os.chdir(self.filePathMaster)

        try:
            to_address = self.adr1
            # These can be added to the config.json file if you want to
            message = "WRITE SOME KIND OF MESSAGE IN HERE TO INSERT IT IN THE EMAIL"
            subject = "YOUR SUBJECT HEADING" + " @" + str(self.current_date)    # Added the date here since I needed it.

            file1 = 'FILENAME1.csv'
            file2 = 'FILENAME2.csv'
            file3 = 'FILENAME3.csv'
            files = [file1, file2, file3]

            server = smtplib.SMTP(str(self.host) + ":" + str(self.port))
            server.starttls()
            server.login(self.host_usr, self.host_psw)

            print("Receiver address - {to_address}".format(to_address=self.adr1 + ',' + self.adr2 + ',' + self.adr3))
            print("Building email content")

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
            print('Done Sending mail')
            if server:
                server.quit()


def main():
    print("Start Program")

    fm = FileManager()
    fm.loadconfig()
    fm.email_files()


if __name__ == '__main__':
    main()