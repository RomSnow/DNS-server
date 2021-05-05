# coding=utf-8
from struct import pack, unpack
from time import time

from dns_package.pkg_work import PacketWorker


class ResourceRecord():
    def __init__(
            self,
            all_info=None,
            owner_name=None,
            type=None,
            type_class=None,
            TTL=0):
        self.owner = owner_name
        self.type = type
        self.type_class = type_class
        self.TTL = TTL
        self.length_of_data = None
        self.data = None
        self.expected = int(time()) + TTL
        self.packer = PacketWorker()
        self.used = False
        self.oneOff = TTL == 0
        self.ptr = b""
        self.all_info = all_info

    def pack(self):
        data = b""
        if self.ptr != b"":
            self.owner = self.ptr
        data += self.packer.pack(self.owner) + pack("!h", self.type) \
                + pack("!h", self.type_class) + pack("!I", max(0, self.expected - int(time()))) + \
                pack("!H", self.length_of_data) + self.data
        return data

    def unpack(self, data, raw):
        (self.owner, data, self.ptr) = self.packer.unpack(data, raw)
        (self.type, self.type_class, self.TTL, self.length_of_data) = unpack("!hhiH", data[:10])
        self.oneOff = self.TTL == 0
        self.expected = int(time()) + self.TTL
        data = data[10:]
        self.data = data[:self.length_of_data]
        data = data[self.length_of_data:]
        self.all_info = data
        return data

    def __str__(self):
        return "Resource Record: OWNER:{} TYPE:{} CLASS:{} USED:{} EXPECT:{} LENGTH:{}".format(
            self.owner,
            self.type,
            self.type_class,
            self.used,
            self.expected,
            self.length_of_data)
