import os
from socket import socket
from select import select
import ssl
import json

from color_log.log_color import log_verbose, log_info, log_error, log_warning


def my_server():
    log_verbose("my_server()")
    # context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # context.load_cert_chain(
    #     certfile="api_keys/alice.crt",
    #     keyfile="api_keys/alice.key")

    server = socket()
    server.bind(('192.168.0.102', 5001))
    server.listen(5)
    to_monitor = [server]

    s = ''

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
                    message = sock.recv(254)
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

                    log_info("full massage.e: %s" % s)
                    json_esp32 = json.loads(s)
                    log_info("\tj1: %s" % json_esp32['sensor'])
                    log_info("\tj2: %s" % json_esp32['time'])
                    log_info("\tj3: %s" % json_esp32['temp'])
                    log_info("\tj4: %s" % json_esp32['hum'])
                    log_info("\tj5: %s" % json_esp32['air'])
                    log_info("\tj6: %s" % json_esp32['pres'])

                    s = ''
                elif message:
                    log_info("\tmassage: %s (%s)" % (message, type(message)))
                    # log_info("massage.e: %s" % message.decode())

                    s += message.decode()



                    # ssl_text = connstream.read()
                    # log_info("ssl_text: %s" % ssl_text)

                    sock.send(b"OK from RPi server")


def ping():
    log_verbose("ping()")

    host_name = "192.168.0.28"
    re = os.system("ping %s -c 1" % host_name)

    if not re:
        log_info("\tresponse: %s\n" % re)
    else:
        log_error("\tresponse NONE:\n %s" % re)


if __name__ == '__main__':
    # ping()

    my_server()
