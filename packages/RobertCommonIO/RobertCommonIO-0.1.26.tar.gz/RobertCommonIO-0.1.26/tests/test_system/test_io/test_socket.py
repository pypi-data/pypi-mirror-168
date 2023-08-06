import time

from robertcommonio.system.io.socket import SocketType, SocketConfig, SocketAccessor, SocketHandler


def call_back(data):
    print(data)


def test_tcp_client():
    config = SocketConfig(MODE=SocketType.TCP_CLIENT, HOST='0.0.0.0', PORT=1000, CALL_BACK={})
    accessor = SocketAccessor(config)
    accessor.start()


def test_tcp_server():
    config = SocketConfig(MODE=SocketType.TCP_SERVER, HOST='0.0.0.0', PORT=9500)
    accessor = SocketAccessor(config)
    accessor.start(False)
    while True:
        time.sleep(1)


def test_s7_client():
    config = SocketConfig(MODE=SocketType.TCP_CLIENT, HOST='0.0.0.0', PORT=1000, CALL_BACK={})
    accessor = SocketAccessor(config)
    accessor.start()