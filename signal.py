class Signal:
    def __init__(self):
        self.slots = []

    def addSlot(self, slot):
        self.slots.append(slot)

    def removeSlot(self, slot):
        self.slots.remove(slot)

    def signal(self):
        for slot in self.slots:
            slot()
