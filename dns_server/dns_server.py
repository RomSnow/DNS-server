import asyncio

from dns_server.dns_struct import DNS


class DNSServer(asyncio.Protocol):
    def __init__(self, transport=None):
        self.transport = transport

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        dns = DNS()
        answer = dns.get_addr(data)
        while answer is None:
            answer = dns.get_addr(data)
        self.transport.sendto(answer, addr)
