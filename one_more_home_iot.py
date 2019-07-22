import json
import os
from socket import socket
from sqlite3 import connect

from select import select

from color_log.log_color import log_verbose, log_info, log_error, log_warning


def my_server():
    log_verbose("my_server()")

    # try:
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
                log_info('\taccept connect to ' + str(addr))
            else:
                try:
                    message = sock.recv(254)
                except Exception as ex:
                    log_error("\tEx. with %s\n%s" % (sock, ex))
                    to_monitor.remove(sock)
                    continue

                if message == b'q':
                    sock.send(b'poka')
                    sock.close()
                    # log_warning("\tremove %s" % sock)
                    to_monitor.remove(sock)
                    ready_to_read.remove(sock)

                    # log_info("\tfull massage.e: %s" % s)
                    json_iot = json.loads(s)
                    s = ''

                    iot_data = [json_iot['sensor'], json_iot['time'], json_iot['temp'], json_iot['hum'],
                                json_iot['air'], json_iot['pres']]

                    log_info('\tiot_data: %s' % iot_data)
                    save_iot_data_to_db(iot_data)

                elif message:
                    # log_info("\tmassage: %s (%s)" % (message, type(message)))
                    s += message.decode()
                    # ssl_text = connstream.read()
                    # log_info("ssl_text: %s" % ssl_text)
                    sock.send(b"OK from RPi server")
    # except Exception as ex:
    #     log_error("\tEx. in my_server()\n%s" % ex)


def save_iot_data_to_db(_json_iot):
    log_verbose("save_iot_data_to_db()")

    # db = get_db()
    db = connect("data/flask_test.sqlite")
    cur = db.cursor()

    iot_names = cur.execute('SELECT iot_name FROM home_iot').fetchall()  # list of tuples
    iot_names = [i[0] for i in iot_names]  # Before: iot_names: [('esp32',), ('esp8266',)];
    log_warning("iot_names: %s" % iot_names)  # After: iot_names: ['esp32', 'esp8266']

    if _json_iot[0] in iot_names:

        cur.execute(f"INSERT INTO {_json_iot[0]}"
                    f" (created, temp, hum, air, pess)"
                    f" VALUES (?, ?, ?, ?, ?)",
                    _json_iot[1:])

        db.commit()
        log_info("\tINSERT iot data - OK")
    else:
        log_error("\tEr. in save_iot_data_to_db\nno satch name in DB")

    # close_db()
    db.close()
    log_verbose("save_iot_data_to_db() - EXIT")


def ping(address):
    log_verbose("ping()")

    host_name = str(address)
    re = os.system("ping %s -c 1" % host_name)

    if not re:
        log_info("\tresponse:\n%s" % re)
    else:
        log_error("\tresponse NONE:\n%s" % re)


if __name__ == '__main__':
    # ping()

    my_server()
