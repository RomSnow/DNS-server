import datetime
from socket import *

from dns_package.dns_msg import DNSMessage
from dns_package.header import HeaderQuery


class Singleton(type):
    """Суперкласс, для создание singleton классов"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DNS(object, metaclass=Singleton):
    def __init__(self, forwarder, ttl, cache):
        self.cache = cache
        self.forwarder = forwarder
        self.err_count = 0
        self.ttl = ttl

    def get_addr(self, packet):
        dns_msg = DNSMessage()
        dns_msg.unpack(packet)

        for question in dns_msg.query:
            if question.name in self.cache.keys():
                answer, timestamp = self.cache[question.name]
                now = datetime.datetime.now()
                age = now - timestamp
                if age.seconds > self.ttl:
                    print('Record is too old, get new data')
                    return self._get_addr(question, dns_msg)
                else:
                    print(f'Record "{question.name}" found in cache')
                    return answer.pack()
            else:
                print(f'Record "{question.name}" is not found')
                return self._get_addr(question, dns_msg)

    def _get_addr(self, question, dns_msg):
        ID = dns_msg.header.identification
        flags = dns_msg.header.flags
        validation = dns_msg.validation
        header = HeaderQuery(
            identification=ID,
            flags=flags,
            responses_count=1,
            answers_count=0,
            resources_count=0,
            optional_count=0)
        msg = DNSMessage(header, [question], [])

        try:
            with socket(AF_INET, SOCK_DGRAM) as new_socket:
                new_socket.settimeout(1)
                new_socket.sendto(msg.pack(), (self.forwarder, 53))
                data, addr = new_socket.recvfrom(1024)

            answer = DNSMessage()
            answer.unpack(data)
            self.cache[question.name] = (
                answer, datetime.datetime.now())
            print(f'Receiving "{question.name}"')
            return data
        except timeout:
            print('DNS server is not reached')
