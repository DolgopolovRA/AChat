from server import incoming_message, outgoing_message
import unittest
import json


class TestServer(unittest.TestCase):

    def test_incoming_message_ok(self):
        msg = {'action': 'presence', 'time': 123123123}
        res = incoming_message(json.dumps(msg).encode('utf-8'))[1]
        self.assertEqual(res['responce'], 200)

    def test_incoming_message_failed(self):
        msg = {'action': 'iii', 'time': 123123123}
        res = incoming_message(json.dumps(msg).encode('utf-8'))[1]
        self.assertEqual(res['responce'], 400)

    def test_outgoing_message(self):
        answer = {'responce': 200, 'time': 123123123}
        self.assertEqual(outgoing_message(answer), json.dumps(answer).encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
