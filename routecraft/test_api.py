import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from server import Handler

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def request(self,method,path,body=None):
        c=HTTPConnection(*self.server.server_address,timeout=5)
        c.request(method,path,body,{'Content-Type':'application/json'})
        r=c.getresponse();status=r.status;data=r.read();c.close()
        return status,data
    def test_valid_solve(self):
        status,data=self.request('POST','/solve',json.dumps({'points':[[0,0],[3,4]]}))
        self.assertEqual(status,200);self.assertEqual(json.loads(data)['optimised_length'],10)
    def test_invalid_payload(self):
        for payload in ['null','{}','{"points":[]}','not json']:
            status,_=self.request('POST','/solve',payload);self.assertEqual(status,400)
    def test_page_and_unknown_path(self):
        status,data=self.request('GET','/');self.assertEqual(status,200);self.assertIn(b'RouteCraft',data)
        self.assertEqual(self.request('GET','/missing')[0],404)
