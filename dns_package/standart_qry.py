from struct import pack, unpack

from dns_package.pkg_work import PacketWorker


class StandartQuery:
    INTERNET_QUESTION_RESPONSE = 1
    DEFAULT_QUESTION_TYPE = 255

    def __init__(
            self,
            qname=None,
            qtype=DEFAULT_QUESTION_TYPE,
            qclass=INTERNET_QUESTION_RESPONSE):
        self.type = qtype
        self.qclass = qclass
        self.packer = PacketWorker()
        self.ptr = b""
        if qname != None:
            self.name = PacketWorker.pack(qname)

    def unpack(self, data, raw):
        self.name, data, self.ptr = self.packer.unpack(data, raw)
        self.type, self.qclass = unpack("!hh", data[:4])
        return data[4:]

    def pack(self):
        if self.ptr != b"":
            self.name = self.ptr
        return self.packer.pack(self.name) + pack("!hh", self.type, self.qclass)

    def __str__(self):
        return "QUEST: NAME:{} TYPE:{} CLASS:{}".format(
            self.name,
            self.type,
            self.qclass)
