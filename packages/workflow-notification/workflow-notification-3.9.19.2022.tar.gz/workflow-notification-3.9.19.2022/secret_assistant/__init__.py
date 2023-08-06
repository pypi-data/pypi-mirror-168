import os
import yaml
import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def config(getFile):
    if(not os.path.isfile(getFile)):
        print(f"{UNDERLINE} - see https://github.com/Nllii/workflow-notification/blob/main/README.md - {ENDC}")
        return None
    try:
        if getFile:
            config = yaml.safe_load(open(getFile))
            for information in config:
                if information == 'notifications':
                    return config[information]
    except Exception as e:
        print(f"error: {e}")
        return False



class notification:
    # using the logger module... is just too complicated.
    def __init__(self,message=None,file=None):
        self.message = message
        self.config = file if  file != None else config('dev.notification.yaml')
        if self.config is None or False:
              print(f"{FAIL} - configfile returned {self.config}... please check your path and make sure the keys and values are as expected. {ENDC}")


    def send_mail(self):
        msg = MIMEMultipart()
        msg['From'] = self.config[1]['email']['from']
        msg['To'] = self.config[1]['email']['to']
        msg['Subject'] = self.config[1]['email']['subject']
        message = str(''.join(self.message))
        msg.attach(MIMEText(message))

        mailserver = smtplib.SMTP(self.config[1]['email']['smtp_host'], self.config[1]['email']['smtp_port'])
        # identify ourselves
        mailserver.ehlo()
        # secure our email with tls encryption
        if self.config[1]['email']['smtp_tls']:
            mailserver.starttls()
            mailserver.ehlo()

            # mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.login(self.config[1]['email']['smtp_username'], self.config[1]['email']['smtp_password'])
        mailserver.sendmail(self.config[1]['email']['from'],self.config[1]['email']['to'], msg.as_bytes())
        mailserver.quit()
        return self



    def sendmessage(self):
        if self.config is None or False:
            return False
        data = {
            'text': self.message,
            'bot_id': self.config[0]['groupme']['bot_id']

        }
        info = json.dumps(data)
        response = requests.post('https://api.groupme.com/v3/bots/post', data=info)
        if response.status_code == 202:
            pass

        else:
            #TODO, handle error and send email when groupme is down or errors.
            print(response.text)
        return self


    def _reply(self):
        print(f"configfile returned {self.config}... please check your path and make sure the keys and valus are as expected.")
        # return self

    def info(self):
        print(f"{BOLD}{self.message}{ENDC}")
        return self

    def warning(self):
        print(f"{WARNING}{self.message}{ENDC}")
        return self


    def critical(self):
        print(f"{FAIL}{self.message}{ENDC}")
        return self

    # def logtraceback(self):
    #     print(f"{FAIL}{traceback.format_exc()}{ENDC}")
    #     return self



