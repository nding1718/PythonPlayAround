This paragraph comes from "A Simple Web Server --- Greg Wilson" an article of the the book "500 lines or less"  

“”“
    Almost every program on web runs on a family of communication standards callecd Internet Protocol(IP) and we concern one of them (Transmission Control Protocol) TCP/IP.
    It makes communication between computers look like read and wrinting files

    Prorgrams using IP communicate through sockets. And each socket is one end of a point-to-point communication channel. A socket consists of an IP address that identifies a particular machine
    and a port number on that machine
”“”

import BaseHTTPServer
import os

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    class case_no_file(object):
        '''File or directory does not exist'''
        def test(self, handler):
            return not os.path.exists(handler.full_path)

        def act(self, handler):
            raise Exception("'{0}' not found".format(handler.path))

    class case_existing_file(object):
        '''File exist'''
        def test(self, handler):
            return os.path.isfile(handler.full_path)

        def act(self, handler):
            handler.handle_file(handle.full_path)

    class case_always_fail(object):
        '''Base case is nothing works'''
        def test(self, handler):
            return True

        def act(self, handler):
            raise Exception("Unknow ojbect '{0}'".format(handler.path))

    Cases = [case_no_file(), case_existing_file(), case_always_fail()]

    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    def do_GET(self):
        try:
            # figure out what exactly is being requested
            self.full_path = os.getcwd() + self.path

            for case in self.Cases:
                handler = case
                if handler.test(self):
                    handler.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' can not be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg = msg)
        self.send_content(content, 404)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Context-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)



if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
