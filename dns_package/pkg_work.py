from struct import unpack


class PacketWorker:
    def __init__(self, data=None):
        self.data = data

    def pack(self, data=None):
        packet = b""
        if data != b'\xc0\x0c':
            if data is not None:
                domains = data.split(".")
            else:
                domains = self.data.split(".")

            for domain in domains:
                packet += str(chr(len(domain))).encode("utf-8")
                packet += domain.encode("utf-8")
            packet += str(chr(0)).encode("utf-8")
        else:
            packet += data

        return packet

    def unpack(self, data, raw):
        domain = ""
        while data[0] != 0:
            if data[0] & 192 == 192:
                offset = unpack("!H", data[:2])[0] & 16383
                data = data[2:]
                domain += self.unpack(raw[offset:], raw)[0]
                return domain, data, b"\xc0\x0c"
            else:
                count = data[0]
                for i in range(1, count + 1):
                    domain += chr(data[i])
                domain += '.'
                data = data[count + 1:]
        return domain[:-1], data[1:], b""
