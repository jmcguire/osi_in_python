from src.http import *

def main():
    LOG = "\033[35m"
    RESET = "\033[0m"

    request = client_send_request()
    print(f"{LOG}request:{RESET}\n{request}")

    content = server_receive_request(request)
    print(f"{LOG}content:{RESET}\n{content}")

    response = server_send_response(content)
    print(f"{LOG}response:{RESET}\n{response}")

    html = client_receive_response(response)
    print(f"{LOG}html:{RESET}\n{html}")


if __name__ == '__main__':
    main()
