'''
Base class for notification
'''
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
from config import config

class notification(object):
    def __init__(self, host, port, name, password, usetls):
        self.host = host 
        self.port = port
        self.name = name
        self.password = password

    def sendNotification():
        pass

class mail_notification(notification):
    def __init__(self,host=config['mail_conf']['mail_hostname'], 
            port=config['mail']['mail_port'],\
            name=config['mail']['mail_login'],\
            password=config['mail']['mail_pass']),\
            usetls = config['mail_conf']['mail_tls']):
        super(mail_notification, self).__init__(host, port, name, password, usetls)
        try:
            if usetls:
                self.server = smtplib.SMTP(self.host, self.port)
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login(self.name, self.password)
            else:
                self.server = smtplib.SMTP(self.host, self.port)
        except Exception, e:
            print "Could not create connection %s" % e

    def sendNotification(self, fromaddr=config['mail_conf']['mail_from'],\
            toaddr=config['mail_conf']['mail_to'],\
            message, subj, interval=1):
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subj
        msg.attach(MIMEText(message, 'plain'))
        self.queue = []
        self.current_mes = ''
        try:
            if queue:
                if hash(self.current_mes) == hash(msg.as_string()):
                    self.current_mes = msg.as_string()
                else:
                    self.queue.append(self.current_mes)
                    self.server.sendmail(fromaddr, toaddr, msg.as_string())
                    self.server.close()
            else:
                self.server.sendmail(fromaddr, toaddr, msg.as_string())
        except Exception, e:
            print "Could not send mail %s" % e 
        finally:
            self.server.close()
