from functools import reduce

from dns_package.header import HeaderQuery
from dns_package.standart_qry import StandartQuery
from dns_package.record import ResourceRecord


class DNSMessage:
    def __init__(
            self,
            header=HeaderQuery(),
            query=None,
            answers=None):
        self.header = header
        self.query = query
        self.answers = answers

    def pack(self):
        data = b""
        data += self.header.pack()
        data += reduce(lambda res, x: res + x.pack(), self.query, b"")
        data += reduce(lambda res, x: res + x.pack(), self.answers, b"")
        return data

    def unpack(self, data):
        raw = data
        data = self.header.unpack(data)
        self.query = []
        self.answers = []
        self.validation = []

        for index in range(self.header.responses_count):
            query = StandartQuery()
            data = query.unpack(data, raw)
            self.query.append(query)

        for index in range(self.header.answers_count):
            resource_record = ResourceRecord()
            data = resource_record.unpack(data, raw)
            self.answers.append(resource_record)

        for index in range(self.header.optional_count):
            resource_record = ResourceRecord()
            data = resource_record.unpack(data, raw)
            self.validation.append(resource_record)

        return data

    def __str__(self):
        res = "MESSAGE:\n"
        res += str(self.header)
        for q in self.query:
            res += '\n{}'.format(str(q))

        for i in self.answers:
            res += '\n{}'.format(str(i))
        return res
