import socketserver
import sys
import http.server
import signal
import os
import mimetypes

SERVER_DEFAULT_PORT = 8080

global server

class GetRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        pathIsFound = False
        absolutePath = os.getcwd() + os.sep + "resources" + os.sep + self.path.replace("/", "")

        if os.path.isdir(absolutePath) : 
            if os.path.isdir(absolutePath) and "index.htm" in os.listdir(absolutePath):
                absolutePath = absolutePath + "index.htm"
                pathIsFound = True
            elif os.path.isdir(absolutePath) and "index.html" in os.listdir(absolutePath):
                absolutePath = absolutePath + "index.html"
                pathIsFound = True
        elif os.path.isfile(absolutePath):
            pathIsFound = True
            
        if pathIsFound :
            print("Path found: ", absolutePath)
            self.send_response(200)
            (mime_type, _) = mimetypes.guess_type(absolutePath)
            self.send_header('Content-Type', mime_type)
            self.end_headers()
            with open(absolutePath, "rb") as file:
                self.wfile.write(file.read())
            print("File \"", absolutePath, "\" was found and sent correctly (200)")
        else:
            self.send_error(404)
            print("Error 404: file \"", absolutePath, "\" not found")

def terminationSignalHandler():
    print("Exit sequence pressed, closing server")
    try:
        if (server):
            server.server_close()
    finally:
        print("Server closed correctly")
        exit(0)

def main():
    port = SERVER_DEFAULT_PORT
    if sys.argv[1:]:
        port = int(sys.argv[1:])
    server_socket = ('localhost', port)

    try:
        server = socketserver.ThreadingTCPServer(server_socket, GetRequestHandler)
        server.allow_reuse_address = True
        server.daemon_threads = True
        print("Server listening...")
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    http.server
    main()