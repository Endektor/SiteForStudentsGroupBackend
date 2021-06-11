import pickle
import ezgmail
from django.utils.timezone import make_aware

import imaplib
from decouple import config
import email

class Service:
    """
    Service for receiving messages from mailbox
    """
    def __init__(self):
        # Connection to mailbox
        self.mailbox = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mailbox.login(config('EMAIL_HOST_USER'), config('EMAIL_HOST_PASSWORD'))
        self.mailbox.select(mailbox='Inbox', readonly=True)

        # Initializing django
        import os
        os.environ["Mail_env"] = 'true'     # prevents creating several processes with service in debug mode
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_site.settings')
        application = get_wsgi_application()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

    def get_mails(self):
        latest_uid = self.get_latest_uid()
        print(latest_uid)
        uids_list = self.get_list_of_uids(latest_uid)
        letters = self.get_letters(uids_list)

    def get_latest_uid(self):
        result, data = self.mailbox.uid('search', None, "ALL")
        latest_email_uid = data[0].split()[-1]
        return latest_email_uid

    @staticmethod
    def get_list_of_uids(new_uid):
        with open('mail_app/mail_data.json', 'wb') as data_file:
            pickle.dump({'latest_uid': '607'}, data_file)
        with open('mail_app/mail_data.json', 'rb+') as data_file:
            data = pickle.load(data_file)
            pickle.dump({'latest_uid': str(new_uid)}, data_file)
        old_uid = int(data['latest_uid'])

        if int(new_uid) > old_uid:
            return [uid for uid in range(old_uid, int(new_uid) + 1)]
        return []

    def get_letters(self, uids_list):
        letters_list = []
        result, data = self.mailbox.uid('fetch', ','.join(map(str, uids_list)), '(RFC822)')
        email_message = email.message_from_string(data[0][0])
        print(email_message)
        # if data == [None]:
        #     return []
        # raw_email = data[0][1]
        # email_message = email.message_from_bytes(raw_email)
        # mailer = email.utils.parseaddr(email_message['From'])[1]
        # subject = email_message['Subject']
        # # письма на английском в правильной кодировке, на русском - в неправильной
        # eng_text = self.get_first_text_block(email_message)
        # # проверка на наличие русских символов, если он есть, сообщение декодируется
        # text = base64.b64decode(eng_text)
        # for letter in self.utf8_alphabet:
        #     if letter in text:
        #         text = text.decode('utf-8', 'ignore')
        #         break
        # else:
        #     text = eng_text
        #     # text = email_message.
        # # print(base64.b64decode(self.get_first_text_block(email_message)).decode('utf-8', 'ignore'))
        # if '=?UTF-8?B?' in subject:
        #     while '=?UTF-8?B?' in subject:
        #         subject = subject.replace('=?UTF-8?B?', '')
        #     subject = base64.b64decode(subject).decode('UTF-8')
        # letters_list.append({'mailer': mailer, 'topic': subject, 'text': text})
        # return letters_list

#         try:
#             with open('mail_app/mail_data.json', 'rb') as data_file:
#                 downloaded_summary = pickle.load(data_file)
#                 mail_data_exists = True
#         except FileNotFoundError:
#             downloaded_summary = None
#             mail_data_exists = False
#             self.latest_letters = ezgmail.search('in=inbox')
#
#             else:
#                 aware_datetime = make_aware(letter.timestamp)
#                 letter_obj = Letter(mailer=letter.sender,
#                                     topic=letter.subject,
#                                     text=letter.body,
#                                     date_time=aware_datetime)
#                 letter_obj.save()
#                 for file in letter.attachments:
#                     letter.downloadAttachment(file, downloadFolder='media/mail_attachments/')
#                     attachment = Attachment()
#                     attachment.file.name = 'media/mail_attachments/' + file
#                     attachment.letter = letter_obj
#                     attachment.save()
#
#         with open('mail_app/mail_data.json', 'wb') as data_file:
#             latest_letter_summary = ezgmail.summary(self.latest_letters[0], printInfo=False)
#             pickle.dump(latest_letter_summary, data_file)
