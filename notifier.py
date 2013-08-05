'''
Base class for notification
'''
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

class notification(object):
    def __init__(self, host, port, name, password):
        self.host = host 
        self.port = port
        self.name = name
        self.password = password

    def sendNotification():
        pass
    
class mail_notification(notification):
    def __init__(self, host, port, name, password, usetls = True):
        super(mail_notification, self).__init__(host, port, name, password)
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

    def sendNotification(self, fromaddr, toaddr, message, subj):
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subj
        msg.attach(MIMEText(message, 'plain'))
        try:
            self.server.sendmail(fromaddr, toaddr, msg.as_string())
        except Exception, e:
            print "Could not send mail %s" % e 
        finally:
            self.server.close()
