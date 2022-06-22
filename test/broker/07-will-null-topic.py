#!/usr/bin/env python3

import struct

from mosq_test_helper import *

def do_test(start_broker, proto_ver):
    rc = 1
    connect_packet = mosq_test.gen_connect("will-null-topic", will_topic="", will_payload=struct.pack("!4sB7s", b"will", 0, b"message"), proto_ver=proto_ver)

    port = mosq_test.get_port()
    broker = None
    if start_broker:
        broker = mosq_test.start_broker(filename=os.path.basename(__file__), port=port)

    try:
        sock = mosq_test.do_client_connect(connect_packet, b"", timeout=30, port=port)
        sock.close()
    except BrokenPipeError:
        rc = 0
    finally:
        if broker:
            broker.terminate()
            broker.wait()
            (stdo, stde) = broker.communicate()
            if rc:
                print(stde.decode('utf-8'))
                print("proto_ver=%d" % (proto_ver))
    return rc


def all_tests(start_broker=False):
    rc = do_test(start_broker, proto_ver=4)
    if rc:
        return rc
    rc = do_test(start_broker, proto_ver=5)
    if rc:
        return rc
    return 0

if __name__ == '__main__':
    sys.exit(all_tests(True))
