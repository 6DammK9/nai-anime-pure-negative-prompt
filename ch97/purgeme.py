from telethon import TelegramClient
from telethon.tl.functions.channels import DeleteMessagesRequest

api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

phone = '+1234567890'
code = '12345'
session_file = 'delete_messages.session'

group_id = 12345
message_count = 100

client = TelegramClient(session_file, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, code)

messages = client.get_messages(group_id, limit=message_count)
message_ids = [msg.id for msg in messages]

client(DeleteMessagesRequest(group_id, message_ids))

client.disconnect()