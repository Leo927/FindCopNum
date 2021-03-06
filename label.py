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
        if i > 0:
            return self.sv[i-1]  # compensate for 1 start
        elif i < 0:
            return self.sv[i]
        else:
            raise IndexError

    @property
    def weakBranInd(self):
        '''returns the k-weakly-branching indicator stored in the label'''
        return self.ind[0]

    @property
    def weaklyCounter(self):
        '''returns the k-weakly counter stored in the label'''
        return self.ind[1]

    @property
    def prebranInd(self):
        '''returns the k-pre-branching indicator stored in the label'''
        return self.ind[2]

    @property
    def initialCounter(self):
        '''returns the k-initial-counter stored in the label'''
        return self.ind[3]

    def __len__(self):
        return len(self.sv)

    def __eq__(self, other):
        return (type(other) == Label and self.sv == other.sv and self.ind == other.ind)

    @classmethod
    def make(cls, s, v, *arg):
        '''used to create simple label with 1 length.
        Example: 
            Label.make(1,5,0,1,0,0) = [(1,5),0,0,0,0]'''
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
        '''used to append key-attribute pairs to an existing label. 
        Can be used to create longer Label. 
        Example: 
            Label.make(1,5).appen(2,3) = [(1,5),(2,3),0,0,0,0]'''
        if(len(arg) & 1):
            raise TypeError("number of argument{arg} must be even number")
        for i in range(0, len(arg), 2):
            self.sv.append(SV(arg[i], arg[i+1]))
        return self

    @classmethod
    def noChild(cls):
        '''return a quick instantce of label for nodes with no children
        returns [(0,⊥),0,0,0,0]'''
        return cls.make(1, constant.PERPEN_SYM, 0, 0, 0, 0)

    def __str__(self):
        return f'{self.sv + self.ind}'

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self[1].s

    def containPerpen(self):
        '''return True if the label contains ⊥ in any of its attributes, else False'''
        return sum([sv.v == constant.PERPEN_SYM for sv in self.sv])

    def lastSix(self):
        '''Returns the last six items in the label using the terminology in the project documentaion.
        Example:
            lastSix([(6,2),(3,1),0,0,1,0]) = [(3,1),0,0,0,0]'''
        tempLabel = copy.deepcopy(self)
        tempLabel.sv = [tempLabel.sv[-1]]
        return tempLabel

    def deleteLast(self, n):
        '''Returns a copy of the object with the last n items removed
        Example:
            ([(6,2),(3,1),0,0,1,0]).deleteLast(6) = [(6,2)]'''
        if n == 4:
            return copy.deepcopy(self.sv)
        return self.sv[0: int(-(n-4)/2)]


if __name__ == "__main__":
    l = Label.make(1, 2)
    print(l)
    print(l.deleteLast(6))
