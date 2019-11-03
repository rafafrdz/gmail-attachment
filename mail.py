# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.
import datetime, email, imaplib, os
import yaml

class mail():
    def __init__(self, config_mail, server='imap.gmail.com'):
        self.config_mail = yaml.safe_load(open(config_mail))
        self.userMail = self.config_mail.get('user')
        self.__password = self.config_mail.get('passwd')
        self.__server = server

    def __conexion(self):
        try:
            imapSession = imaplib.IMAP4_SSL(self.__server)
            imapSession.login(user=self.userMail, password=self.__password)
            return imapSession
        except:
            print('Error Login')

    def __attachment(self, partMail, fileName, categoria='attachment'):
        detach_dir = '.'
        if categoria not in os.listdir(detach_dir):
            os.mkdir(os.path.join(detach_dir, categoria))
        filePath = os.path.join(detach_dir, categoria, fileName)
        if not os.path.isfile(filePath):
            fp = open(filePath, 'wb')
            fp.write(partMail.get_payload(decode=True))
            fp.close()

    # Descarga los archivos adjuntos de los mails del mes actual
    def latest_mails(self, Label='inbox', limit=100):
        imapSession = self.__conexion()
        imapSession.select(Label)
        month_now = (datetime.date.today() + datetime.timedelta(365 / 12)).strftime("01-%b-%Y")
        month_last = (datetime.date.today()).strftime("01-%b-%Y")

        typ, data = imapSession.search(None,
                                       '(SINCE "{m_last}" BEFORE "{m_now}")'.format(m_last=month_last, m_now=month_now))
        ids = data[0].split()[::-1][:limit]
        for msgId in ids:
            typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
            if typ != 'OK':
                print('Error fetching mail.')

            emailBody = (messageParts[0][1])
            mail = email.message_from_bytes(emailBody)
            for part in mail.walk():
                fileName = part.get_filename()
                if bool(fileName):
                    self.__attachment(part, fileName)

        # Desconexion y desloggeo
        imapSession.close()
        imapSession.logout()

if __name__ == "__main__":
    mail = mail("config_mail.yml")
    mail.latest_mails()
