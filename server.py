import argparse
import pickle
from dns_server.dns_errors import DNSError
from dns_server.dns_server import *


def get_args():
    parser = argparse.ArgumentParser(description="DNS server")
    parser.add_argument(
        "--master",
        default="8.8.4.4",
        help="Master Server IP address (default: Open Google sever)")
    parser.add_argument(
        "--ttl",
        help="Time to life data in cache",
        default=3600, type=int)
    parser.add_argument(
        "--address",
        help="Address of this DNS server",
        default='127.0.0.1'
    )
    return parser.parse_args()


def main(arg):
    try:
        cache = pickle.load(open('dump', 'rb'))
    except FileNotFoundError:
        cache = {}
    dns = DNS(arg.master, arg.ttl, cache)
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(
        DNSServer, local_addr=(arg.address, 53))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except DNSError as e:
        print(e)
    except KeyboardInterrupt:
        pickle.dump(dns.cache, open('dump', 'wb'))

    transport.close()
    loop.close()


if __name__ == "__main__":
    args = get_args()
    main(args)
