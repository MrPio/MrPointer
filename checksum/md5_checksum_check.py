import base64
import hashlib
from checksum.checksum_check import ChecksumCheck


class MD5ChecksumCheck(ChecksumCheck):
    def check(self, msg: bytes, checksum: str) -> bool:
        my_base64 = base64.b64encode(msg)
        my_md5 = hashlib.md5(my_base64).hexdigest()
        return my_md5 == checksum
