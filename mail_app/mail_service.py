from dateutil.parser import parse
from decouple import config
from email.header import decode_header
from itertools import product

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
        self.mailbox = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mailbox.login(config("EMAIL_HOST_USER"), config("EMAIL_HOST_PASSWORD"))
        self.mailbox.select(mailbox="Inbox", readonly=True)

        # Initializing django
        import os
        os.environ["Mail_env"] = "true"     # prevents creating several processes with service in debug mode
        from django.core.wsgi import get_wsgi_application
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_site.settings")
        get_wsgi_application()
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    def get_mails(self):
        latest_uid = self.get_latest_uid()
        previous_uid = self.get_previous_uid()
        uid_list = self.get_list_of_uid(latest_uid, previous_uid)
        if not uid_list:
            return 0
        letters = self.get_letters(uid_list)
        self.add_letters(letters)

    def get_latest_uid(self):
        """
        Returns uid of the last letter on email
        """
        result, data = self.mailbox.uid("search", None, "ALL")
        return int(data[0].split()[-1])

    @staticmethod
    def get_previous_uid():
        """
        Returns uid of the last uploaded letter
        """
        from django.db.models import Max
        from .models import Letter
        letter = Letter.objects.aggregate(Max('uid'))
        if letter["uid__max"]:
            return letter["uid__max"]
        else:
            return 0

    @staticmethod
    def get_list_of_uid(new_uid, old_uid):
        """
        Returns generator of uids it will upload
        """
        return [uid for uid in range(new_uid, old_uid, -1)]

    @staticmethod
    def get_header(letter, header_str):
        """
        Returns parsed and decoded part of the letter
        """
        header, encoding = decode_header(letter.get(header_str))[0]
        if isinstance(header, bytes) and encoding:
            header = header.decode(encoding)
        return header

    def get_letters(self, uids_list):
        """
        Returns a list of parsed letters
        """
        letters_list = []
        folder_name = "media/mail_attachments/"
        result, data = self.mailbox.uid("fetch", ",".join(map(str, uids_list)), "(RFC822)")

        for letter in data:
            if isinstance(letter, bytes):   # If letter is bytes, it is empty
                continue
            text = "Во время чтения сообщения произошла ошибка или тело письма пустое."
            attachments = []
            uid = letter[0].decode()
            letter = email.message_from_bytes(letter[1])

            uid = uid.split()[2]
            topic = self.get_header(letter, "Subject")
            mailer = self.get_header(letter, "From")
            date_time, qw = decode_header(letter.get("Date"))[0]
            date_time = parse(date_time)

            if letter.is_multipart():   # If it is multipart, it has attachment
                for part in letter.walk():
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        text = part.get_payload(decode=True).decode()
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
                text = letter.get_payload(decode=True).decode()

            letters_list.append({
                "uid": uid,
                "topic": topic,
                "mailer": mailer,
                "date_time": date_time,
                "attachments": attachments,
                "text": text,
            })
        return letters_list

    @staticmethod
    def add_letters(letters):
        """
        Adds letters to the database
        """
        from .models import Letter, Attachment

        for letter in letters:

            letter_obj = Letter(mailer=letter["mailer"],
                                topic=letter["topic"],
                                text=letter["text"],
                                date_time=letter["date_time"],
                                uid=letter["uid"])
            letter_obj.save()

            for filepath in letter["attachments"]:
                attachment = Attachment()
                attachment.file.name = filepath
                attachment.letter = letter_obj
                attachment.save()
