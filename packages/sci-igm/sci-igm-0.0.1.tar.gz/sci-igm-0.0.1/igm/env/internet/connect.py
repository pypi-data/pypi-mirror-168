import socket
import time
from typing import Tuple, Optional

CONNECT_TIMEOUT = 1


def try_connect(host, port: int, timeout: float = CONNECT_TIMEOUT) -> Tuple[bool, Optional[float]]:
    """
    Overview:
        Connection function for given host ip and port.

        Based on `How can I see if there's an available and active internet connection in Python? <https://stackoverflow.com/a/33117579/6995899>`_.

    :param host: Host address.
    :param port: Port.
    :param timeout: Timeout of this connection, default is ``1``.
    """
    _default_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(timeout)
        session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            _start_time = time.time()
            session.connect((host, port))
            _end_time = time.time()
        finally:
            session.close()

        return True, _end_time - _start_time
    except socket.error:
        return False, None
    finally:
        socket.setdefaulttimeout(_default_timeout)
