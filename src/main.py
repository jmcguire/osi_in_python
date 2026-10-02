from src.http import *

def main():
    LOG = "\033[35m"
    RESET = "\033[0m"

    client = HTTPClient()
    server = HTTPServer()

    request = client.send_request()
    print(f"{LOG}request:{RESET}\n{request}")

    server.receive_request(request)
    if server.process_request():
        print(f"{LOG}process_request:{RESET} success")
    else:
        print(f"{LOG}process_request:{RESET} fail")
        return

    response = server.send_response()
    print(f"{LOG}response:{RESET}\n{response}")

    client.receive_response(response)
    if client.process_response():
        print(f"{LOG}process_response:{RESET} success")
    else:
        print(f"{LOG}process_response:{RESET} fail")

    html = client.get_html()

    print(f"{LOG}html:{RESET}\n{html}")


if __name__ == '__main__':
    main()
