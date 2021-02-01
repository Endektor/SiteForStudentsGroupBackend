import pickle
import ezgmail
from django.utils.timezone import make_aware


class Service:
    def __init__(self, amount_of_letters=10):
        self.latest_letters = ezgmail.recent(maxResults=amount_of_letters)

        import os
        os.environ["Mail_env"] = 'true'
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_site.settings')
        application = get_wsgi_application()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

    def get_mails(self):
        from .models import Letter, Attachment
        try:
            with open('mail_app/mail_data.json', 'rb') as data_file:
                downloaded_summary = pickle.load(data_file)
                mail_data_exists = True
        except FileNotFoundError:
            downloaded_summary = None
            mail_data_exists = False
            self.latest_letters = ezgmail.search('in=inbox')

        for letter in self.latest_letters:
            letter = letter.messages[0]
            if ezgmail.summary(letter, printInfo=False) == downloaded_summary and mail_data_exists:
                break
            else:
                aware_datetime = make_aware(letter.timestamp)
                letter_obj = Letter(mailer=letter.sender,
                                    topic=letter.subject,
                                    text=letter.body,
                                    date_time=aware_datetime)
                letter_obj.save()
                for file in letter.attachments:
                    letter.downloadAttachment(file, downloadFolder='media/mail_attachments/')
                    attachment = Attachment()
                    attachment.file.name = 'media/mail_attachments/' + file
                    attachment.letter = letter_obj
                    attachment.save()

        with open('mail_app/mail_data.json', 'wb') as data_file:
            latest_letter_summary = ezgmail.summary(self.latest_letters[0], printInfo=False)
            pickle.dump(latest_letter_summary, data_file)
