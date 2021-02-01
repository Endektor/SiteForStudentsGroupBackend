import datetime
import os
from time import sleep
from django.apps import AppConfig
from multiprocessing import Process

from .mail_service import Service


class MailAppConfig(AppConfig):
    name = 'mail_app'

    @staticmethod
    def start_mail_service():
        while True:
            print('Mail check ' + datetime.datetime.today().strftime("%H.%M.%S"), flush=True)
            service = Service()
            service.get_mails()
            sleep(60*5)

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true' and \
                not os.environ.get('Mail_env', None) == 'true':
            p = Process(target=MailAppConfig.start_mail_service)
            p.start()
