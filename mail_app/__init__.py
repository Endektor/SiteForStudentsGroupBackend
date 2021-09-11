default_app_config = 'mail_app.apps.MailAppConfig'
from .mail_celery import app as mail_celery
__all__ = ('mail_celery',)