# Derived from https://github.com/fleephub/fleep-api/blob/master/python-client/chatbot.py

import uuid
import base64
import time
from configparser import ConfigParser
from fleepclient.cache import FleepCache
from fleepclient.utils import convert_xml_to_text
import __init__ as init
from common.request import BackendConnection


log = init.getLogger(__name__)

config = ConfigParser()
config.read('../configuration.ini')
fleep = config['fleep']
username = fleep['user']
password = fleep['pass']
server = fleep['server']
chatid = fleep['chatid']

backend = config['backend']
url = backend['url'] + ':' + backend['port']

conn = BackendConnection(url)


def uuid_decode(b64uuid):
    ub = base64.urlsafe_b64decode(b64uuid + '==')
    uobj = uuid.UUID(bytes=ub)
    return str(uobj)


def process_message(chat, message):
    if message.mk_message_type != 'text':
        return

    chat.mark_read(message.message_nr)
    user_id = message.account_id
    message = convert_xml_to_text(message.message).strip()

    response = conn.get_response(message, user_id)

    if response is not None and  response[0] is not None:
        chat.message_send(str(response))


def main():
    log.info("Initializing bot")

    log.info('Login')
    fc = FleepCache(server, username, password)
    log.info('Loading contacts')
    log.info('convs: %d' % len(fc.conversations))

    chat_id = uuid_decode(chatid)
    chat = fc.conversations[chat_id]
    log.info('chat_id: %s' % chat_id)

    chat_msg_nr = chat.read_message_nr

    log.info("Bot initialized")
    while True:
        while True:
            msg = chat.get_next_message(chat_msg_nr)
            if not msg:
                break

            process_message(chat, msg)
            chat_msg_nr = msg.message_nr

        if not fc.poll():
            time.sleep(1)
            continue


if __name__ == '__main__':
    main()
