from dateutil.parser import parse
from decouple import config
from email.header import decode_header

import email
import imaplib
import os
import pickle


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
        dumped_uid = self.get_previous_uid()
        uid_list = self.get_list_of_uid(latest_uid, dumped_uid)
        letters = self.get_letters(uid_list)
        self.uid_dump(latest_uid)

    def get_latest_uid(self):
        result, data = self.mailbox.uid('search', None, "ALL")
        return int(data[0].split()[-1])

    @staticmethod
    def get_previous_uid():
        try:
            with open('mail_app/mail_data.json', 'rb') as data_file:
                data = pickle.load(data_file)
            return int(data['latest_uid'])

        except FileNotFoundError:
            # with open('mail_app/mail_data.json', 'wb') as data_file:
            #     pickle.dump({'latest_uid': '607'}, data_file)
            return 0    # Returns zero as the first uid

    @staticmethod
    def uid_dump(new_uid):
        with open('mail_app/mail_data.json', 'wb+') as data_file:
            pickle.dump({'latest_uid': str(new_uid)}, data_file)

    @staticmethod
    def get_list_of_uid(new_uid, old_uid):
        return [uid for uid in range(new_uid, old_uid, -1)]

    def get_letters(self, uids_list):
        letters_list = []
        # result, data = self.mailbox.uid('fetch', ','.join(map(str, uids_list)), '(RFC822)')
        result, data = self.mailbox.uid('fetch', '620', '(RFC822)')
        uid = 620
        email_message = email.message_from_bytes(data[0][1], _class=email.message.EmailMessage)

        msg = email.message_from_bytes(data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding)
        sender, encoding = decode_header(msg.get("From"))[0]
        if isinstance(sender, bytes) and encoding:
            sender = sender.decode(encoding)
        date_time, qw = decode_header(msg.get("Date"))[0]
        date_time = parse(date_time)


        body = "Во время чтения сообщения произошла ошибка или тело письма пустое."


        folder_name = "media/mail_attachments/"
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass

                if "attachment" in content_disposition:
                    filename, encoding = decode_header(part.get_filename())[0]
                    if isinstance(filename, bytes) and encoding:
                        filename = filename.decode(encoding)
                    filepath = os.path.join(folder_name, filename)
                    attachments.append(filepath)
                    open(filepath, "wb").write(part.get_payload(decode=True))
        else:
            body = msg.get_payload(decode=True).decode()

        from .models import Letter, Attachment

        letter_obj = Letter(mailer=sender,
                            topic=subject,
                            text=body,
                            date_time=date_time,
                            uid=uid)
        letter_obj.save()

        for filepath in attachments:
            attachment = Attachment()
            attachment.file.name = filepath
            attachment.letter = letter_obj
            attachment.save()

        # if email_message.is_multipart():
        #     for payload in email_message.get_payload():
        #         body = payload.get_payload(decode=True).decode('utf-8')
        #         print(body)
        # else:
        #     body = email_message.get_payload(decode=True).decode('utf-8')
        #     print(body)
        # print(email_message.items())
        # print(email.utils.getaddresses(email_message))
        #
        # print(email.utils.parseaddr(email_message['From']))
        #
        # print(email_message.items())
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
