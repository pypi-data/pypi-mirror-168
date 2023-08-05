import pandas as pd
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
from IPython.core.magic import  Magics, magics_class, cell_magic, line_magic

@magics_class
class Tutor(Magics):

  def __init__(self, shell=None,  **kwargs):
    super().__init__(shell=shell, **kwargs)

  @cell_magic
  def pytutor(self, line, cell):
    import urllib.parse
    url_src = urllib.parse.quote(cell)
    str_begin = '<iframe width="1000" height="500" frameborder="0" src="https://pythontutor.com/iframe-embed.html#code='
    str_end   = '&cumulative=false&py=3&curInstr=0"></iframe>'
    import IPython
    from google.colab import output
    display(IPython.display.HTML(str_begin+url_src+str_end))


class list_upload:

    def __init__(self,url):
        self.url = url
        global URL
        URL =self.url

    @property
    def show(self):
        df = pd.read_csv(URL)
        return df
    
    @property
    def welcome(self):
        df = self.show
        col = df["nombres"]
        for nombre in col:
            print("BIENVENIDO AL CURSO"+" "+ nombre.upper())

    @property
    def winner(self):
        df = self.show
        col = df["nombres"]
        ganador = random.choice(col)
        return ganador

    def send_mail(self,asunto,mensaje,correo,test_mail=False):

        df = self.show
        sender_address = correo
        sender_pass = getpass("Enter password ")

        subject = asunto
        messenger = mensaje 

        if test_mail== True:
            nombre = df["nombres"][0].split()[0]

            receiver_address = correo

            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = subject 

            mail_content = messenger.format(nombre) 


            # Sent Email
            # https://www.google.com/settings/security/lesssecureapps
            # https://support.google.com/accounts/answer/185839 verificación en dos pasos

            message.attach(MIMEText(mail_content, 'plain'))
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print("Mail Sent Successfully")

        else:
            
            for i in range(df.shape[0]):
                nombre = df["nombres"][i].split()[0]

                receiver_address = df["correos"][i].split()[0]

                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = subject 

                mail_content = messenger.format(nombre)

                # Sent Email
                message.attach(MIMEText(mail_content, 'plain'))
                session = smtplib.SMTP('smtp.gmail.com', 587)
                session.starttls()
                session.login(sender_address, sender_pass)
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)

            session.quit()
            print("Successfully Sent Emails")

            
