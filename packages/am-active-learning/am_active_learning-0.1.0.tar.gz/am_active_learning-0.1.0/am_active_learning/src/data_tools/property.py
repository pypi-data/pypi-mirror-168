class Property:
    def __init__(self, name, base):
        self.name = name
        self.base = base
        self.target = 'max'
        self.dual = False
    
    def set_dual(self, dual):
        self.dual = dual

    def set_target(self, target):
        if target == 'min' or target == 'max' or isinstance(target, int()):
            self.target = target
        else:
            raise Exception("Target needs to be min, max, or a value.")

    def __repr__(self):
        return self.name