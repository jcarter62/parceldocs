import platform
import getmac
import hashlib

class SystemId:

    def __init__(self):
        sep = ' - '
        self._system_id = platform.system() + sep + platform.node() + sep + getmac.get_mac_address() + \
            sep + platform.machine() + sep + platform.processor()
        self._b_system_id = self._system_id.encode()
        self._md5 = hashlib.md5(self._b_system_id)
        return

    def id(self):
        return self._md5.hexdigest()


