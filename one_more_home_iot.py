import os
from socket import socket
from select import select
import ssl

from color_log.log_color import log_verbose, log_info, log_error, log_warning


def my_server():
    log_verbose("my_server()")
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(
        certfile="api_keys/alice.crt",
        keyfile="api_keys/alice.key")

    server = socket()
    server.bind(('192.168.43.62', 5001))
    server.listen(5)
    to_monitor = [server]

    while True:
        ready_to_read, ready_to_write, _ = select(to_monitor, to_monitor, [])
        # connstream = context.wrap_socket(ready_to_read, server_side=True)

        for sock in ready_to_read:
            if sock is server:
                client, addr = sock.accept()
                to_monitor.append(client)
                log_info('accept connect to ' + str(addr))
            else:
                try:
                    message = sock.recv(100)
                except Exception as ex:
                    log_error("Ex. with %s\n%s" % (sock, ex))
                    to_monitor.remove(sock)
                    continue

                if message == b'q':
                    sock.send(b'poka')
                    sock.close()
                    log_warning("remove %s" % sock)
                    to_monitor.remove(sock)
                    ready_to_read.remove(sock)
                elif message:
                    log_info("massage: %s" % message)

                    # ssl_text = connstream.read()
                    # log_info("ssl_text: %s" % ssl_text)

                    sock.send(b"OK from server")


def ping():
    log_verbose("ping()")

    host_name = "192.168.43.86"
    re = os.system("ping %s -c 1" % host_name)

    if not re:
        log_info("\tresponse: %s\n" % re)
    else:
        log_error("\tresponse NONE:\n %s" % re)


if __name__ == '__main__':
    # ping()

    my_server()

