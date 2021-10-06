from record import SessionLogger
import unittest
import socket
from config import *


class TestSession(unittest.TestCase):

    def setUp(self) -> None:
        self.counter = SessionLogger(server_address=MAIN_ADDRESS, alias="main_server")

    def test_count(self):
        i = self.counter.get_session(filter="")
        print("session number : ", len(i))  # -1: except for SessionLogger connection
        self.assertIsInstance(len(i), int)

    def test_my_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            my_ip = s.getsockname()[0]
        i = self.counter.get_session(filter=f"client_addr = '{my_ip}'")
        print("your session number : ", len(i))  # -1: except for SessionLogger connection
        self.assertIsInstance(len(i), int)


if __name__ == "__main__":

    unittest.main()