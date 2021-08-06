class Signal:
    def __init__(self):
        self.slots = []

    def addSlot(self, slot):
        self.slots.append(slot)

    def removeSlot(self, slot):
        self.slots.remove(slot)

    def signal0(self):
        for slot in self.slots:
            slot()

    def signal1(self, x):
        for slot in self.slots:
            slot(x)