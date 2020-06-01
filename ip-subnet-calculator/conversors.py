import re


class SubnetCalc:
    def __init__(self, address, cidr=None, net=None, wildcard=None):
        self.address = address
        self.cidr = cidr
        self.cidr_remainder = 32 - cidr
        self.net = net
        self.wildcard = wildcard
        self.hosts_number = self.calc_hosts(self.calc(net=0, wildcard=1))
        self.hosts_number = self.hosts_number - 2 if self.hosts_number >= 2 else self.hosts_number
        self.network = self.calc2(y='0', z='0')
        self.broadcast = self.calc2(y='1')
        self.hostmin = self.calc2(y='0', z='1')
        self.hostmax = self.calc2(y='1', z='0')

    @property
    def address(self):
        return self._address

    @property
    def net(self):
        return self._net

    @property
    def wildcard(self):
        return self._wildcard

    @property
    def cidr(self):
        return self._cidr

    @address.setter
    def address(self, value):
        if not self.address_validator(value):
            raise ValueError('Invalid Address')
        self._address = value

    @net.setter
    def net(self, value):
        if value:
            self._net = value
            return
        else:
            self._net = self.octets_converter(self.calc(net=1, wildcard=0))
            return

    @wildcard.setter
    def wildcard(self, value):
        if value:
            self._wildcard = value
            return
        else:
            self._wildcard = self.octets_converter(self.calc(net=0, wildcard=1))
            return

    @cidr.setter
    def cidr(self, value):
        if value <= 0 or value > 32:
            raise ValueError('Invalid CIDR')
        else:
            self._cidr = value

    @staticmethod
    def decimal_to_binary(value):
        converted = ''
        x = 128
        for i in range(8):
            if value >= x:
                converted += '1'
                value -= x
            else:
                converted += '0'
            x /= 2
        return converted

    @staticmethod
    def binary_to_decimal(value):
        x = ''
        y = 128
        value = str(value)
        converted = 0
        for i in range(8 - len(value)):
            x += '0'
        x += value
        for i in range(8):
            if x[i] == '1':
                converted += y
            y /= 2
        return int(converted)

    @staticmethod
    def address_validator(address):
        regexp = re.compile(r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$')
        if regexp.search(address):
            return True

    @staticmethod
    def calc_hosts(value):
        value = list(value)
        converted = 1
        for i in value:
            if i == '1':
                converted *= 2
        return converted

    def calc(self, net=0, wildcard=0):
        value = []
        for i in range(self.cidr):
            value.append(net)
        for i in range(self.cidr_remainder):
            value.append(wildcard)
        value = ''.join(str(i) for i in value)
        return value

    def calc2(self, y='0', z='1'):
        x = self.address.split('.')
        converted = []
        for i in range(4):
            converted.append(self.decimal_to_binary(int(x[i])))
        converted = ''.join(str(i) for i in converted)
        converted = converted[:self.cidr]
        for i in range(self.cidr_remainder - 1):
            converted += y
        converted += z
        return self.octets_converter(converted)

    def octets_converter(self, value):
        x = 0
        y = 8
        converted = []
        for i in range(4):
            converted.append(self.binary_to_decimal(value[x:y]))
            x += 8
            y += 8
        converted = '.'.join(str(i) for i in converted)
        return converted
