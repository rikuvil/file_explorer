import http.server
import socketserver
import os
import base64

# Set the directory you want to share
directory_to_share = "C:/Users/rikuv/Videos/"

# Set the port you want the server to listen on
port = 8020

# Set the username and password for basic authentication
username = "riku"
password = "viljanen"

# Create a custom handler to allow directory listing and add basic authentication
class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check for basic authentication
        if not self.authenticate():
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Secure Area"')
            self.end_headers()
            return

        # If authenticated, serve the requested file
        super().do_GET()

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            return False

        # Extract and decode the credentials from the Authorization header
        try:
            auth_type, auth_string = auth_header.split(' ', 1)
            if auth_type.lower() == 'basic':
                username_password = base64.b64decode(auth_string).decode("utf-8")
                username, password = username_password.split(':', 1)
                return username == "riku" and password == "viljanen"
        except Exception as e:
            pass

        return False

# Change the current working directory to the directory you want to share
os.chdir(directory_to_share)

# Create a socket server to listen on the specified port with the custom handler
with socketserver.TCPServer(("", port), AuthHandler) as httpd:
    print(f"Serving at port {port}")

    # Start the HTTP server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
