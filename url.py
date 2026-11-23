import socket
import ssl

class URL:
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        if "/" not in url:
            url = url + "/"
        self.host, path = url.split("/", 1)
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.path = "/" + path

    def conn_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_status = s.connect_ex((self.host, self.port))
        if conn_status == 0:
            if self.scheme == "https":
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=self.host)
            return s
        else:
            print("Error: Failed to establish TCP connection!")

    def send_request(self):
        s = self.conn_socket()

        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"
        request += f"\r\n"

        s.sendall(request.encode("utf8"))
        return s

    def recv_response(self):
        s = self.send_request()

        response = b""
        while True:
            data = s.recv(4096)
            if data == b"":
                break
            response += data

        s.close()
        return response

    def parse_response(self):
        response = self.recv_response()

        head, body = response.split(b"\r\n\r\n", 1)
        head = head.decode("utf8")
        body = body.decode("utf8")
        statusline = head.split("\r\n", 1)[0]
        headers = head.split("\r\n", 1)[1:]

        headers_dict = {}
        version, status_code, explanation = statusline.split(" ", 2)
        status_code = int(status_code)
        
        for item in headers:
            header, value = item.split(":", 1)
            headers_dict[header.casefold()] = value.strip()

        return {
            "version": version,
            "status_code": status_code,
            "explanation": explanation,
            "headers": headers_dict,
            "body": body
        }

    def extract_text(self):
        response = self.parse_response()
        body = response["body"]
        text = ""
        in_tag = False
   
        for char in body:
            if char == "<":
               in_tag = True
            elif char == ">":
               in_tag = False
            elif in_tag == False:
               text += char
       
        return text