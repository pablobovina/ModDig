
class Module:

    def __init__(self, name, registers):
        self.registers = registers
        self.name = name

    def add_register(self, name, register):
        self.registers[name] = register

    def remove_register(self, name):
        return self.registers.pop(name)
