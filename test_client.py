from client import incoming_message, outgoing_message
import unittest
import json


class TestClient(unittest.TestCase):
    def test_incoming_message(self):
        self.assertEqual(incoming_message(b'"\\u0442\\u0435\\u0441\\u0442"'), 'тест')

    def test_outgoing_message(self):
        res = outgoing_message()
        tm = json.loads(res.decode('utf-8'))['time']
        st = f'"action": "presence", "time": {tm}'
        st = '{'+st+'}'
        self.assertEqual(res, bytes(st.encode('utf-8')))


if __name__ == '__main__':
    unittest.main()
