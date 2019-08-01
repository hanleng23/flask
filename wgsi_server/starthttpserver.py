from wgsi_server.wgsi_server import WSGIServer
from app import application

if __name__ == "__main__":
    # host = '10.25.44.136'
    host = '127.0.0.1'
    port = 8889
    print("running http://{}:{}".format(host, port))
    httpd = WSGIServer(host, port, application)
    httpd.server_forever()