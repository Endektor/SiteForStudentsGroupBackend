from django.utils.timezone import make_aware
from django.core.files.storage import FileSystemStorage

import pickle
import ezgmail
from decouple import config
import pyAesCrypt


class Service:
    def __init__(self, amount_of_letters=10, group=None):
        self.group = group
        self.amount_of_letters = amount_of_letters

        import os
        os.environ['Mail_env'] = 'true'
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_site.settings')
        application = get_wsgi_application()
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

    @staticmethod
    def encrypt_file(file_name):
        buffer_size = 64 * 1024
        key = config('KEY')
        pyAesCrypt.encryptFile(file_name, file_name + '.aes', key, buffer_size)

    @staticmethod
    def decrypt_file(file_name):
        buffer_size = 64 * 1024
        key = config('KEY')
        pyAesCrypt.decryptFile(file_name + '.aes', file_name, key, buffer_size)

    def start(self):
        from custom_auth.models import Group
        if not self.group:
            groups = Group.objects.all()
        else:
            groups = (Group.objects.get(name=self.group),)
        for group in groups:
            folder = 'mail_app/group_files/' + group.name + '/'
            fs = FileSystemStorage(location=folder)

            if fs.exists('credentials.json.aes') and fs.exists('token.json.aes'):
                self.decrypt_file(folder + 'credentials.json')
                self.decrypt_file(folder + 'token.json')

                self.get_mails(folder, group)

            self.encrypt_file(folder + 'credentials.json')
            self.encrypt_file(folder + 'token.json')
            fs.delete('credentials.json')
            fs.delete('token.json')

    def get_mails(self, folder, group):
        ezgmail.init(tokenFile=folder + 'token.json',
                     credentialsFile=folder + 'credentials.json')
        latest_letters = ezgmail.recent(maxResults=self.amount_of_letters)
        from .models import Letter, Attachment
        try:
            with open(folder + 'mail_data.json', 'rb') as data_file:
                downloaded_summary = pickle.load(data_file)
                mail_data_exists = True
        except FileNotFoundError:
            downloaded_summary = None
            mail_data_exists = False
            latest_letters = ezgmail.search('in=inbox')

        for letter in latest_letters:
            letter = letter.messages[0]
            if ezgmail.summary(letter, printInfo=False) == downloaded_summary and mail_data_exists:
                break
            else:
                aware_datetime = make_aware(letter.timestamp)
                letter_obj = Letter(mailer=letter.sender,
                                    topic=letter.subject,
                                    text=letter.body,
                                    date_time=aware_datetime,
                                    group=group)
                letter_obj.save()
                for file in letter.attachments:
                    letter.downloadAttachment(file, downloadFolder='media/mail_attachments/' + group.name + '/')
                    attachment = Attachment(group=group)
                    attachment.file.name = 'media/mail_attachments/' + group.name + '/' + file
                    attachment.letter_attachment = letter_obj
                    attachment.save()

        with open(folder + '/mail_data.json', 'wb') as data_file:
            latest_letter_summary = ezgmail.summary(latest_letters[0], printInfo=False)
            pickle.dump(latest_letter_summary, data_file)
