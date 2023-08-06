import json
import socketserver
import threading

from je_auto_control import execute_action


class TCPServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        command_data = self.request.recv(8192).strip()
        try:
            execute_str = json.loads(command_data)
            execute_action(execute_str)
        except Exception as error:
            print(repr(error))


class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def start_autocontrol_server():
    host, port = "localhost", 9938
    server = TCPServer((host, port), TCPServerHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server
