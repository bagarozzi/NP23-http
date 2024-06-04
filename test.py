import requests
import sys

SERVER_DEFAULT_PORT = 8080

port = SERVER_DEFAULT_PORT
if sys.argv[1:]:
    port = int(sys.argv[1:])

address = "http://localhost:" + str(port) + "/index.html"

print("Testing POST and GET requests to: ", address)

try:
    get_request = requests.get(address)
    post_request = requests.post(address)
    head_request = requests.head(address)
except requests.exceptions.Exception :
    print("Exception in making the test requests, make sure the server is running and has something to display")

print("POST REQUEST: ",
    "\n Status code: ", post_request.status_code,
)
print("HEAD REQUEST: ",
    "\n Status code: ", post_request.status_code,
)
print("GET REQUEST: ",
    "\n Status code: ", get_request.status_code,
    "\n Content: ", get_request.text
)   
