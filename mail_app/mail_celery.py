from celery import Celery

import datetime
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_site.settings')

app = Celery('mail_celery')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(120.0, test1.s(), name='1')


@app.task
def test1():
    from mail_app.mail_service import Service
    print('Mail check ' + datetime.datetime.today().strftime("%H.%M.%S"), flush=True)
    service = Service()
    service.get_mails()
