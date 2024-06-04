import socketserver
import sys
import http.server
import signal
import os
import mimetypes

SERVER_DEFAULT_PORT = 8080

global server

# This class extends BaseHTTPRequestHandler and implements only the do_GET method
# as explained in the report
class GetRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        pathIsFound = False
        # Create path starting from resources directory inside the current working directory
        absolutePath = os.getcwd() + os.sep + "resources" + os.sep + self.path.replace("/", "")
        # Remove the queries
        absolutePath = absolutePath.split("?")[0]
        # If it's a directory then look for "index.html" or "index.htm" and return them 
        if os.path.isdir(absolutePath) : 
            if os.path.isdir(absolutePath) and "index.htm" in os.listdir(absolutePath):
                absolutePath = absolutePath + "index.htm"
                pathIsFound = True
            elif os.path.isdir(absolutePath) and "index.html" in os.listdir(absolutePath):
                absolutePath = absolutePath + "index.html"
                pathIsFound = True
        # If it's a file then return it
        elif os.path.isfile(absolutePath):
            pathIsFound = True
        
        # If the path is found then respond with 200 and send the file
        if pathIsFound :
            print("Path found: ", absolutePath)
            self.send_response(200)
            (mime_type, _) = mimetypes.guess_type(absolutePath)
            self.send_header('Content-Type', mime_type)
            self.end_headers()
            with open(absolutePath, "rb") as file:
                self.wfile.write(file.read())
            print("File \"", absolutePath, "\" was found and sent correctly (200)")
        # If the path is not found respond with 404
        else:
            self.send_error(404)
            print("Error 404: file \"", absolutePath, "\" not found")

# Define a method to handle the termination signal
def terminationSignalHandler(signal, frame):
    print("Exit sequence pressed, closing server")
    try:
        if (server):
            server.server_close()
    finally:
        print("Server closed correctly")
        exit(0)

def main():
    # If a port is specified then use it, otherwise use the default port
    port = SERVER_DEFAULT_PORT
    if sys.argv[1:]:
        port = int(sys.argv[1:])
    server_socket = ('localhost', port)

    # Bind the custom signal handler to the termination signal
    signal.signal(signal.SIGINT, terminationSignalHandler)

    try:
        # Start the server, allow for address reuse and enable daemon threads
        server = socketserver.ThreadingTCPServer(server_socket, GetRequestHandler)
        server.allow_reuse_address = True
        server.daemon_threads = True
        print("Server listening...")
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()