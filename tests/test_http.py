from src.http import HTTPClient, HTTPServer


def test_httpclient_send_request():
    client = HTTPClient()
    request = client.send_request()

    lines = request.split("\n")
    assert len(lines) > 1
    start_line_pieces = lines[0].split(" ")
    assert len(start_line_pieces) > 1
    assert start_line_pieces[0] == "GET"


def test_httpclient_receive_response():
    client = HTTPClient()
    response = "a\nb\nc"
    client.receive_response(response)
    assert len(client.response_lines) == 3


def test_httpclient_process_response_on_200():
    client = HTTPClient()
    client.response_lines = [
        "HTTP/1.1 200 OK",
        "",
        "hello",
    ]
    assert client.process_response()
    assert client.get_html() == "hello"


def test_httpclient_process_response_on_404():
    client = HTTPClient()
    client.response_lines = [
        "HTTP/1.1 404 NOT FOUND",
    ]
    assert not client.process_response()



def test_httpserver_receive_request():
    server = HTTPServer()
    request = "a\nb\nc"
    server.receive_request(request)
    assert len(server.request_lines) == 3


def test_httpserver_process_request_get_1_1():
    server = HTTPServer()
    server.request_lines = [
         "GET / HTTP/1.1",
    ]
    assert server.process_request()


def test_httpserver_process_request_post_1_1():
    server = HTTPServer()
    server.request_lines = [
         "POST / HTTP/1.1",
    ]
    assert not server.process_request()


def test_httpserver_process_request_get_2():
    server = HTTPServer()
    server.request_lines = [
         "GET / HTTP/2",
    ]
    assert not server.process_request()


def test_httpserver_send_response():
    server = HTTPServer()
    server.content = "hello"
    response = server.send_response()
    assert response
    lines = response.split("\n")
    assert len(lines) > 1
    assert lines[-2] == "hello"
    assert lines[-1] == ""
