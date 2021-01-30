import datetime
import os
from time import sleep
from django.apps import AppConfig
from multiprocessing import Process

from .mail_service import Service


class MailAppConfig(AppConfig):
    name = 'mail_app'

    @staticmethod
    def start_mail_service():
        while True:
            print('Mail check ' + datetime.datetime.today().strftime("%H.%M.%S"), flush=True)
            service = Service()
            service.get_mails()
            sleep(60*5)

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true' and \
                not os.environ.get('Mail_env', None) == 'true':
            p = Process(target=MailAppConfig.start_mail_service)
            p.start()

    # @staticmethod
    # def test():
    #     import imaplib
    #     import email
    #     USERNAME = "v.nikolaev55555@gmail.com"
    #     PASSWORD = "kobudicqkwwxtgrk"
    #     imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    #     imap.login(USERNAME, PASSWORD)
    #     imap.select('INBOX')
    #     # if sender_of_interest:
    #     status, response = imap.uid('search', '453')
    #     # else:
    #     # status, response = imap.uid('search', None, 'UNSEEN')
    #     if status == 'OK':
    #         unread_msg_nums = response[0].split()
    #     else:
    #         unread_msg_nums = []
    #     data_list = []
    #     for e_id in unread_msg_nums:
    #         e_id = e_id.decode('utf-8')
    #         _, response = imap.uid('fetch', e_id, '(RFC822)')
    #         html = response[0][1].decode('utf-8')
    #         email_message = email.message_from_string(html)
    #         data_list.append(email_message.get_payload())
    #     for elem in data_list:
    #         print(elem)

    @staticmethod
    def test():
        import ezgmail
        # import json
        # USERNAME = "v.nikolaev55555@gmail.com"
        # PASSWORD = "kobudicqkwwxtgrk"
        # with open('token.json', 'w') as data_file:
        #     json.dump(USERNAME, data_file)
        # with open('credentials.json', 'w') as data_file:
        #     json.dump(PASSWORD, data_file)
        # ezgmail.init(tokenFile='token.json', credentialsFile='credentials.json')
        # ezgmail.init()

        letter = ezgmail.search("")[0].messages[0]
        print(letter.sender)
        print(letter.timestamp)
        print(letter.subject)
        print(letter.body)
        print(letter.attachments)
        print(ezgmail.summary(letter, printInfo=False))
        # with open('mail_app/mail_data.json', 'wb') as data_file:
        #     import pickle
        #     pickle.dump(ezgmail.summary(letter, printInfo=False), data_file)



        # print(ezgmail.LOGGED_IN)





    # @staticmethod
    # def test():
    #     import email
    #
    #     from imapclient import IMAPClient
    #
    #     HOST = "imap.gmail.com"
    #     USERNAME = "v.nikolaev55555@gmail.com"
    #     PASSWORD = "kobudicqkwwxtgrk"
    #
    #     with IMAPClient(HOST) as server:
    #         server.login(USERNAME, PASSWORD)
    #         server.select_folder("INBOX", readonly=True)
    #
    #         messages = server.search()
    #         for uid, message_data in server.fetch(messages, "RFC822").items():
    #             email_message = email.message_from_bytes(message_data[b"RFC822"])
    #             # print(uid, email_message.get("From"), email_message.get("Subject"))
    #             eng_text = MailAppConfig.get_first_text_block(email_message)
    #             import base64
    #             text = base64.b64decode(eng_text)
    #             utf8_alphabet = [b'\xd0\xb0', b'\xd0\xb1', b'\xd0\xb2', b'\xd0\xb3', b'\xd0\xb4', b'\xd0\xb5',
    #                              b'\xd1\x91',
    #                              b'\xd0\xb6', b'\xd0\xb7', b'\xd0\xb8', b'\xd0\xb9', b'\xd0\xba', b'\xd0\xbb',
    #                              b'\xd0\xbc',
    #                              b'\xd0\xbd', b'\xd0\xbe', b'\xd0\xbf', b'\xd1\x80', b'\xd1\x81', b'\xd1\x82',
    #                              b'\xd1\x83',
    #                              b'\xd1\x84', b'\xd1\x85', b'\xd1\x86', b'\xd1\x87', b'\xd1\x88', b'\xd1\x89',
    #                              b'\xd1\x8a',
    #                              b'\xd1\x8b', b'\xd1\x8c', b'\xd1\x8d', b'\xd1\x8e', b'\xd1\x8f', b'\xd0\x90',
    #                              b'\xd0\x91',
    #                              b'\xd0\x92', b'\xd0\x93', b'\xd0\x94', b'\xd0\x95', b'\xd0\x81', b'\xd0\x96',
    #                              b'\xd0\x97',
    #                              b'\xd0\x98', b'\xd0\x99', b'\xd0\x9a', b'\xd0\x9b', b'\xd0\x9c', b'\xd0\x9d',
    #                              b'\xd0\x9e',
    #                              b'\xd0\x9f', b'\xd0\xa0', b'\xd0\xa1', b'\xd0\xa2', b'\xd0\xa3', b'\xd0\xa4',
    #                              b'\xd0\xa5',
    #                              b'\xd0\xa6', b'\xd0\xa7', b'\xd0\xa8', b'\xd0\xa9', b'\xd0\xaa', b'\xd0\xab',
    #                              b'\xd0\xac',
    #                              b'\xd0\xad', b'\xd0\xae', b'\xd0\xaf']
    #             for letter in utf8_alphabet:
    #                 if letter in text:
    #                     text = text.decode('utf-8', 'ignore')
    #                     break
    #             else:
    #                 text = eng_text
    #             print(text)
    #
    # @staticmethod
    # def get_first_text_block(email_message_instance):
    #     maintype = email_message_instance.get_content_maintype()
    #     if maintype == 'multipart':
    #         for part in email_message_instance.get_payload():
    #             if part.get_content_maintype() == 'text':
    #                 return part.get_payload()
    #     elif maintype == 'text':
    #         return email_message_instance.get_payload()