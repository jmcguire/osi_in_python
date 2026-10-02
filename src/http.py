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


def get_server_file(uri: str) -> str:
    if uri[-1] == "/":
        uri += "index.html"
    current_dir = Path(__file__).parent.parent
    file_path = current_dir / "static" / uri.lstrip("/")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def client_send_request() -> str:
    start_line = "GET / HTTP/1.1"
    headers = {
        "Host": "localhost",
    }

    envelope = create_envelope(start_line, headers)

    return f"{envelope}\n"


def server_receive_request(request: str) -> str:
    request_lines = request.split("\n")
    first_line = request_lines[0].split(" ")
    return get_server_file(first_line[1])


def server_send_response(content) -> str:
    start_line = "HTTP/1.1 200 OK"
    headers = {
        "Content-Type": "text/html",
        "Date": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "Content-Length": len(content),
    }

    envelope = create_envelope(start_line, headers)

    return f"{envelope}\n\n{content}\n"


def client_receive_response(request: str) -> str:
    lines = request.split("\n")

    i = 0
    while lines[i] != "":
        i += 1

    return "\n".join(lines[i+1:])
