from celery import Celery
import datetime

from .mail_service import Service


app = Celery('mail_celery')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test1.s(), name='1')


@app.task
def test1():
    print('Mail check ' + datetime.datetime.today().strftime("%H.%M.%S"), flush=True)
    service = Service()
    service.get_mails()
