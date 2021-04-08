from django.apps import AppConfig
from django.core.files.storage import FileSystemStorage

import datetime
import os
from time import sleep
from multiprocessing import Process

from .mail_service import Service


class MailAppConfig(AppConfig):
    name = 'mail_app'

    @staticmethod
    def start_mail_service():
        while True:
            print('Mail check ' + datetime.datetime.today().strftime("%H:%M:%S"), flush=True)
            service = Service()
            service.start()
            sleep(60 * 5)

    def ready(self):
        """
        Outdated method for mail check. Celery is used instead now.
        But it can be used for mail Service debug (if mail_for_debug = True)
        """
        mail_for_debug = True
        if os.environ.get('RUN_MAIN', None) != 'true' and \
                not os.environ.get('Mail_env', None) == 'true' and \
                mail_for_debug:
            p = Process(target=MailAppConfig.start_mail_service)
            p.start()
