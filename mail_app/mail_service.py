import imaplib
import pickle
import email
import base64


class Service:
    def __init__(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login('v.nikolaev55555@gmail.com', 'kobudicqkwwxtgrk')
        self.mail.select('inbox')

        import os
        os.environ["Mail_env"] = 'true'
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_site.settings')
        application = get_wsgi_application()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

        # alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        # utf8_alphabet = [letter.encode('utf8') for letter in alphabet]
        # print(self.utf8_alphabet)
        self.utf8_alphabet = ['\xd0\xb0', '\xd0\xb1', '\xd0\xb2', '\xd0\xb3', '\xd0\xb4', '\xd0\xb5', '\xd1\x91',
                              '\xd0\xb6', '\xd0\xb7', '\xd0\xb8', '\xd0\xb9', '\xd0\xba', '\xd0\xbb', '\xd0\xbc',
                              '\xd0\xbd', '\xd0\xbe', '\xd0\xbf', '\xd1\x80', '\xd1\x81', '\xd1\x82', '\xd1\x83',
                              '\xd1\x84', '\xd1\x85', '\xd1\x86', '\xd1\x87', '\xd1\x88', '\xd1\x89', '\xd1\x8a',
                              '\xd1\x8b', '\xd1\x8c', '\xd1\x8d', '\xd1\x8e', '\xd1\x8f', '\xd0\x90', '\xd0\x91',
                              '\xd0\x92', '\xd0\x93', '\xd0\x94', '\xd0\x95', '\xd0\x81', '\xd0\x96', '\xd0\x97',
                              '\xd0\x98', '\xd0\x99', '\xd0\x9a', '\xd0\x9b', '\xd0\x9c', '\xd0\x9d', '\xd0\x9e',
                              '\xd0\x9f', '\xd0\xa0', '\xd0\xa1', '\xd0\xa2', '\xd0\xa3', '\xd0\xa4', '\xd0\xa5',
                              '\xd0\xa6', '\xd0\xa7', '\xd0\xa8', '\xd0\xa9', '\xd0\xaa', '\xd0\xab', '\xd0\xac',
                              '\xd0\xad', '\xd0\xae', '\xd0\xaf']
        self.utf8_alphabet = [b'\xd0\xb0', b'\xd0\xb1', b'\xd0\xb2', b'\xd0\xb3', b'\xd0\xb4', b'\xd0\xb5', b'\xd1\x91',
                              b'\xd0\xb6', b'\xd0\xb7', b'\xd0\xb8', b'\xd0\xb9', b'\xd0\xba', b'\xd0\xbb', b'\xd0\xbc',
                              b'\xd0\xbd', b'\xd0\xbe', b'\xd0\xbf', b'\xd1\x80', b'\xd1\x81', b'\xd1\x82', b'\xd1\x83',
                              b'\xd1\x84', b'\xd1\x85', b'\xd1\x86', b'\xd1\x87', b'\xd1\x88', b'\xd1\x89', b'\xd1\x8a',
                              b'\xd1\x8b', b'\xd1\x8c', b'\xd1\x8d', b'\xd1\x8e', b'\xd1\x8f', b'\xd0\x90', b'\xd0\x91',
                              b'\xd0\x92', b'\xd0\x93', b'\xd0\x94', b'\xd0\x95', b'\xd0\x81', b'\xd0\x96', b'\xd0\x97',
                              b'\xd0\x98', b'\xd0\x99', b'\xd0\x9a', b'\xd0\x9b', b'\xd0\x9c', b'\xd0\x9d', b'\xd0\x9e',
                              b'\xd0\x9f', b'\xd0\xa0', b'\xd0\xa1', b'\xd0\xa2', b'\xd0\xa3', b'\xd0\xa4', b'\xd0\xa5',
                              b'\xd0\xa6', b'\xd0\xa7', b'\xd0\xa8', b'\xd0\xa9', b'\xd0\xaa', b'\xd0\xab', b'\xd0\xac',
                              b'\xd0\xad', b'\xd0\xae', b'\xd0\xaf']

    def get_latest_uid(self):
        result, data = self.mail.uid('search', None, "ALL")
        latest_email_uid = data[0].split()[-1]
        return latest_email_uid

    @staticmethod
    def get_list_of_uids(latest_uid):
        # with open('mail_app/mail_data.json', 'wb') as data_file:
        #     pickle.dump({'latest_uid': '440'}, data_file)
        with open('mail_app/mail_data.json', 'rb') as data_file:
            data = pickle.load(data_file)
        uid = int(data['latest_uid'])
        with open('mail_app/mail_data.json', 'rb+') as data_file:
            pickle.dump({'latest_uid': str(latest_uid)}, data_file)
        if latest_uid > uid:
            return [uid_ for uid_ in range(uid, latest_uid + 1)]
        return []

    def get_letters(self, uids_list):
        letters_list = []
        for uid in uids_list:
            result, data = self.mail.uid('fetch', str(uid), '(RFC822)')
            if data != [None]:
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                mailer = email.utils.parseaddr(email_message['From'])[1]
                subject = email_message['Subject']
                # письма на английском в правильной кодировке, на русском - в неправильной
                eng_text = self.get_first_text_block(email_message)
                # проверка на наличие русских символов, если он есть, сообщение декодируется
                text = base64.b64decode(eng_text)
                for letter in self.utf8_alphabet:
                    if letter in text:
                        text = text.decode('utf-8', 'ignore')
                        break
                else:
                    text = eng_text
                    # text = email_message.
                # print(base64.b64decode(self.get_first_text_block(email_message)).decode('utf-8', 'ignore'))
                if '=?UTF-8?B?' in subject:
                    while '=?UTF-8?B?' in subject:
                        subject = subject.replace('=?UTF-8?B?', '')
                    subject = base64.b64decode(subject).decode('UTF-8')
                letters_list.append({'mailer': mailer, 'topic': subject, 'text': text})
        return letters_list

    @staticmethod
    def get_first_text_block(email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()

    def get_mails(self):
        latest_uid = int(self.get_latest_uid())
        uids_list = self.get_list_of_uids(latest_uid)
        letters = self.get_letters(uids_list)

        from .models import Letter
        for letter in letters:
            Letter(mailer=letter['mailer'], topic=letter['topic'], text=letter['text']).save()
