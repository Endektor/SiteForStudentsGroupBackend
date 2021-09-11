from django.apps import AppConfig
from multiprocessing import Process
from time import sleep

from .mail_service import Service

import datetime
import os


class MailAppConfig(AppConfig):
    name = "mail_app"
    verbose_name = "Почта"

    @staticmethod
    def start_mail_service():
        while True:
            sleep(5)
            print("Mail check " + datetime.datetime.today().strftime("%H.%M.%S"), flush=True)
            service = Service()
            service.get_mails()
            sleep(60 * 5)

    def ready(self):
        mail_for_debug = False
        if os.environ.get("RUN_MAIN", None) != "true" and \
                not os.environ.get("Mail_env", None) == "true" and \
                mail_for_debug:
            # os.system('python manage.py celeryd -l INFO -B')
            p = Process(target=MailAppConfig.start_mail_service)
            p.start()
