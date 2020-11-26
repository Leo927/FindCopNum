import constant
import copy


class SV:
    def __init__(self, s, v):
        self.s = s
        self.v = v

    def __eq__(self, other):
        return (type(other) == SV and self.s == other.s and self.v == other.v)

    def __str__(self):
        return f'({self.s}, {self.v})'

    def __repr__(self):
        return str(self)

    @property
    def key(self):
        return self.s

    @property
    def attribute(self):
        return self.v


class Label:

    def __init__(self):
        self.sv = []
        self.ind = [None for i in range(5)]

    def __getitem__(self, i):
        if i == 0:
            raise IndexError
        return self.sv[i-1]  # compensate for 1 start

    def __eq__(self, other):
        return (type(other) == Label and self.sv == other.sv and self.ind == other.ind)

    @classmethod
    def make(cls, s, v, *arg):
        if len(arg) < 4 and len(arg) > 0:
            raise TypeError()
        tempLabel = Label()
        tempLabel.append(s, v)
        if len(arg) == 4:
            tempLabel.ind = list(arg)
        else:
            tempLabel.ind = [0, 0, 0, 0]
        return tempLabel

    def append(self, *arg):
        if(len(arg) & 1):
            raise TypeError("number of argument{arg} must be even number")
        for i in range(0, len(arg), 2):
            self.sv.append(SV(arg[i], arg[i+1]))
        return self

    @classmethod
    def noChild(cls):
        return cls.make(1, constant.PERPEN_SYM, 0, 0, 0, 0)

    def __str__(self):
        return f'{self.sv + self.ind}'

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self[1].s

    def containPerpen(self):
        return sum([sv.v == constant.PERPEN_SYM for sv in self.sv])

    def lastSix(self):
        tempLabel = copy.deepcopy(self)
        tempLabel.sv = [tempLabel.sv[-1]]
        return tempLabel

    def deleteLast(self, n):
        if n == 4:
            return [sv for sv in self.sv]
        return self.sv[0: int(-(n-2)/2 + 1)]
