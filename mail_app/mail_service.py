import pickle
import ezgmail


class Service:
    def __init__(self):
        self.latest_letters = ezgmail.recent(maxResults=10)
        print(self.latest_letters)

        import os
        os.environ["Mail_env"] = 'true'
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_site.settings')
        application = get_wsgi_application()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

    def get_mails(self):
        from .models import Letter
        with open('mail_app/mail_data.json', 'rb') as data_file:
            downloaded_summary = pickle.load(data_file)

        for letter in self.latest_letters:
            letter = letter.messages[0]
            if ezgmail.summary(letter) == downloaded_summary:
                break
            else:
                Letter(mailer=letter.sender, topic=letter.subject, text=letter.body).save()
