import datetime
import hashlib
import random
import json


class FirewallHeader:
    def __init__(self):
        super().__init__()
    # Represents a strategy for generating a header that identifies Serato applications to the firewall. This header
    # should be non-trivial to guess by outsiders (unless they find this repository). If we wanted to make this header
    # harder to guess, we could introduce an environment variable that isn't present in the source code.

    # The values by which ordinal values of the ASCII characters in each 8-character chunk of the md5 hash will be
    # shifted

    SHIFTS = [-8, 8, -16, 16]

    # In another effort to make the header less guessable by people curious enough to make requests to our test servers
    # (but not curious enough to look at this open source code), add a prefix with characters drawn from a specific set
    # to the header

    PREFIX_CHARACTERS = 'serato'

    def getHeader(self):
        return {self.getHeaderKey(): self.getHeaderHash()}

    def getHeaderKey(self):
        return "x-serato-firewall"

    # Regular expression pattern that will match valid firewall header lines
    # Example match: "ras~/[Y*(0*Y9j:Ak8k9)T!Q )')@tFB@BDs"

    # HEADER_PATTERN = '/"[serato]{3}~[\x28-\x31\x59-\x5B\x5D\x5E\x79]{8}[\x38-\x41\x69-\x6E]{8}[\x20-\x21\x23-\x29\x51-\x56\x78]{8}[\x40-\x49\x71-\x76]{8}"/'; # nopep8

    # Returns a header value consisting of:
    # 1. A 3 character prefix drawn from characters in the PREFIX_CHARACTERS string with no repeats, and
    # 2. A hash, with every 8 ASCII character chunk shifted by the offsets defined in the SHIFTS array
    # - separated by a ~ character.
    # @return string Header value, for example "rta~Y[)(/*\,:ijkk>k:S!#R((U$tGvuIstE"

    def getHeaderHash(self):
        # @var string Date/time at which this header was created (used to create the hash)
        timeStamp = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)").encode('utf-8')
        # @var string Three letter prefix for the firewall header, from the set of PREFIX_CHARACTERS letters
        prefix = ''.join(random.choice(self.PREFIX_CHARACTERS) for i in range(3))

        g_hash = hashlib.md5(timeStamp).hexdigest()
        shiftedHash = ""
        for i in range(0, 4):
            shiftedHash += self.shiftChunk(g_hash[i*8:i*8+8], self.SHIFTS[i])

        shiftedHash = self.replaceInvalidCharacters(shiftedHash)

        header = '\"' + prefix + '~' + shiftedHash + '\"'
        return header

    def shiftChunk(self, chunk, shift_num):
        shiftedChunk = ""
        for i in range(0, len(chunk)):
            shiftedChunk += self.shiftCharacter(chunk[i], shift_num)

        return shiftedChunk

    def shiftCharacter(self, character, shift_num):
        return chr(ord(character) + shift_num)

    # Characters to replace (and what to replace them with) in the header, since they'd be invalid in a quoted string
    # under RFC 2616 or RFC 7230

    def replaceInvalidCharacters(self, header):
        header = header.replace('\"', 'x')
        header = header.replace('\\', 'y')
        return header
