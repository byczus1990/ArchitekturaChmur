#!/usr/bin/env python3
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
 
        path = urlparse(self.path)
        params = parse_qs(path.query) 
        string_from_query = params.get('str', None)
        print("STRING PASSED AS QUERY:")
        print(string_from_query) 
        
        if path.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()

            if string_from_query:
                local_string = string_from_query[0]
                answer =  { "lowercase" : 0, "uppercase" : 0, "digits" : 0, "special" : 0}

                for i in range(len(local_string)):
                    if local_string[i].isupper():
                        answer["uppercase"] += 1
                    elif local_string[i].islower():
                        answer["lowercase"] += 1
                    elif local_string[i].isdigit():
                        answer["digits"] += 1
                    else:
                        answer["special"] += 1
            
                self.wfile.write(str.encode(json.dumps(answer)))

        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
