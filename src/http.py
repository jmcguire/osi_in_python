from datetime import datetime, timezone
from pathlib import Path

def foo():
    return 23


def create_envelope(start_line: str, headers: dict) -> str:
    lines = []
    lines.append(start_line)
    for k,v in headers.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


class HTTPClient:
    def __init__(self):
        self.html: str = ""
        self.response: str = ""
        self.response_lines = []


    def send_request(self) -> str:
        start_line = "GET / HTTP/1.1"
        headers = {
            "Host": "localhost",
        }

        envelope = create_envelope(start_line, headers)

        return f"{envelope}\n"


    def receive_response(self, response: str):
        self.response = response
        self.response_lines = response.split("\n")


    def process_response(self) -> bool:
        if not self.__validate_code():
            return False
        self.__load_html()
        return True


    def __validate_code(self) -> bool:
        code = self.response_lines[0].split(" ")[1]
        if code != "200":
            return False
        return True


    def __load_html(self):
        i = 0
        while i < len(self.response_lines) and self.response_lines[i] != "":
            i += 1

        if i < len(self.response_lines):
            self.html = "\n".join(self.response_lines[i+1:])


    def get_html(self):
        return self.html


class HTTPServer:
    def __init__(self):
        self.file_dir = Path(__file__).parent.parent / "static"
        self.request: str = ""
        self.request_lines = []
        self.content: str = ""


    def receive_request(self, request: str):
        self.request = request
        self.request_lines = request.split("\n")


    def process_request(self) -> bool:
        first_line = self.request_lines[0].split(" ")
        self.content = self.__get_server_file(first_line[1])
        if not self.__validate():
            return False

        return True


    def send_response(self) -> str:
        start_line = "HTTP/1.1 200 OK"
        headers = {
            "Content-Type": "text/html",
            "Date": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "Content-Length": len(self.content),
        }

        envelope = create_envelope(start_line, headers)

        return f"{envelope}\n\n{self.content}\n"


    def __validate(self) -> bool:
        return self.__validate_action() and self.__validate_version()


    def __validate_version(self) -> bool:
        version = self.request_lines[0].split(" ")[2]
        if version == "HTTP/1.0" or version == "HTTP/1.1":
            return True
        return False


    def __validate_action(self) -> bool:
        action = self.request_lines[0].split(" ")[0]
        if action == "GET":
            return True
        return False


    def __get_server_file(self, uri: str) -> str:
        if uri[-1] == "/":
            uri += "index.html"
        file_path = self.file_dir / uri.lstrip("/")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

