import selectors
import socket
import time

from wgsi_server.http_parsed import BaseRequest
# from app import application

_weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def format_date_time(timestamp):
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    return "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
        _weekdayname[wd], day, _monthname[month], year, hh, mm, ss
    )

class WSGIServer(object):

    def __init__(self, host, port, application):
        self.app = application
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.address = (host, port)
        self.request_queue_size = 5
        self.open_socket()

    def accept(self, sock, mask):
        sel = self.selector
        conn, addr = sock.accept()
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def start_response(self, status, headers_list):
        r = 'HTTP/1.1 {}\r\n'.format(status)
        for h in headers_list:
            k = h[0]
            v = h[1]
            r += '{}: {}\r\n'.format(k, v)

        r += "Date: %s\r\n" % format_date_time(time.time())
        r += "Server: neudu-wsgi\r\n"

        r += '\r\n'

        self.response = r.encode()

    def write(self, sock, mask):
        # print("write")
        sel = self.selector

        # response_headers = "HTTP/1.1 200 OK\r\n"
        # response_headers += "\r\n"
        # response_body = "hello world"
        #
        # response = response_headers + response_body
        # print(response)
        # sock.send(response.encode("utf-8"))

        body = self.app(self.req.getenv(), self.start_response)

        for data in body:
            self.response += data

        resp = self.response
        sock.send(resp)

        sel.unregister(sock)
        sock.close()

    def read(self, conn, mask):
        sel = self.selector

        data = conn.recv(1000)
        if data:
            conn.setblocking(False)
            sel.unregister(conn)

            s = data.decode("utf-8")
            self.req = BaseRequest(s)

            sel.register(conn, selectors.EVENT_WRITE, self.write)
        else:
            # print("closing", conn)
            sel.unregister(conn)
            conn.close()

    def server_close(self):
        self.sock.close()
        self.selector.close()

    def server_bind(self):
        sock = self.sock

        sock.bind(self.address)
        self.server_address = sock.getsockname()

    def server_listen(self):
        self.sock.listen(self.request_queue_size)

    def open_socket(self):
        sock = self.sock
        self.server_bind()
        self.server_listen()
        sock.setblocking(False)

    def server_forever(self):
        sock = self.sock
        sel = self.selector

        sel.register(sock, selectors.EVENT_READ,self.accept)
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        finally:
            print("close")
            self.server_close()

# if __name__ == '__main__':
#     host = '127.0.0.1'
#     port = 8889
#     print('running http://{}:{}'.format(host, port))
#     httpd = WSGIServer(host, port)
#     httpd.serve_forever()