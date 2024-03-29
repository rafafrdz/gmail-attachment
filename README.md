# Gmail Attachment

El siguiente proyecto consiste en la descarga de los archivos adjuntos a los mails que se ha recibido en el mes actual. El cliente de correos que se utilzia es el de Google, esto es, Gmail.

Los datos de cuenta de correo y contraseña, de momento, iran en texto plano en un archivo yml de configuración. No es lo apropiado, puesto que debería ir securizado, sin embargo se estudiará ese punto en un futuro.

Una alternativa a esa forma de conexión seria mediante un prompt a la shell que pidiera tanto email como contraseña, lo cual sí sería más "seguro", pero una tarea incómoda tanto para un desarrollo como para el consumo de la aplicación de forma excesivamente reiterada.

## Requisitos

Antes de continuar, se debe [habilitar los permisos de aplicaciones poco seguras](https://myaccount.google.com/lesssecureapps) en la cuenta de Gmail que vayamos a utilizar y habilitar el [Acceso via IMAP](https://support.google.com/mail/answer/7126229?hl=es).

Puede obtener mayor información aqui: [Aplicaciones poco seguras y la cuenta de Google](https://support.google.com/accounts/answer/6010255?hl=es)

## Código

#### Archivo de configuración YML

```yaml
user: user@gmail.com # Cuenta de gmail
passwd: passswd # Password
```

#### mail.py

```python
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

```

## Autores ✒️

_Se agradece la reseña o cita del autor, de su trabajo y del propio repositorio en los trabajos a los que haya aportado algo de luz y conocimiento._

**Rafael Fernández Ortiz**.- :briefcase: [LinkedIn](https://www.linkedin.com/in/rafael-fern%C3%A1ndez-ortiz-7a1684171/) - ​<img src="https://img.icons8.com/color/20/000000/open-envelope.png">​ ​[Gmail](mailto:rafaelfernandezortiz@gmail.com) - ​<img src="https://img.icons8.com/color/20/000000/cardboard-box.png">​ [GitHub](https://github.com/rafafrdz) - :bookmark_tabs: [Cv](https://rafafrdz.github.io/) 

