from struct import pack, unpack


class HeaderQuery:
    def __init__(
            self,
            identification=None,
            flags=None,
            responses_count=0,
            answers_count=0,
            resources_count=0,
            optional_count=0):
        self.identification = identification
        self.flags = flags
        self.responses_count = responses_count
        self.answers_count = answers_count
        self.resources_count = resources_count
        self.optional_count = optional_count

    def unpack(self, header_information):
        (self.identification,
         self.flags,
         self.responses_count,
         self.answers_count,
         self.resources_count,
         self.optional_count) = unpack("!HHHHHH", header_information[:12])
        return header_information[12:]

    def pack(self):
        header_information = pack(
            "!HHHHHH",
            self.identification,
            self.flags,
            self.responses_count,
            self.answers_count,
            self.resources_count,
            self.optional_count)
        return header_information

    def __str__(self):
        return "Header: ID:{} FLAGS:{} NUM_OF_RESP:{} NUM_OF_ANS:{} NUM_OF_VALID:{} NUM_OF_OPT:{}".format(
            self.identification,
            self.flags,
            self.responses_count,
            self.answers_count,
            self.resources_count,
            self.optional_count)
