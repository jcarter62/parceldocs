from cryptography.fernet import Fernet
import base64
from systemid import SystemId


class EncDec:

    def __init__(self):
        _systemid_key = SystemId().id().encode('ASCII')
        _key = base64.b64encode(_systemid_key)
        self._fernet = Fernet(_key)

    def encrypt(self, msg):
        return self._fernet.encrypt(msg.encode()).decode()

    def decrypt(self, msg):
        msg_bytes = msg.encode()
        return self._fernet.decrypt(msg_bytes).decode()


if __name__ == '__main__':
    ed = EncDec()
    msg = 'this is the message in clear text'
    encrypted = ed.encrypt(msg)
    decrypted = ed.decrypt(encrypted)
    print(encrypted)
    print(decrypted)


